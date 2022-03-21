from django.db import models

# Create your models here.
class BoardMatching(models.Model):
    """
        id : no
        from_board_url : 가져올 게시판 url
        from_club_id : 가져올 카페 clubid
        from_menu_id : 가져올 게시판 menuid

        to_board_url : 업로드할 게시판 url
        to_club_id : 업로드할 카페 clubid
        to_menu_id : 업로드할 게시판 menuid

        from_article_no : 게시글 시작 index
        to_article_no : 게시글 끝 index

        user_no : 매칭 유저 번혼
        is_active : 활성화 여부
    """
    id = models.AutoField(primary_key=True)
    from_board_url = models.TextField()
    from_club_id = models.CharField(max_length=20)
    from_menu_id = models.CharField(max_length=20)

    to_board_url = models.TextField()
    to_club_id = models.CharField(max_length=20)
    to_menu_id = models.CharField(max_length=20)

    from_article_no = models.IntegerField()
    to_article_no = models.IntegerField()

    user_no = models.IntegerField()

    is_active = models.BooleanField()

    class Meta:
        db_table = 'board_matching'