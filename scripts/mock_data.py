from contents.models import Book, Review, Tag, ReviewTag, Like, Dislike, Scrap, Comment, FeaturedAuthor
from django.contrib.auth import get_user_model
from django.utils import timezone
import random

User = get_user_model()

# ✅ 데이터 초기화
Comment.objects.all().delete()
Like.objects.all().delete()
Dislike.objects.all().delete()
Scrap.objects.all().delete()
ReviewTag.objects.all().delete()
Review.objects.all().delete()
Book.objects.all().delete()
Tag.objects.all().delete()
FeaturedAuthor.objects.all().delete()

# ✅ 유저 생성
user, _ = User.objects.get_or_create(username="testuser")

# ✅ 태그 생성
primary_tags = [Tag.objects.create(name=f"기쁨", tag_type="primary")]
secondary_tags = [Tag.objects.create(name=f"감동", tag_type="secondary")]
all_tags = primary_tags + secondary_tags

# ✅ 책 생성
books = []
for i in range(1, 6):
    book = Book.objects.create(
        title=f"샘플 책 {i}",
        author=f"작가 {i}",
        google_book_id=f"mock-book-{i}",
        thumbnail="https://via.placeholder.com/150x200.png?text=Book+Cover"
    )
    books.append(book)

# ✅ 리뷰 + ReviewTag 생성
reviews = []
for book in books:
    for j in range(1, 3):
        review = Review.objects.create(
            user=user,
            book=book,
            rating=random.randint(1, 5),
            short_comment=f"{book.title}에 대한 한 줄 리뷰 {j}",
            detailed_review=f"이 책은 정말 인상 깊었어요. #{j}"
        )
        reviews.append(review)

        # 태그 연결 (랜덤 1~2개)
        selected_tags = random.sample(all_tags, k=random.randint(1, 2))
        for tag in selected_tags:
            ReviewTag.objects.create(review=review, tag=tag)

# ✅ 좋아요 / 싫어요 / 스크랩 임의 생성
for review in reviews:
    if random.random() < 0.7:
        Like.objects.create(user=user, review=review)
    if random.random() < 0.3:
        Dislike.objects.create(user=user, review=review)
    if random.random() < 0.5:
        Scrap.objects.create(user=user, review=review)

# ✅ 댓글 생성
for review in reviews:
    for i in range(random.randint(1, 2)):
        Comment.objects.create(
            review=review,
            user=user,
            content=f"{review.book.title}에 대한 댓글 {i+1}"
        )

print("🟢 Mock 데이터 전체 생성 완료")
