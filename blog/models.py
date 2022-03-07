from django.db import models
from django.utils import timezone
from taggit.managers import TaggableManager
from django.urls import reverse
from django.contrib.auth.models import User
from tinymce.models import HTMLField


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status='published')


class DraftManager(models.Manager):
    def get_queryset(self):
        return super(DraftManager, self).get_queryset().filter(status='draft')


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=220)
    body = HTMLField()
    thumbnail = models.ImageField(upload_to='post_thumbnails/%Y/%m/%d/')
    quote_author = models.CharField(blank=True, max_length=20)
    post_quote = models.CharField(blank=True, max_length=300)
    slug = models.SlugField(max_length=225, unique_for_date='published_date')
    status_choices = ('published', 'published'), ('draft', 'draft')
    status = models.CharField(max_length=10, choices=status_choices, default='draft')
    published_date = models.DateField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    tags = TaggableManager()
    objects = models.Manager()
    published = PublishedManager()
    draft = DraftManager()

    def post_detail_content(self):
        return reverse('blog:post_detail', args=[self.published_date, self.slug, self.id ])

    class Meta:
        ordering = ('-published_date',)

    def __str__(self):
        return self.title

class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='comments', null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('-created_at',)
