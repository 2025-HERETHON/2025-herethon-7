from django.contrib import admin
from .models import Tag, Review, Book, Comment, ReviewTag, FeaturedAuthor

# Register your models here.
admin.site.register(Tag)
admin.site.register(Review)
admin.site.register(Book)
admin.site.register(Comment)
admin.site.register(ReviewTag)
admin.site.register(FeaturedAuthor)