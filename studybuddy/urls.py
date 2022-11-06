from django.urls import path
from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView
from . import views
app_name = 'studybuddy'
urlpatterns = [
    path('<str:email>/', views.index.as_view(), name='index'),
    path('<str:email>/account/', views.account, name='account'),
    path('<str:email>/account/add/', views.addAccount, name='addAccount'),
    path('<str:email>/account/edit/', views.EditAccount, name='editAccount'),
    path('<str:email>/account/update/', views.UpdateAccount, name='updateAccount'),
    path('<str:email>/alldepartments/', views.alldepartments.as_view(), name='alldepartments'),
    path('<str:email>/chat/', views.chat, name='chat'),
    path('<str:email>/chat/rooms/', views.rooms, name='rooms'),
    path('<str:email>/chat/rooms/<slug:slug>/', views.room, name='room'),
    path('<str:email>/<str:dept>/', views.department, name='department'),
    path('<str:email>/<str:dept>/<int:course_number>/', views.coursefeed, name = 'coursefeed'),
    path("<str:email>/<str:dept>/<int:course_number>/makepost", views.makepost, name = 'makepost'),
]