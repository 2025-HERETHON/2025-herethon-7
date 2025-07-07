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
        label='아이디',
        widget=forms.TextInput(attrs={'autofocus': True})
    )
    password = forms.CharField(
        label='비밀번호',
        strip=False,
        widget=forms.PasswordInput,
    )

class PasswordResetRequestForm(forms.Form):
    user_id = forms.CharField(label='아이디', max_length=150)
    email = forms.EmailField(label='이메일')

class DeleteAccountForm(forms.Form):
    password = forms.CharField(
        label="비밀번호 확인",
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password'})
    )

class FindIDForm(forms.Form):
    email = forms.EmailField(label='이메일')

class CustomUserChangeForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('nickname', 'profile_image')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nickname'].label = '닉네임'
        self.fields['profile_image'].label = '프로필 이미지'