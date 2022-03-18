from pyexpat import model
from django.contrib import admin
from .models import Post, Comment


class CommentInline(admin.StackedInline):
    model = Comment
    extra = 0


class PostAdmin(admin.ModelAdmin):
    list_display = ('title','status','author',)
    list_filter = ('status','created_at')
    inlines =[
        CommentInline,
    ]

admin.site.register(Post, PostAdmin)
admin.site.register(Comment)