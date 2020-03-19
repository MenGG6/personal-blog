from django.urls import path
from . import views


app_name = 'article'
#path函数中的反斜杠‘ / ’很重要！！！
urlpatterns = [
    path('article_list/', views.article_list, name='article_list'),
    path('article_context/<int:id>/', views.article_context, name='article_context'),
    path('article_create/', views.article_create, name='article_create'),
    path('article_delete/<int:id>/', views.article_delete, name='article_delete'),
    # 安全删除文章
    path('article-safe-delete/<int:id>/', views.article_safe_delete, name='article_safe_delete'),
    path('article_edit/<int:id>/', views.article_edit, name='article_edit'),
]
