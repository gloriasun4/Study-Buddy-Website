import requests, json
from . import post_views
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from studybuddy.models import User, Departments, Course, Post, EnrolledClass, Room, Message, Friend_Request


def index(request):
    if request.user.is_anonymous or not User.objects.filter(email=request.user.email).exists():
        return render(request, template_name="index.html")
    else:
        template_name = 'homepage.html'

        context = {
            'student': User.objects.get(email=request.user.email),
        }

        return render(request, template_name, context)


def chat(request):
    if request.user.is_anonymous:
        return render(request, template_name="index.html")

    return render(request, 'studybuddy/chat.html')


def rooms(request):
    if request.user.is_anonymous:
        return render(request, template_name="index.html")

    rooms = Room.objects.all()

    return render(request, 'studybuddy/rooms.html', {'rooms': rooms})


def room(request, slug):
    if request.user.is_anonymous:
        return render(request, template_name="index.html")

    room = Room.objects.get(slug=slug)
    messages = Message.objects.filter(room=room)[0:25]

    context = {
        'room': room,
        'messages': messages,
        'username': User.objects.get(email=request.user.email).username
    }

    return render(request, 'studybuddy/room.html', context)


def addAccount(request):
    if request.user.is_anonymous:
        return render(request, template_name="index.html")

    email = request.user.email
    exist = User.objects.filter(email=email).exists()
    if not exist:
        newAcc = User(email=email, name=request.user.username)
        newAcc.save()

    return HttpResponseRedirect(reverse('studybuddy:index'))


def account(request):
    if request.user.is_anonymous:
        return render(request, template_name="index.html")

    email = request.user.email
    user = User.objects.get(email__exact=email)
    context = {
        'Email': user.email,
        'UserName': user.username,
        'Name': user.name,
        'Major': user.major,
        'ZoomLink': user.zoomLink,
        'AboutMe': user.blurb

    }
    return render(request, 'studybuddy/account.html', context)


def EditAccount(request):
    if request.user.is_anonymous:
        return render(request, template_name="index.html")

    email = request.user.email
    user = User.objects.get(email=email)
    context = {
        'Email': user.email,
        'UserName': user.username,
        'Name': user.name,
        'Major': user.major,
        'ZoomLink': user.zoomLink,
        'AboutMe': user.blurb

    }
    return render(request, 'studybuddy/editAccount.html', context)


def UpdateAccount(request):
    if request.user.is_anonymous:
        return render(request, template_name="index.html")

    email = request.user.email
    account = User.objects.get(email__exact=email)
    account.username = request.POST['username']
    account.name = request.POST['name']
    account.major = request.POST['major']
    account.zoomLink = request.POST['zlink']
    account.blurb = request.POST['blurb']

    account.save()

    return HttpResponseRedirect(reverse('studybuddy:account'))


class alldepartments(generic.ListView):
    model = Departments
    template_name = ('alldepartments.html')

    # Get the json for all the departments
    deptList = requests.get('http://luthers-list.herokuapp.com/api/deptlist/')
    deptList_json = json.loads(deptList.text)

    # makes sure there are no departments from previous calls
    if Departments.objects.exists():
        Departments.objects.all().delete()

    # Get all of the current departments available
    for i in range(len(deptList_json)):
        newDept = Departments(dept=deptList_json[i].get("subject"))
        newDept.save()

    def get_queryset(self):
        return Departments.objects.all()


def department(request, dept):
    if request.user.is_anonymous:
        return render(request, template_name="index.html")

    if dept == "viewpost":
        return post_views.viewposts(request)

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
        if not Course.objects.filter(subject=dept,
                                     catalog_number=current_class.get('catalog_number'),
                                     instructor=current_class.get('instructor').get('name'),
                                     section=current_class.get('course_section'),
                                     course_number=current_class.get('course_number'),
                                     description=current_class.get('description')).exists():
            newClass = Course(subject=dept,
                              catalog_number=current_class.get('catalog_number'),
                              instructor=current_class.get('instructor').get('name'),
                              section=current_class.get('course_section'),
                              course_number=current_class.get('course_number'),
                              description=current_class.get('description'))
            newClass.save()

    return render(request, template_name, {'department_list': Course.objects.filter(subject=dept), 'dept': dept})


def coursefeed(request, dept, course_number):
    template_name = 'course_feed.html'

    if request.user.is_anonymous:
        return render(request, template_name="index.html")

    if request.POST.get('delete'):
        post_views.deletepost(request)

    if request.POST.get('submit'):
        post_views.submitpost(request, dept, course_number)

    if Course.objects.filter(course_number=course_number).exists() and Course.objects.filter(subject=dept):
        course = Course.objects.get(course_number=course_number)
        Post.objects.filter(endDate__lt=timezone.now()).delete()
        post_for_this_class = Post.objects.filter(
            course=course)  # this will find posts that are related to this specific section only

        for catalog_course in Course.objects.filter(subject=course.subject, catalog_number=course.catalog_number):
            post_for_this_class = post_for_this_class | Post.objects.filter(course=catalog_course, post_type='course')

        context = {
            'dept': dept.upper(),
            'course': course,
            'valid': 'true',
            'feed_posts': post_for_this_class,
            'has_posts': post_for_this_class.exists()
        }
    else:
        context = {
            'dept': dept.upper(),
            'course': course_number,
        }

    return render(request, template_name, context)


def enrollcourse(request, dept, course_number):
    if request.user.is_anonymous:
        return render(request, template_name="index.html")

    template_name = 'enroll.html'

    if (Course.objects.filter(course_number=course_number).exists()):
        context = {
            'dept': dept.upper(),
            'course': Course.objects.get(course_number=course_number),
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


def updatecourseload(request, dept, course_number):
    if request.user.is_anonymous:
        return render(request, template_name="index.html")

    email = request.user.email
    account = User.objects.get(email__exact=email)
    course = Course.objects.get(course_number=course_number)

    action = request.POST['choice']
    if action == "YesD":
        EnrolledClass.objects.filter(course=course, student=account).delete()
    elif action == "YesE":
        enrolled = EnrolledClass(course=course, student=account)
        enrolled.save()

    return HttpResponseRedirect(reverse('studybuddy:index'))


# implementing friends
@login_required
def send_friend_request(request, requestee_email):
    '''
    return 0: friend request was already sent and is pending approval
           1: friend request was created and sent
    '''

    # This method is called after already processing to and from users are valid
    from_user = User.objects.get(email__exact=request.user.email)
    to_user = User.objects.get(email__exact=requestee_email)

    friend_request, created = Friend_Request.objects.get_or_create(from_user=from_user, to_user=to_user)
    if created:
        return 1
    else:
        return 0


@login_required
def accept_friend_request(request, requester_email):
    from_user = User.objects.get(email=requester_email)
    to_user = User.objects.get(email=request.user.email)

    friend_request_query_set = Friend_Request.objects.filter(from_user=from_user).filter(to_user=to_user)
    friend_request = friend_request_query_set.first()

    friend_request.to_user.friends.add(friend_request.from_user)
    print(friend_request.to_user.friends.all())
    friend_request.from_user.friends.add(friend_request.to_user)
    print(friend_request.from_user.friends.all())
    friend_request.delete()


def remove_friend(request, email):
    User.objects.get(email=request.user.email).friends.remove(User.objects.get(email=email))


def decline_request(request, email):
    from_user = User.objects.get(email=email)
    to_user = User.objects.get(email=request.user.email)

    Friend_Request.objects.filter(from_user=from_user).filter(to_user=to_user).delete()


def view_friends(request):
    if request.user.is_anonymous:
        return render(request, template_name="index.html")

    from_user = User.objects.get(email=request.user.email)
    # get the friend requests that are sent to the current user
    friend_request = Friend_Request.objects.filter(to_user = from_user)
    sent_requests = Friend_Request.objects.filter(from_user = from_user)
    friends = from_user.friends.all()

    context = {
        'friends': friends,
        'friend_requests': friend_request,
        'sent_requests' : sent_requests,
        # add declined?
    }

    # if the user sent a friend request
    if request.POST.get('request'):
        requestee_email = request.POST.get('email')
        context['toEmail'] = requestee_email
        # make sure the user isn't trying to add themselves
        if requestee_email == request.user.email:
            context['self'] = True
        # check that the requested friend is in our system
        elif User.objects.filter(email__exact=requestee_email).exists():
            # send the request (adds to friend_request model)
            send = send_friend_request(request, requestee_email)

            # if returned 1, means the friend request was created
            if send == 1:
                context['sent'] = True
            # else it returned a 0 meaning the friend request was already pending
            else:
                context['alreadySent'] = True

        # if the user isn't in our system let the user know
        else:
            context['notValid'] = True

    # user accepted a friend request
    if request.POST.get('accept'):
        ad_email = request.POST.get('ad_email')
        accept_friend_request(request, ad_email)
        context['accepted'] = True
        context['accepted_email'] = ad_email

    if request.POST.get('decline'):
        ad_email = request.POST.get('ad_email')
        decline_request(request, ad_email)
        context['declined'] = True
        context['declined_email'] = ad_email

    if request.POST.get('unfriend'):
        remove_email = request.POST.get('remove_email')
        remove_friend(request, remove_email)
        context['remove_friend'] = True
        context['removed_email'] = remove_email

    return render(request, "friends/view_friends.html", context)

# def disenrollcourse(reques, dept, course_number):
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
