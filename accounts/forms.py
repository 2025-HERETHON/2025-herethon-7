from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    GENDER_CHOICES = [
        ('M', '남성'),
        ('F', '여성'),
        ('O', '기타'),
    ]

    gender = forms.ChoiceField(
        choices=GENDER_CHOICES,
        widget=forms.RadioSelect,
        label='성별'
    )

    class Meta:
        model = CustomUser
        fields = ('user_id', 'nickname', 'gender', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)

        self.fields['user_id'].label = '아이디'
        self.fields['user_id'].widget.attrs.update({
            'placeholder': '숫자, 영문 조합 8자 이상',
            'class': 'form-input'
        })

        self.fields['nickname'].label = '닉네임'
        self.fields['nickname'].widget.attrs.update({
            'placeholder': '',
            'class': 'form-input'
        })

        self.fields['gender'].label = '성별'
        self.fields['gender'].widget.attrs.update({
            'class': 'form-input'
        })

        self.fields['email'].label = '이메일'
        self.fields['email'].widget.attrs.update({
            'placeholder': 'example@email.com',
            'class': 'form-input'
        })

        self.fields['password1'].label = '비밀번호'
        self.fields['password1'].widget.attrs.update({
            'placeholder': '숫자, 영문 조합 8자 이상',
            'class': 'form-input'
        })

        self.fields['password2'].label = '비밀번호 확인'
        self.fields['password2'].widget.attrs.update({
            'placeholder': '비밀번호 재입력',
            'class': 'form-input'
        })


class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': '아이디',
            'class': 'form-input'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': '비밀번호',
            'class': 'form-input'
        })
    )
