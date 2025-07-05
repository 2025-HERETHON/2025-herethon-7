import requests
import random
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from .models import Book, Tag, Review, Comment, FeaturedAuthor
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Count
from django.utils import timezone

def main(request):
    sort = request.GET.get('sort', 'recent')
    if sort == 'popular':
        reviews = Review.objects.annotate(
            num_likes=Count('like')
        ).order_by('-num_likes', '-created_at')
    else: 
        reviews = Review.objects.order_by('-created_at')

    top_books = Book.objects.annotate(review_count=Count('reviews')).order_by('-review_count')[:5]

    all_tags = Tag.objects.annotate(review_count=Count('reviews')).filter(review_count__gt=0)
    random_tag = random.choice(all_tags) if all_tags else None

    recommended_reviews = []
    if random_tag:
        all_recommendations = Review.objects.filter(tags=random_tag).order_by('-created_at')
        unique_books = {}
        for review in all_recommendations:
            if review.book_id not in unique_books:
                unique_books[review.book_id] = review
            if len(unique_books) >= 5:
                break
        recommended_reviews = list(unique_books.values())

    now = timezone.now()

    author = FeaturedAuthor.objects.filter(
        featured_month__year=now.year,
        featured_month__month=now.month
    ).first()

    if author and author.representative_work:
        works = [w.strip() for w in author.representative_work.split(',')]
    else:
        works = []

    feminism_tag = Tag.objects.filter(name='여성중심서사').first()
    feminism_reviews = []
    if feminism_tag:
        all_feminism_reviews = Review.objects.filter(tags=feminism_tag).annotate(
            num_likes=Count('like')
        ).order_by('-num_likes', '-created_at')

        unique_books = {}
        for review in all_feminism_reviews:
            if review.book_id not in unique_books:
                unique_books[review.book_id] = review
            if len(unique_books) >= 3:
                break
        feminism_reviews = list(unique_books.values())

    return render(request, 'contents/main.html', {
        'reviews': reviews,
        'sort': sort,
        'top_books': top_books,
        'random_tag': random_tag,
        'recommended_reviews': recommended_reviews,
        'featured_author': author,
        'representative_works': works,
        'feminism_reviews': feminism_reviews,
    })

def book_search(request):
    query = request.GET.get('q')
    results = []

    if query:
        url = 'https://www.googleapis.com/books/v1/volumes'
        params = {
            'q': query,
            'key': settings.GOOGLE_BOOKS_API_KEY,
            'maxResults': 10
        }
        response = requests.get(url, params=params)
        data = response.json()
        for item in data.get('items', []):
            volume_info = item.get('volumeInfo', {})
            image_links = volume_info.get('imageLinks', {})
            thumbnail = image_links.get('thumbnail')

            results.append({
                'google_book_id': item.get('id'),
                'title': volume_info.get('title', '제목 없음'),
                'author': ', '.join(volume_info.get('authors', [])) or '작자 미상',
                'thumbnail': thumbnail or '', 
            })

    return render(request, 'contents/book_search.html', {
        'query': query,
        'results': results
    })

@login_required
def select_book(request):
    if request.method == 'POST':
        google_book_id = request.POST.get('google_book_id')
        title = request.POST.get('title')
        author = request.POST.get('author')
        thumbnail = request.POST.get('thumbnail', '')

        book, _ = Book.objects.get_or_create(
            google_book_id=google_book_id,
            defaults={
                'title': title,
                'author': author,
                'thumbnail': thumbnail
            }
        )
        return redirect('contents:create', book_id=book.id)

    return redirect('contents:book_search')

@login_required
def create(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    tags = Tag.objects.all()

    if request.method == "POST":

        try:
            rating = int(request.POST.get('rating'))
        except (ValueError, TypeError):
            rating = 0

        short_comment = request.POST.get('short_comment')
        detailed_review = request.POST.get('detailed_review')

        tag_ids = request.POST.getlist('tag')
        tag_list = [get_object_or_404(Tag, id=tag_id) for tag_id in tag_ids]

        review = Review.objects.create(
            user=request.user,
            book=book,
            rating=rating,
            short_comment=short_comment,
            detailed_review=detailed_review
        )

        for tag in tag_list:
            review.tags.add(tag)

        return redirect('contents:main')

    return render(request, 'contents/create.html', {'book': book, 'tags': tags, 'rating_range': range(1, 6)})

def detail(request, id):
    review = get_object_or_404(Review, id=id)
    return render(request, 'contents/detail.html', {'review': review})

@login_required
def update(request, id):
    review = get_object_or_404(Review, id=id)
    tags = Tag.objects.all()

    if request.method == 'POST':
        review.short_comment = request.POST.get('short_comment')
        review.detailed_review = request.POST.get('detailed_review')
        review.rating = int(request.POST.get('rating', 0))

        tag_ids = request.POST.getlist('tag')
        review.save()
        review.tags.set(Tag.objects.filter(id__in=tag_ids))
        return redirect('contents:detail', review.id)

    return render(request, 'contents/update.html', {'review': review, 'tags': tags, 'rating_range': range(1, 6)})

@login_required
def delete(request, id):
    review = get_object_or_404(Review, id=id)
    review.delete()
    return redirect('contents:main')

@login_required
def like(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    user = request.user
    if user in review.like.all():
        review.like.remove(user)
    else:
        review.like.add(user)
    return redirect('contents:detail', review_id)

@login_required
def dislike(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    user = request.user
    if user in review.dislike.all():
        review.dislike.remove(user)
    else:
        review.dislike.add(user)
    return redirect('contents:detail', review_id)

@login_required
def scrap(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    user = request.user
    if user in review.scrap.all():
        review.scrap.remove(user)
    else:
        review.scrap.add(user)
    return redirect('contents:detail', review_id)

@login_required
def create_comment(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Comment.objects.create(
                review=review,
                content=content,
                user=request.user
            )
    return redirect('contents:detail', id=review_id)

@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    review_id = comment.review.id
    comment.delete()
    return redirect('contents:detail', review_id)

def search_reviews(request):
    query = request.GET.get('q')
    reviews = Review.objects.all()

    if query:
        reviews = reviews.filter(
            Q(book__title__icontains=query) | Q(book__author__icontains=query)
        )

    return render(request, 'contents/search_reviews.html', {
        'query': query,
        'reviews': reviews
    })

def popular_reviews(request):
    reviews = Review.objects.annotate(
        num_likes=Count('like')
    ).order_by('-num_likes', '-created_at')
    return render(request, 'contents/popular.html', {'reviews': reviews})

def filter_by_tags(request):
    tag_ids = request.GET.getlist('tags')
    tags = Tag.objects.all()
    reviews = Review.objects.all()
    selected_tags = []

    if tag_ids:
        tag_ids = list(map(int, tag_ids))
        selected_tags = Tag.objects.filter(id__in=tag_ids)
        for tag_id in tag_ids:
            reviews = reviews.filter(tags__id=tag_id)
        reviews = reviews.distinct().order_by('-created_at')
    else:
        reviews = reviews.order_by('-created_at')

    return render(request, 'contents/filter_reviews.html', {
        'reviews': reviews,
        'tags': tags,
        'selected_tags': selected_tags,
    })
