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


class Review(models.Model):
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews')

    book_title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    cover_image = models.ImageField(upload_to=upload_filepath, blank=True, null=True)

    tags = models.ManyToManyField(to=Tag, through='ReviewTag', blank=True, related_name='reviews')

    rating = models.PositiveSmallIntegerField(default=0)
    short_comment = models.CharField(max_length=100) 
    detailed_review = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.book_title} - {self.short_comment[:20]}"


class ReviewTag(models.Model):
    review = models.ForeignKey(to=Review, on_delete=models.CASCADE, related_name='review_tags')
    tag = models.ForeignKey(to=Tag, on_delete=models.CASCADE, related_name='review_tags')

    def __str__(self):
        return f"{self.review} - {self.tag}"