from django.urls import path
from . import views
app_name = 'liudong'

urlpatterns = [

	path('maifang/', views.liudong_note, name='liudong_note'),

]
