from django.urls import path
from .views import *


app_name = 'blogapp'
urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('articles/<slug:article_name>/', ArticleView.as_view(), name='articles'),
    path('about/', AboutView.as_view(), name='about'),
    path('archives/', ArchiveView.as_view(), name='archives'),
    path('categories/', CategoryView.as_view(), name='categories'),
    path('categories/<slug:category_name>/', DetailCategoryView.as_view(), name='detail_category'),
    path('tags/', TagView.as_view(), name='tags'),
    path('tags/<slug:tag_name>/', DetailTagView.as_view(), name='detail_tag'),
    path('links/', LinkView.as_view(), name='links'),
    path('like/', like, name='like')
]
