from django.urls import path
from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView
from studybuddy.views import views, post_views

app_name = 'studybuddy'
urlpatterns = [
    path('', views.index, name='index'),
    # implementing friends
    path('send_friend_request/<str:requestee_email>/', views.send_friend_request, name='send friend request'),
    path('accept_friend_request/<str:requester_email>/', views.accept_friend_request, name='accept friend request'),

    path('account/', views.account, name='account'),
    path('account/add/', views.addAccount, name='addAccount'),
    path('account/edit/', views.EditAccount, name='editAccount'),
    path('account/update/', views.UpdateAccount, name='updateAccount'),

    path('alldepartments/', views.alldepartments.as_view(), name='alldepartments'),
    path('chat/', views.chat, name='chat'),
    path('chat/rooms/', views.rooms, name='rooms'),
    path('chat/rooms/<slug:slug>/', views.room, name='room'),
    path('<str:dept>/', views.department, name='department'),
    path('<str:dept>/<int:course_number>/', views.coursefeed, name ='coursefeed'),

    path('<str:dept>/<int:course_number>/makepost', post_views.makepost, name ='makepost'),
    path('<str:dept>/<int:course_number>/submitpost', post_views.submitpost, name ='submitpost'),
    path('viewpost', post_views.viewposts, name='viewposts'),  # we need to fix this after updating email

    path('<str:dept>/<int:course_number>/enroll', views.enrollcourse, name = 'enroll'),
    path('<str:dept>/<int:course_number>/updatecourseload', views.updatecourseload, name = 'ucl'),
    #path('<str:email>/<str:dept>/<int:course_number>/disenroll', views.enrollcourse, name = 'disenroll'),
]