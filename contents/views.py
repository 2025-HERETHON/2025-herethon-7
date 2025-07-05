import requests
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from .models import Book, Tag, Review

# Create your views here.
def main(request):
    reviews = Review.objects.all().order_by('-created_at')
    return render(request, 'contents/main.html', {'reviews': reviews})

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
            results.append({
                'google_book_id': item.get('id'),
                'title': volume_info.get('title', '제목 없음'),
                'author': ', '.join(volume_info.get('authors', [])) or '작자 미상',
            })

    return render(request, 'contents/book_search.html', {'query': query, 'results': results})

def select_book(request):
    if request.method == 'POST':
        google_book_id = request.POST.get('google_book_id')
        title = request.POST.get('title')
        author = request.POST.get('author')

        book, _ = Book.objects.get_or_create(
            google_book_id=google_book_id,
            defaults={'title': title, 'author': author}
        )

        return redirect('contents:create', book_id=book.id)
    return redirect('contents:book_search')

def create(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    tags = Tag.objects.all()

    if request.method == "POST":
        cover_image = request.FILES.get('cover_image')

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
            cover_image=cover_image,
            rating=rating,
            short_comment=short_comment,
            detailed_review=detailed_review
        )

        for tag in tag_list:
            review.tags.add(tag)

        return redirect('contents:main')

    return render(request, 'contents/create.html', {'book': book, 'tags': tags})