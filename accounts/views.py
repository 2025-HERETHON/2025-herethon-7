from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from .forms import CustomUserCreationForm, CustomLoginForm
from django.contrib.auth.decorators import login_required
from contents.models import Scrap, Tag
from django.db.models import Count

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