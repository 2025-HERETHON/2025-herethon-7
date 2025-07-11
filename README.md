# 2025-herethon-7
2025 여기톤 : HER+ETHON 7팀

# 📚 감정 기반 독서 기록 플랫폼 - SHELF

---

## 🌟 서비스 소개
여성의 감정을 존중하는 감정 기반 독서 기록 플랫폼입니다.
책을 읽고 느낀 ‘여성혐오’, ‘분노’, ‘위로’ 같은 감정을 자유롭게 기록하세요.
여성만을 위한 공간에서 검열 없이 감정을 꺼내고 공감받을 수 있습니다.
감정 태그로 비슷한 경험을 나눈 여성들과 연결됩니다.
별점 중심의 리뷰가 아닌, 진짜 감정을 중심에 둔 독서 기록을 지향합니다.
이제 감정을 숨기지 말고, 함께 나누세요.

---

## 💻 기술 스택
<span>프론트엔드: </span> 
<img src="https://img.shields.io/badge/html-E34F26?style=for-the-badge&logo=html5&logoColor=white"> 
<img src="https://img.shields.io/badge/css-1572B6?style=for-the-badge&logo=css3&logoColor=white"> 
<img src="https://img.shields.io/badge/javascript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black">

<span>백엔드: </span>
<img src="https://img.shields.io/badge/python-3776AB?style=for-the-badge&logo=python&logoColor=white"> 
<img src="https://img.shields.io/badge/django-092E20?style=for-the-badge&logo=Django&logoColor=white">

<span>기획·디자인: </span> 
<img src="https://img.shields.io/badge/figma-F24E1E?style=for-the-badge&logo=figma&logoColor=white">

---

## 👩‍💻 팀원 소개
|이정음|김지원|유진서|김민솔|양현빈|
|:------:|:------:|:------:|:------:|:------:|
|<img width="100" alt="lje" src="https://github.com/user-attachments/assets/0d43f36a-9034-443d-b66d-0a8687c2ace9" />|<img width="100" alt="kjw" src="https://github.com/user-attachments/assets/15909954-7449-4951-b59b-5f1e6d562690" />|<img width="100" alt="yjs" src="https://github.com/user-attachments/assets/0f508f7a-8945-40e1-8290-14d9b143d9fd" />|<img width="100" alt="kms" src="https://github.com/user-attachments/assets/f062f42b-077c-4c49-88d3-377968f0e02c" />|<img width="100" alt="yhb" src="https://github.com/user-attachments/assets/bee2c402-0b4e-40b7-8cff-d0886a19b7aa" />|
|기획 · 디자인|프론트엔드|프론트엔드|백엔드|백엔드|

---

### 📁 폴더 구조
```bash
shelf/
├── __pycache__
├── __init__.py
├── asgi.py
├── settings.py
├── urls.py
├── wsgi.py
accounts/
├── __pycache__
├── migrations/
├── templates/
│   └── accounts/
│       ├── delete_account.html
│       ├── edit_profile.html
│       ├── emotion_stats.html
│       ├── find_id.html
│       ├── login.html
│       ├── my_reviews.html
│       ├── my_scraps.html
│       ├── mypage.html
│       ├── password_reset_complete.html
│       ├── password_reset_confirm.html
│       ├── password_reset_form.html
│       ├── password_reset_invalid.html
│       ├── password_reset_sent.html
│       └── signup.html
├── __init__.py
├── admin.py
├── apps.py
├── forms.py
├── models.py
├── tests.py
├── urls.py
└── views.py
contents/
├── __pycache__
├── migrations/
├── templates/
│   └── contents/
│       ├── book_search.html
│       ├── create.html
│       ├── detail.html
│       ├── filter_reviews.html
│       ├── intro.html
│       ├── main.html
│       ├── search_reviews.html
│       └── update.html
├── __init__.py
├── admin.py
├── apps.py
├── models.py
├── tests.py
├── urls.py
└── views.py
static/
├── css/
│   ├── base_menu.css
│   ├── base.css
│   ├── book_search.css
│   ├── create.css
│   ├── delete_account.css
│   ├── detail.css
│   ├── edit_profile.css
│   ├── emotion_status.css
│   ├── filter_reviews.css
│   ├── find_id.css
│   ├── intro.css
│   ├── login.css
│   ├── main.css
│   ├── my_reviews_scraps.css
│   ├── mypage.css
│   ├── password_reset_complete.css
│   ├── password_reset_form.css
│   ├── search_reviews.css
│   ├── signup.css
│   └── update.css
├── js/
│   └── search-clear.js
templates/
├── base_menu.html
└── base.html
manage.py
```

---

## 💻 개발 환경 실행 방법
```bash
python -m venv venv
source venv\Scripts\activate
pip install -r requirements.txt
python manage.py runserver
```
