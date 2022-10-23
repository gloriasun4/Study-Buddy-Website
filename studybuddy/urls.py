from django.urls import path
from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView
from . import views
app_name = 'studybuddy'
urlpatterns = [

    path('<str:email>/', views.index, name='index'),
    #path('', TemplateView.as_view(template_name="index.html")),
    path('<str:email>/account/', views.account, name='account'),
    path('<str:email>/account/add/', views.addAccount, name='addAccount'),
    path('<str:email>/account/edit/', views.EditAccount, name='editAccount'),
]