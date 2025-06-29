from django.shortcuts import render, redirect, get_object_or_404
from .models import Tag, Review

# Create your views here.
def main(request):
    return render(request, 'contents/main.html')

def create(request):
    tags = Tag.objects.all()

    if request.method == "POST":
        book_title = request.POST.get('book_title')
        author = request.POST.get('author')
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
            book_title=book_title,
            author=author,
            cover_image=cover_image,
            rating=rating,
            short_comment=short_comment,
            detailed_review=detailed_review
        )

        for tag in tag_list:
            review.tags.add(tag)

        return redirect('contents:main')

    return render(request, 'contents/create.html', {'tags': tags})