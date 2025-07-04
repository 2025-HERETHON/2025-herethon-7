from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from .forms import CustomUserCreationForm, CustomLoginForm
from django.contrib.auth.decorators import login_required
from contents.models import Scrap, Tag
from django.db.models import Count
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from .forms import PasswordResetRequestForm

def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.user_id
            user.save()
            return redirect('login')  
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/signup.html', {'form': form})

class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    authentication_form = CustomLoginForm

@login_required
def mypage(request):
    return render(request, 'accounts/mypage.html')

@login_required
def my_scraps(request):
    scraps = Scrap.objects.filter(user=request.user).select_related('review__book')
    return render(request, 'accounts/my_scraps.html', {'scraps': scraps})

@login_required
def my_reviews(request):
    reviews = request.user.reviews.select_related('book')
    return render(request, 'accounts/my_reviews.html', {'reviews': reviews})

@login_required
def emotion_stats(request):
    user = request.user

    user_top_tags = Tag.objects.filter(reviews__user=user).annotate(
        usage_count=Count('reviews')
    ).order_by('-usage_count', 'name')[:3]

    user_tag_distribution_raw = Tag.objects.filter(reviews__user=user).annotate(
        count=Count('reviews')
    )

    total_count = sum(tag.count for tag in user_tag_distribution_raw)

    user_tag_distribution = []
    for tag in user_tag_distribution_raw:
        percentage = (tag.count / total_count * 100) if total_count > 0 else 0
        user_tag_distribution.append({
            'name': tag.name,
            'type': tag.get_tag_type_display(),
            'count': tag.count,
            'percentage': round(percentage, 1),
        })

    return render(request, 'accounts/emotion_stats.html', { 'user_top_tags': user_top_tags, 'user_tag_distribution': user_tag_distribution})

User = get_user_model()

def password_reset_request(request):
    if request.method == "POST":
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            user_id = form.cleaned_data['user_id']
            email = form.cleaned_data['email']
            try:
                user = User.objects.get(user_id=user_id, email=email)
                token = default_token_generator.make_token(user)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                reset_link = request.build_absolute_uri(
                    f'/accounts/reset/{uid}/{token}/'
                )
                
                send_mail(
                    subject="비밀번호 재설정 안내",
                    message=f"아래 링크를 눌러 비밀번호를 재설정하세요:\n{reset_link}",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[email],
                )
                return render(request, "accounts/password_reset_sent.html")
            except User.DoesNotExist:
                form.add_error(None, "아이디와 이메일이 일치하지 않습니다.")
    else:
        form = PasswordResetRequestForm()
    return render(request, "accounts/password_reset_form.html", {"form": form})

from django.contrib.auth.forms import SetPasswordForm

def password_reset_confirm(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                return render(request, "accounts/password_reset_complete.html")
        else:
            form = SetPasswordForm(user)
        return render(request, "accounts/password_reset_confirm.html", {'form': form})
    else:
        return render(request, "accounts/password_reset_invalid.html")