from django.http import HttpResponse
from django.shortcuts import render

from .models import User

def index(request):
    return render(request, 'studybuddy/home.html')




def account(request):

    return render(request, 'studybuddy/Account.html')

def EditAccount(request):

    return HttpResponse("Edit account details")


