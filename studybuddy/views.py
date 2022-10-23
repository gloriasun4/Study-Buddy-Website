

from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from .models import User

def index(request, email):

   return render(request, 'studybuddy/home.html')

def addAccount(request, email):
    exist = User.objects.filter(email=email).exists()
    if not exist:
        newAcc = User(email=email)
        newAcc.save()

    return HttpResponseRedirect(reverse('studybuddy:account', args=(email,)))


def account(request, email):
    user = User.objects.get(email=email)
    context = {
        'Email': user.email,
        'FirstName': user.firstName,
        'LastName': user.lastName,
        'ZoomLink': user.zoomLink,
        'AboutMe': user.blurb

    }
    return render(request, 'studybuddy/account.html', context)

def EditAccount(request, email):

    return HttpResponse("Edit account details")


