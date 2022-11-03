from django.urls import path
from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView
from studybuddy.views import views, post_views

app_name = 'studybuddy'
urlpatterns = [
    path('<str:email>/', views.index.as_view(), name='index'),
    path('<str:email>/account/', views.account, name='account'),
    path('<str:email>/account/add/', views.addAccount, name='addAccount'),
    path('<str:email>/account/edit/', views.EditAccount, name='editAccount'),
    path('<str:email>/account/update/', views.UpdateAccount, name='updateAccount'),
    path('<str:email>/alldepartments/', views.alldepartments.as_view(), name='alldepartments'),
    path('<str:email>/<str:dept>/', views.department, name='department'),
    path('<str:email>/<str:dept>/<int:course_number>/', views.coursefeed, name ='coursefeed'),
    path('<str:email>/<str:dept>/<int:course_number>/makepost', post_views.makepost, name ='makepost'),
    path('<str:email>/<str:dept>/<int:course_number>/submitpost', post_views.submitpost, name ='submitpost'),
    path('<str:email>/viewpost', post_views.viewposts, name='viewposts'), #we can probably change this to be my courses?
]