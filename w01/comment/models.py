from django.db import models

# Create your models here.
from django.db import models
from loginpage.models import Member  # Member 모델을 가져옴
from diary.models import Content

# 댓글 모델
class Comment(models.Model):
    content = models.ForeignKey(Content, on_delete=models.CASCADE)  # 연결된 게시글
    member = models.ForeignKey(Member, on_delete=models.CASCADE)  # 작성자
    text = models.TextField()  # 댓글 내용
    created_at = models.DateTimeField(auto_now_add=True)  # 댓글 작성 시간
    updated_at = models.DateTimeField(auto_now=True)  # 댓글 수정 시간

    def __str__(self):
        return f"{self.member.name} - {self.text[:20]}"

# 좋아요 모델
class Like(models.Model):
    content = models.ForeignKey(Content, on_delete=models.CASCADE)  # 연결된 게시글
    member = models.ForeignKey(Member, on_delete=models.CASCADE)  # 좋아요 누른 유저
    liked_at = models.DateTimeField(auto_now_add=True)  # 좋아요 누른 시간

    class Meta:
        unique_together = ('content', 'member')  # 같은 사용자가 같은 게시글에 좋아요를 중복으로 누를 수 없음
