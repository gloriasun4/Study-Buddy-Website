from django.http import HttpResponse
from django.shortcuts import render

from .models import User

def index(request):
    return HttpResponse("Welcome to the Study Buddy App!")




def account(request):

    return HttpResponse("Hey welcome to account page you are logged in as {{ user.username }}" )

