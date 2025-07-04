from django.db import models
from django.conf import settings

import os
from uuid import uuid4
from django.utils import timezone

def upload_filepath(instance, filename):
    today_str = timezone.now().strftime("%Y%m%d")
    file_basename = os.path.basename(filename)
    return f'{instance._meta.model_name}/{today_str}/{str(uuid4())}_{file_basename}'

# Create your models here.
class Tag(models.Model):
    TAG_TYPE_CHOICES = [
        ('primary', '1차 감정'),
        ('secondary', '2차 감정'),
    ]
    name = models.CharField(max_length=50, unique=True)
    tag_type = models.CharField(max_length=10, choices=TAG_TYPE_CHOICES)

    def __str__(self):
        return f"[{self.get_tag_type_display()}] {self.name}"

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    google_book_id = models.CharField(max_length=50, unique=True)
    thumbnail = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.title} - {self.author}"

class Review(models.Model):
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews')

    book = models.ForeignKey(to=Book, on_delete=models.CASCADE, related_name='reviews')
    cover_image = models.ImageField(upload_to=upload_filepath, blank=True, null=True)

    tags = models.ManyToManyField(to=Tag, through='ReviewTag', blank=True, related_name='reviews')

    rating = models.PositiveSmallIntegerField(default=0)
    short_comment = models.CharField(max_length=100) 
    detailed_review = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    like = models.ManyToManyField(to=settings.AUTH_USER_MODEL, through='Like', related_name='like_reviews')
    dislike = models.ManyToManyField(to=settings.AUTH_USER_MODEL, through='Dislike', related_name='dislike_reviews')
    scrap = models.ManyToManyField(to=settings.AUTH_USER_MODEL, through='Scrap', related_name='scrap_reviews')

    def __str__(self):
        return f"{self.book.title} - {self.short_comment[:20]}"


class ReviewTag(models.Model):
    review = models.ForeignKey(to=Review, on_delete=models.CASCADE, related_name='review_tags')
    tag = models.ForeignKey(to=Tag, on_delete=models.CASCADE, related_name='review_tags')

    def __str__(self):
        return f"{self.review} - {self.tag}"
    
class Like(models.Model):
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_likes')
    review = models.ForeignKey(to=Review, on_delete=models.CASCADE, related_name='review_likes')

class Dislike(models.Model):
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_dislikes')
    review = models.ForeignKey(to=Review, on_delete=models.CASCADE, related_name='review_dislikes')

class Scrap(models.Model):
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_scraps')
    review = models.ForeignKey(to=Review, on_delete=models.CASCADE, related_name='review_scraps')

class Comment(models.Model):
    review = models.ForeignKey(to=Review, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="comments")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'[{self.id}] {self.content[:20]}'

class FeaturedAuthor(models.Model):
    name = models.CharField(max_length=100)
    profile_image = models.ImageField(upload_to='authors/', blank=True, null=True)
    bio = models.TextField(blank=True)
    featured_month = models.DateField()
    representative_work = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.name} ({self.featured_month.strftime('%Y-%m')})"