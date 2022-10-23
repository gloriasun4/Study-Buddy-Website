from django.urls import path
from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView
from . import views
app_name = 'studybuddy'
urlpatterns = [

    path('', views.index, name='index'),
    #path('', TemplateView.as_view(template_name="index.html")),
    path('account/', views.account, name='account'),
    path('account/edit/', views.EditAccount, name='editAccount'),
]