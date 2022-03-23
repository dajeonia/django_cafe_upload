import os
import ssl
import sys
import json
import traceback
import bs4
import requests
import ast
import time
import re
import urllib.request
import datetime


from bs4 import BeautifulSoup
from requests import get
from selenium import webdriver
from selenium.webdriver.common.by import By
from urllib.error import HTTPError
from urllib.parse import urlencode

from board_matching.models import BoardMatching
from user_setting.models import UserSetting





def checkFolder(tempImgPath):
    try:
        if not os.path.exists(tempImgPath):
            os.makedirs(tempImgPath)
    except OSError:
        print ('os error')
        sys.exit(0)

def deleteAllFilesInFolder(tempImgPath):
    try:
        if os.path.exists(tempImgPath):
            for file in os.scandir(tempImgPath):
                os.remove(file.path)
        else:
            print("Directory Not Found")
            sys.exit(0)
    except OSError:
        print('OS Error')
        sys.exit(0)

def get_naver_token(driver, user):
    naver_cid = user.naver_cid
    naver_csec = user.naver_csec
    naver_redirect = "http://localhost"

    driver.get('https://nid.naver.com/nidlogin.login')

    id=user.naver_id
    pw=user.naver_pw
    driver.execute_script("document.getElementsByName('id')[0].value=\'"+id+"\'")
    driver.execute_script("document.getElementsByName('pw')[0].value=\'"+pw+"\'")

    driver.find_element(By.XPATH, '//*[@id="log.login"]').click()
    time.sleep(1)

    state = "REWERWERTATE"
    
    req_url='https://nid.naver.com/oauth2.0/authorize?response_type=code&client_id=%s&redirect_uri=%s&state=%s' % (naver_cid, naver_redirect, state)
    driver.get(req_url)
    

    
    try:
        time.sleep(3)
        driver.find_element(By.XPATH, '//*[@class="item_text"]').click()
        time.sleep(1)
        driver.find_element(By.XPATH, '//*[@class="btn_unit_on"]').click()
        time.sleep(1)
    except:
        print("권한 이미 허용됨")



    time.sleep(1)
    redirect_url = driver.current_url
    temp = re.split('code=',redirect_url)

    code = re.split('&state=', temp[1])[0]
    url = "https://nid.naver.com/oauth2.0/token?grant_type=authorization_code" + "&client_id=" + naver_cid   + "&client_secret=" + naver_csec + "&redirect_uri=" + naver_redirect + "'&code=" + code + "&state=" + state
    
    headers = {'X-Naver-Client-Id': naver_cid, 'X-Naver-Client-Secret':naver_redirect}
    response = requests.get(url,headers=headers)
    rescode = response.status_code
    token = ''
    if rescode == 200:
        response_body = response.json()

        token = response_body["access_token"]
    else:
        print("Error Code:", rescode)
        return None

    if len(token) == 0:
        return None
    return token

"""
type : 1
중고폰 게시판

type : 2
중고폰 단가표
"""
def crawl_cafe_contents(driver, access_token, upload_item):
    result = [0 for _ in range(2)] 
    """
    0 : failed,
    1 : success
    """
    addr=upload_item.from_board_url+'?iframe_url=/ArticleList.nhn%3Fsearch.clubid='+upload_item.from_club_id+'%26search.menuid='+upload_item.from_menu_id+'%26userDisplay=50%26search.page=1'
    
    driver.get(addr)
    driver.switch_to.frame('cafe_main')
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    soup = soup.find_all(class_='article-board m-tcol-c')[1]
    a_num_list = soup.findAll("div",{"class":"inner_number"})
    a_title_list = soup.findAll("a",{"class":"article"})
    a_writer_list = soup.findAll("a",{"class":"m-tcol-c"})
    a_regdate_list = soup.findAll("td",{"class":"td_date"})
    total_list = []
    article_link_list = []

    for a, b, c, d in zip(a_num_list, a_title_list, a_writer_list, a_regdate_list):
        list = []
        list.append(a.text)
        list.append(b.text.strip())
        list.append(c.text)
        list.append(d.text)
        total_list.append(list)
        article_link_list.append("https://cafe.naver.com/ArticleRead.nhn?clubid="+upload_item.from_club_id+"&page=1&userDisplay=50&menuid="+upload_item.from_menu_id+"&boardtype=L&articleid=" + a.text + "&referrerAllArticles=false")
        """
        for x in total_list:
        """
    for j in range(upload_item.to_article_no-1, upload_item.from_article_no-1, -1):
        try:
            time.sleep(50)
            adrs = "https://cafe.naver.com/ArticleRead.nhn?clubid="+upload_item.from_club_id+"&page=1&userDisplay=50&menuid="+upload_item.from_menu_id+"&boardtype=L&articleid=" + total_list[j][0] +"&referrerAllArticles=false"
            driver.get(adrs)
            time.sleep(10)
            driver.switch_to.frame('cafe_main')
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            list = soup.select('div.se-main-container')
            time.sleep(1)
            imgs = soup.select('a.se-module-image-link>img')
            imgList=[]
            for k in range(len(imgs)):
                src = imgs[k].get('src')
                if (len(src)):
                    list[0]=str(list[0]).replace(src, "#"+str(k))
                    saveUrl = 'temp_img/' + '/image'+str(k+1)+".jpg"

                    req = urllib.request.Request(src)
                    try:
                        imgUrl = urllib.request.urlopen(req, context=ssl._create_unverified_context()).read()
                        with open(saveUrl, "wb") as f:
                            f.write(imgUrl)
                    except urllib.error.HTTPError:
                        print('에러')
                        sys.exit(0)
                    imgList.append('image'+str(k+1)+".jpg")
                
            total_list[j].append(str(list[0]).replace("\"","\'"))
        except Exception as e:
            result[0]+=1
            print('업로드 실패', e)
            print(traceback.format_exc())
            continue
        if len(imgList):
            try:
                upload_cafe_with_image(access_token, total_list[j], imgList, upload_item)
                result[1]+=1
            except:
                result[0]+=1
                print('업로드 실패', e)
                print(traceback.format_exc())
        else:
            try:
                upload_cafe(access_token, total_list[j], upload_item)
                result[1]+=1
            except Exception as e:
                result[0]+=1
                print('업로드 실패', e)
                print(traceback.format_exc())
                """
                for xx in list:
                    content = ''
                    content += xx.text.strip()
                    print(content)
                """
        deleteAllFilesInFolder('temp_img/')
    return result

def upload_cafe(access_token, contentList, upload_item):
    header = "Bearer " + access_token
    clubid = upload_item.to_club_id
    menuid = upload_item.to_menu_id
    url = "https://openapi.naver.com/v1/cafe/" + clubid + "/menu/" + menuid + "/articles"
    subject = urllib.parse.quote(contentList[1])
    content = urllib.parse.quote(contentList[4])
    data = urlencode({'subject': subject, 'content': content}).encode()
    request = urllib.request.Request(url, data=data)
    request.add_header("Authorization", header)
    response = urllib.request.urlopen(request, context=ssl._create_unverified_context())
    rescode = response.getcode()
    if(rescode==200):
        response_body = response.read()
        print(response_body.decode('utf-8'))
    else:
        print("Error Code:" + rescode)

def upload_cafe_with_image(access_token, contentList, imgList, upload_item):
    header = "Bearer " + access_token
    clubid = upload_item.to_club_id
    menuid = upload_item.to_menu_id
    url = "https://openapi.naver.com/v1/cafe/" + clubid + "/menu/" + menuid + "/articles"
    subject = urllib.parse.quote(contentList[1])
    content = urllib.parse.quote(contentList[4])
    data = {'subject': subject, 'content': content}
    files=[]
    for img in imgList:
        files.append(('image', (img, open('temp_img/'+"/"+img, 'rb'), 'image/jpeg',{'Expires': '0'})))
    headers = {'Authorization': header }
    response = requests.post(url, headers = headers, data=data, files=files, verify=False)
    rescode = response.status_code
    if(rescode==200):
        print(response.text)
    else:
        print("Error Code:" + rescode)

def main_function():
    print("\n\n",datetime.datetime.now())
    chrome_options =webdriver.ChromeOptions()

    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')

    """
    display = Display(visible=0, size=(1024,768))
    display.start()
    """
    driver = webdriver.Chrome('/Users/mkcho1997/Project/chromedriver', chrome_options=chrome_options)
    checkFolder('temp_img/')
    for user in UserSetting.objects.all():
        access_token = get_naver_token(driver, user)
        print(access_token)
        print(user.naver_id+" 업로드")
        uploadList =BoardMatching.objects.filter(user_no = user.id)
        for upload_item in uploadList:
            res = crawl_cafe_contents(driver, access_token, upload_item)
            print("성공 : "+str(res[1]) +", 실패 : "+str(res[0]))
    driver.quit()
    deleteAllFilesInFolder('temp_img/')
"""
upload_cafe(access_token, res)
"""
