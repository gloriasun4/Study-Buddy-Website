import requests, json
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.shortcuts import render
from django.contrib import messages
from . import post_views
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from studybuddy.models import User, Departments, Course, Post, EnrolledClass, Room, Message, Friend_Request

# class index(generic.TemplateView):
#     template_name = 'homepage.html'

def index(request, email):
    if request.user.is_anonymous or not User.objects.filter(email=request.user.email).exists():
        return render(request, template_name="index.html")
    else:
        template_name = 'homepage.html'

        context = {
                'student': User.objects.get(email=request.user.email),
        }

        return render(request, template_name, context)

def chat(request, email):
    return render(request, 'studybuddy/chat.html')

def rooms(request, email):
    rooms = Room.objects.all()

    return render(request, 'studybuddy/rooms.html', {'rooms': rooms})

def room(request, email, slug):
    room = Room.objects.get(slug=slug)
    messages = Message.objects.filter(room=room)[0:25]

    return render(request, 'studybuddy/room.html', {'room': room, 'messages': messages})

def addAccount(request, email):
    if request.user.is_anonymous:
        return render(request, template_name="index.html")

    exist = User.objects.filter(email=email).exists()
    if not exist:
        newAcc = User(email=email, firstName=request.user.username)
        newAcc.save()

    return HttpResponseRedirect(reverse('studybuddy:index', args=(email,)))

def account(request, email):
    if request.user.is_anonymous:
        return render(request, template_name="index.html")

    user = User.objects.get(email__exact=email)
    context = {
        'Email': user.email,
        # 'FirstName': user.firstName,
        # 'LastName': user.lastName,
        'UserName': user.username,
        'Name': user.name,
        'Major': user.major,
        'ZoomLink': user.zoomLink,
        'AboutMe': user.blurb

    }
    return render(request, 'studybuddy/account.html', context)

def EditAccount(request, email):
    if request.user.is_anonymous:
        return render(request, template_name="index.html")

    user = User.objects.get(email=email)
    context = {
        'Email': user.email,
        # 'FirstName': user.firstName,
        # 'LastName': user.lastName,
        'UserName': user.username,
        'Name': user.name,
        'Major': user.major,
        'ZoomLink': user.zoomLink,
        'AboutMe': user.blurb

    }
    return render(request, 'studybuddy/editAccount.html', context)

def UpdateAccount(request, email):
    if request.user.is_anonymous:
        return render(request, template_name="index.html")

    account = User.objects.get(email__exact=email)
    # account.firstName=request.POST['fname']
    # account.lastName=request.POST['lname']
    account.username=request.POST['username']
    account.name=request.POST['name']
    account.major=request.POST['major']
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

def department(request, email, dept):
    if request.user.is_anonymous:
        return render(request, template_name="index.html")

    model = Course
    template_name = ('department.html')

    # Get the json file for the request department
    dept = dept.upper()
    dept_request = "http://luthers-list.herokuapp.com/api/dept/" + dept
    dept_classes = requests.get(dept_request)
    dept_classes_json = json.loads(dept_classes.text)

    # Get all of the classes in the requested department
    for i in range(len(dept_classes_json)):
        current_class = dept_classes_json[i]

        # if the course doesn't exists then we will add it
        if not Course.objects.filter(subject = dept,
                          catalog_number = current_class.get('catalog_number'),
                          instructor = current_class.get('instructor').get('name'),
                          section = current_class.get('course_section'),
                          course_number = current_class.get('course_number'),
                          description = current_class.get('description')).exists():

            newClass = Course(subject=dept,
                              catalog_number=current_class.get('catalog_number'),
                              instructor=current_class.get('instructor').get('name'),
                              section=current_class.get('course_section'),
                              course_number=current_class.get('course_number'),
                              description = current_class.get('description'))
            newClass.save()

    return render(request, template_name, {'department_list' : Course.objects.filter(subject=dept), 'dept' : dept})

def coursefeed (request, email, dept, course_number):
    template_name = 'course_feed.html'

    if request.user.is_anonymous:
        return render(request, template_name="index.html")

    if request.POST.get('delete'):
        post_views.deletepost(request)

    '''
    filter through 2 things to find all posts:
    1. course_number=course_number (this will fidn section specific posts)
    2. sibject=subject, catalog_number=catalog_number, post_Type=course (this finds the course posts)
    3. combine the above 2 posts to display
    '''

    if Course.objects.filter(course_number = course_number).exists():
        course = Course.objects.get(course_number=course_number)
        Post.objects.filter(endDate__lt=timezone.now()).delete()
        post_for_this_class = Post.objects.filter(course=course) #this will find posts that are related to this specific section only

        for catalog_course in Course.objects.filter(subject=course.subject, catalog_number=course.catalog_number):
            post_for_this_class = post_for_this_class | Post.objects.filter(course=catalog_course, post_type='course')

        context = {
            'dept' : dept.upper(),
            'course' : course,
            'valid' : 'true',
            'feed_posts' : post_for_this_class,
            'has_posts' : post_for_this_class.exists()
        }
    else:
        context = {
            'dept': dept.upper(),
            'course': course_number,
        }

    return render(request, template_name, context)

def enrollcourse (request, email, dept, course_number):
    if request.user.is_anonymous:
        return render(request, template_name="index.html")

    template_name = 'enroll.html'

    # print(Departments.objects.filter(dept))
    if(Course.objects.filter(course_number = course_number).exists()):
        context = {
            'dept': dept.upper(),
            'course': Course.objects.get(course_number = course_number),
            'valid': 'true',
            'enrolled': EnrolledClass.objects.filter(course=Course.objects.get(course_number=course_number),
                                                     student=User.objects.get(email=request.user.email)).exists()
        }
    else:
        context = {
            'dept': dept.upper(),
            'course': course_number,
        }

    return render(request, template_name, context)

def updatecourseload(request, email, dept, course_number):
    if request.user.is_anonymous:
        return render(request, template_name="index.html")

    account = User.objects.get(email__exact=email)
    course = Course.objects.get(course_number=course_number)

    action = request.POST['choice']
    if action=="YesD":
        EnrolledClass.objects.filter(course=course, student=account).delete()
    elif action == "YesE":
        enrolled = EnrolledClass(course=course, student=account)
        enrolled.save()



    return HttpResponseRedirect(reverse('studybuddy:index', args=(email,)))

# implementing friends
@login_required
def send_friend_request(request, email, requestee_email):
    from_user = User.objects.get(email__exact=email)
    #print(requestee_email)
    #print(User.objects.all())

    if (User.objects.filter(email__exact=requestee_email).exists()):
        to_user = User.objects.filter(email__exact=requestee_email).exists()
        if (from_user.email == str(request.user.email)):
            friend_request, created = Friend_Request.objects.get_or_create(from_user=from_user, to_user=to_user)
            if created:
                return HttpResponse("friend request sent")
            else:
                return HttpResponse("friend request was already sent")
        else:
            return HttpResponse('Invalid')
    else:
        return HttpResponse("This user, " +  requestee_email + " does not exist")

    
    

@login_required
def accept_friend_request(request, email, requester_email):
    if request.user.is_anonymous:
        return render(request, template_name="index.html")

    from_user = User.objects.get(email=requester_email)
    to_user = User.objects.get(email=email)
    #print("to_user.username: " + to_user.username)
    #print("request.user: " + str(request.user))
    if (Friend_Request.objects.filter(from_user = from_user).count() == 0):
        return HttpResponse("You have no pending requests from " + requester_email)
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

# def disenrollcourse(request, email, dept, course_number):
#     template_name = 'disenroll.html'
#
#     # print(Departments.objects.filter(dept))
#     if (Course.objects.filter(course_number=course_number).exists()):
#         context = {
#             'dept': dept.upper(),
#             'course': Course.objects.get(course_number=course_number),
#             'valid': 'true',
#
#         }
#     else:
#         context = {
#             'dept': dept.upper(),
#             'course': course_number,
#         }
#
#     return render(request, template_name, context)