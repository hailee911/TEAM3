from django.contrib import admin
from comment.models import Comment, Like


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['content', 'member', 'text', 'created_at', 'updated_at']
    
@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ['content', 'member', 'liked_at']