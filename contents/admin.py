from django.contrib import admin
from .models import Tag, Review, Book

# Register your models here.
admin.site.register(Tag)
admin.site.register(Review)
admin.site.register(Book)