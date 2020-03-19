from django.urls import path
from . import views


app_name = 'users'
#path函数中的反斜杠‘ / ’很重要！！！
#path的name参数是给url起名的
urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.user_register, name='register'),
    path('delete/<int:id>/', views.user_delete, name='delete'),
    path('display/<int:id>/', views.user_display, name='display'),
    path('edit/<int:id>/', views.user_edit, name='edit'),
]