from django.contrib import admin
from .models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        '__str__',
        'content',
        'created_at',
        'updated_at',
        'like_count',
        'comment_count',
        'author',
    )
