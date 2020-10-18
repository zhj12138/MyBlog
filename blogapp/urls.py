from django.urls import include, path
from .views import *


app_name = 'blogapp'
url_patterns = [
    path('index/', IndexView.as_view(), name='index'),
    path('about/', AboutView.as_view(), name='about'),
    path('archieve/', ArchiveView.as_view(), name='archive'),
    path('category/', CategoryView.as_view(), name='category'),
    path('category/<slug:category_name>/', DetailCategoryView.as_view(), name='detail_category'),
    path('tag/', TagView.as_view(), name='tag'),
    path('tag/<slug:tag_name>/', DetailTagView.as_view(), name='detail_tag'),
    path('links/', LinkView.as_view(), name='links'),
]
