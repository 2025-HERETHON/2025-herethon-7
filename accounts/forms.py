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

    def clean_gender(self):
        gender = self.cleaned_data.get('gender')
        if gender != 'F':
            raise forms.ValidationError("현재는 '여성'만 가입이 가능합니다.")
        return gender

class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': '아이디',
            'class': 'form-input'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': '비밀번호'})
    )

class PasswordResetRequestForm(forms.Form):
    user_id = forms.CharField(
        label='아이디',
        max_length=150,
        widget=forms.TextInput(attrs={
            'placeholder': '가입한 아이디를 입력하세요',
            'class': 'input-field',
        })
    )
    email = forms.EmailField(
        label='이메일',
        widget=forms.EmailInput(attrs={
            'placeholder': '가입한 이메일 주소를 입력하세요',
            'class': 'input-field',
        })
    )
class DeleteAccountForm(forms.Form):
    password = forms.CharField(
        label="비밀번호 확인",
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password'})
    )

class FindIDForm(forms.Form):
    email = forms.EmailField(
        label='이메일',
        widget=forms.EmailInput(attrs={
            'placeholder': '이메일을 입력하세요'
        })
    )

class CustomUserChangeForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('nickname', 'profile_image')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nickname'].label = ''
        self.fields['profile_image'].label = ''
