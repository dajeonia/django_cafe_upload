import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime

def get_bands(token):
	url = f'https://openapi.band.us/v2.1/bands?access_token={token}'
	res = requests.get(url)
	if (res.status_code == 200):
		bands = res.json()
		return (bands['result_data']['bands'])
	else:
		return (0)

def get_band_title(url):
	if "band.us/band/" not in url:
		return (0)
	res = requests.get(url)
	soup = BeautifulSoup(res.text, 'html.parser')
	str = soup.title.string
	return (str[:-7])

def get_band_key(token, url):
	bands = get_bands(token)
	title = get_band_title(url)
	for b in bands:
		if (b['name'] == title):
			return (b['band_key'])
	return (0)

def get_articles(token, band_key):
	url = f'https://openapi.band.us/v2/band/posts?access_token={token}&band_key={band_key}&locale=ko_KR'
	res = requests.get(url)
	if (res.status_code == 200):
		items = res.json()['result_data']['items']
		list = []
		for n, item in enumerate(items):
			article = {}
			article['number'] = n
			article['author'] = item['author']['name']
			article['subject'] = item['content'].split("\n")[0]
			article['content'] = item['content']
			article['id'] = item['post_key']
			article['created_at'] = item['created_at']
			list.append(article)
		return (list)
	else:
		print("Error: ", res.status_code)
		return (0)


def convert_time(ms):
	timestamp_s = ms / 1000.0
	dt_object = datetime.fromtimestamp(timestamp_s)
	return (dt_object)

def get_band_article(url):
#band_token = 'ZQAAARzsjS9ambaV0vg0Mda6g8mchdEN164KIF7LDVPq1vpoBPYxEd-ark4wCmCs2f8Oc2dIazazSC_vlfgM2T2kA90aooZ0qCvQ2xU55w9OryBW'
	band_token ='ZQAAAS__GLH_jlSZ6JERtocaz84lJHDf4KPLCevoFN5dCk3pBewjmkkhphqU70NkWjCOE3ECNeUC3G-_VYLv8_wbUNX5dwXl2EsWxTLJHQ8JDVrT'

	key = get_band_key(band_token, url)
	if key == 0:
		raise Exception("가입되지 않았거나 잘못된 URL입니다.")
	list = get_articles(band_token, key)
	if list == 0:
		raise Exception("목록을 가져오는 데 실패하였습니다.")
	return (list)
