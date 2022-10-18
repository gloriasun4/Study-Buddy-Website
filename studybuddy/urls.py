from django.urls import path

from . import views
app_name = 'studybuddy'
urlpatterns = [
    path('', views.index, name='index'),
    path('account/', views.account, name='account'),
]