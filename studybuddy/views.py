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
from .models import User, Friend_Request
from django.contrib.auth.decorators import login_required

class index(generic.TemplateView):
    template_name = 'homepage.html'
    # return HttpResponse("Welcome to the Study Buddy App!")

# def index(request, email):
#
#    return render(request, 'studybuddy/home.html')

def addAccount(request, email):
    exist = User.objects.filter(email=email).exists()
    if not exist:
        newAcc = User(email=email, username=request.user)
        newAcc.save()

    return HttpResponseRedirect(reverse('studybuddy:index', args=(email,)))

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
    user = User.objects.get(email__exact=email)
    context = {
        'Email': user.email,
        'FirstName': user.firstName,
        'LastName': user.lastName,
        'ZoomLink': user.zoomLink,
        'AboutMe': user.blurb,
        # implementing friends
        'Friends': user.friends
    }
    return render(request, 'studybuddy/account.html', context)

def EditAccount(request, email):
    user = User.objects.get(email=email)
    context = {
        'Email': user.email,
        'FirstName': user.firstName,
        'LastName': user.lastName,
        'ZoomLink': user.zoomLink,
        'AboutMe': user.blurb,
        # implementing friends
        'Friends': user.friends,
        'Username': user.username
    }
    return render(request, 'studybuddy/editAccount.html', context)

def UpdateAccount(request, email):
    account = User.objects.get(email__exact=email)

    account.firstName=request.POST['fname']
    account.lastName=request.POST['lname']
    account.zoomLink = request.POST['zlink']
    account.blurb = request.POST['blurb']
    account.username = request.POST['uname']

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

# implementing friends
@login_required
def send_friend_request(request, email, requestee_email):
    from_user = User.objects.get(email__exact=email)
    #print(requestee_email)
    #print(User.objects.all())
    to_user = User.objects.get(email__exact=requestee_email)
    if (from_user.email == str(request.user.email)):
        friend_request, created = Friend_Request.objects.get_or_create(from_user=from_user, to_user=to_user)
        if created:
            return HttpResponse("friend request sent")
        else:
            return HttpResponse("friend request was already sent")
    else:
        return HttpResponse('Invalid')

@login_required
def accept_friend_request(request, email, requester_email):
    from_user = User.objects.get(email=requester_email)
    to_user = User.objects.get(email=email)
    #print("to_user.username: " + to_user.username)
    #print("request.user: " + str(request.user))
    if (to_user.email == str(request.user.email)):
        friend_request_query_set = Friend_Request.objects.filter(from_user=from_user).filter(to_user=to_user)
        friend_request = friend_request_query_set.first()
        friend_request.to_user.friends.add(friend_request.from_user)
        print(friend_request.to_user.friends.all())
        friend_request.from_user.friends.add(friend_request.to_user)
        print(friend_request.from_user.friends.all())
        friend_request.delete()
        return HttpResponse("friend request accepted")
    else:
        return HttpResponse('Invalid')