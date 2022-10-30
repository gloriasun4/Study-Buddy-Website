from django.views import generic
from .models import Departments, Course
import requests
import json
from .forms import SnippetForm
from .models import Snippet
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from .models import User

class index(generic.TemplateView):
    template_name = 'homepage.html'
    # return HttpResponse("Welcome to the Study Buddy App!")

# def index(request, email):
#
#    return render(request, 'studybuddy/home.html')

def addAccount(request, email):
    exist = User.objects.filter(email=email).exists()
    if not exist:
        newAcc = User(email=email)
        newAcc.save()

    return HttpResponseRedirect(reverse('studybuddy:account', args=(email,)))

def makepost(request, email, dept, course_number):
    form = SnippetForm(request.POST or None, request.FILES or None)
    if request.method == 'POST':

        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user;
            obj.save()
            form = SnippetForm()
            messages.success(request, "Successfully created")

    return render(request, 'form.html', {'form': form})

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
    user = User.objects.get(email=email)
    context = {
        'Email': user.email,
        'FirstName': user.firstName,
        'LastName': user.lastName,
        'ZoomLink': user.zoomLink,
        'AboutMe': user.blurb

    }
    return render(request, 'studybuddy/EditAccount.html', context)

def UpdateAccount(request, email):
    account = User.objects.get(email=email)

    account.firstName=request.POST['fname']
    account.lastName=request.POST['lname']
    account.zoomLink = request.POST['zlink']
    account.blurb = request.POST['blurb']

    account.save()

    return HttpResponseRedirect(reverse('studybuddy:account', args=(email,)))

class alldepartments(generic.ListView):
    model = Departments
    template_name = ('alldepartments.html')

    # Get the json for all the departments
    deptList = requests.get('http://luthers-list.herokuapp.com/api/deptlist/')
    deptList_json = json.loads(deptList.text)

    # makes sure there are no departments from previous calls
    if(Departments.objects.exists()):
        Departments.objects.all().delete()

    # Get all of the current departments available
    for i in range(len(deptList_json)):
        newDept = Departments(dept = deptList_json[i].get("subject"))
        newDept.save()

    def get_queryset(self):
        return Departments.objects.all()

    # return HttpResponse("here are the departments")

def department(request, email, dept):
    model = Course
    template_name = ('department.html')

    # Get the json file for the request department
    dept = dept.upper()
    dept_request = "http://luthers-list.herokuapp.com/api/dept/" + dept
    dept_classes = requests.get(dept_request)
    dept_classes_json = json.loads(dept_classes.text)

    #
    if (Course.objects.exists()):
        Course.objects.all().delete()

    # Get all of the classes in the requested department
    for i in range(len(dept_classes_json)):
        current_class = dept_classes_json[i]
        newClass = Course(subject = dept,
                          catalog_number = current_class.get('catalog_number'),
                          instructor = current_class.get('instructor').get('name'),
                          section = current_class.get('course_section'),
                          course_number = current_class.get('course_number'))

        # print(newClass)
        newClass.save()

    return render(request, template_name, {'department_list' : Course.objects.all(), 'dept' : dept})
    # return HttpResponse(dept_classes_json)

    # return HttpResponse("choose the class you want to find a study buddy in")

def coursefeed (request, email, dept, course_number):
    template_name = 'course_feed.html'

    # print(Departments.objects.filter(dept))
    if(Course.objects.filter(course_number = course_number).exists()):
        context = {
            'dept' : dept.upper(),
            'course' : Course.objects.get(course_number = course_number),
            'valid' : 'true'
        }
    else:
        context = {
            'dept': dept.upper(),
            'course': course_number,
        }

    return render(request, template_name, context)