from contents.models import Book, Review
from django.contrib.auth import get_user_model
import random

User = get_user_model()

# 유저 하나 생성 (중복 방지 위해 get_or_create)
user, _ = User.objects.get_or_create(username="testuser")

# 책 및 리뷰 초기화
Review.objects.all().delete()
Book.objects.all().delete()

books = []
for i in range(1, 6):
    book = Book.objects.create(
        title=f"샘플 책 {i}",
        author=f"작가 {i}",
        thumbnail=f"https://via.placeholder.com/150?text=책+{i}",
        google_book_id=f"mock-book-{i}"
    )
    books.append(book)

# 리뷰 생성
for book in books:
    for j in range(1, 3):
        Review.objects.create(
            user=user,
            book=book,
            rating=random.randint(1, 5),
            short_comment=f"{book.title}에 대한 한 줄 코멘트 {j}",
            detailed_review=f"이 책 정말 좋아요. 추천합니다! #{j}"
        )

print("🟢 Review mock 데이터 생성 완료")
