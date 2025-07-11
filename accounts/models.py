from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    user_id = models.CharField(max_length=20, unique=True)
    nickname = models.CharField(max_length=30)
    profile_image = models.ImageField(
        upload_to='profile_images/', 
        default='profile_images/default.png',
        blank=True,
        null=True
    )
    gender = models.CharField(
        max_length=10,
        choices=[
            ('M', '남성'),
            ('F', '여성'),
            ('O', '기타'),
        ]
    )
    USERNAME_FIELD = 'user_id'
    REQUIRED_FIELDS = ['username', 'email']

    def __str__(self):
        return self.user_id