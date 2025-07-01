from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('user_id', 'nickname', 'gender', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        self.fields['user_id'].label = '아이디'
        self.fields['nickname'].label = '닉네임'
        self.fields['gender'].label = '성별'
        self.fields['email'].label = '이메일'
        self.fields['password1'].label = '비밀번호'
        self.fields['password2'].label = '비밀번호 확인'

class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': '아이디'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': '비밀번호'})
    )