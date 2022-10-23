from django.urls import path

from . import views

app_name = 'studybuddy'

urlpatterns = [
    path('', views.index.as_view(), name='index'),
    # path('alldepartments/', views.alldepartments.as_view(), name='alldepartments'),
    # path('<str:dept>/', views.department, name='department'),
    # path('<str:dept>/<int:course_number>/', views.coursefeed, name = 'coursefeed'),
    # path("<str:dept>/<int:course_number>/makepost", views.makepost, name = 'makepost'),
]