from django.urls import path
from studybuddy.views import views, post_views, study_session_views, friend_views

app_name = 'studybuddy'
urlpatterns = [
    path('', views.index, name='index'),
    # implementing friends
    path('friends', friend_views.view_friends, name='viewFriends'),

    path('account/', views.account, name='account'),
    path('account/add/', views.addAccount, name='addAccount'),
    path('account/edit/', views.EditAccount, name='editAccount'),
    path('account/update/', views.UpdateAccount, name='updateAccount'),

    path('alldepartments/', views.alldepartments.as_view(), name='alldepartments'),
    path('chat/', views.chat, name='chat'),
    path('chat/rooms/', views.rooms, name='rooms'),
    path('chat/rooms/<str:slug>/', views.room, name='room'),
    path('<str:dept>/', views.department, name='department'),
    path('<str:dept>/<int:course_number>/', views.coursefeed, name ='coursefeed'),

    path('<str:dept>/<int:course_number>/makepost', post_views.makepost, name ='makepost'),
    path('viewpost', post_views.viewposts, name='viewposts'),

    path('<str:dept>/<int:course_number>/enroll', views.enrollcourse, name = 'enroll'),
    path('<str:dept>/<int:course_number>/updatecourseload', views.updatecourseload, name = 'ucl'),
    #path('<str:email>/<str:dept>/<int:course_number>/disenroll', views.enrollcourse, name = 'disenroll'),

    path('<str:roomname>/schedule', study_session_views.schedule, name='schedule'),
    path('upcomingSessions', study_session_views.upcomingSessions, name='upcomingSessions'),
]