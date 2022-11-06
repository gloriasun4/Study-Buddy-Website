import datetime
from django.urls import reverse
from django.utils import timezone
from django.shortcuts import render
from django.http import HttpResponseRedirect
from studybuddy.models import Post, Course, User, EnrolledClass

def makepost(request, email, dept, course_number):
    if request.user.is_anonymous:
        return render(request, template_name="index.html")

    template_name = ('post/makepost.html')

    if Course.objects.filter(course_number=course_number, subject=dept.upper()).exists():
        context = {
            'email' : email,
            'dept' : dept,
            'course': Course.objects.get(course_number=course_number),
            'valid' : 'true'
        }
    else:
        context = {
            'email' : email,
            'dept' : dept.upper(),
            'course': course_number
        }

    return render(request, template_name, context)

def submitpost(request, email, dept, course_number):
    if request.user.is_anonymous:
        return render(request, template_name="index.html")

    # if the course exists
    if Course.objects.filter(course_number=course_number, subject=dept.upper()).exists():
        course = Course.objects.get(course_number=course_number)
    # else go back into course feed and let user know the course is not valid
    else:
        return HttpResponseRedirect(reverse('studybuddy:coursefeed', args=(email, dept, course_number)))
    start_date = request.POST['start_date']
    end_date = request.POST['end_date']
    topic = request.POST['topic']
    description = request.POST['description']

    # If user chooses to not provide values, then the default values will be used
    if(start_date == ""):
        start_date = Post._meta.get_field('startDate').get_default()

    if (end_date == ""):
        end_date = Post._meta.get_field('endDate').get_default()

    if(topic == ""):
        topic = Post._meta.get_field('topic').get_default()

    if description == "":
        description = Post._meta.get_field('description').get_default()

    print(request.POST)

    # Get if user wants post to be in specific section or all sections of catalog_number
    # Default: post to only this specific section
    if request.POST['post_type'] == 'section':
        newPost = Post(course=course,
                       user = User.objects.get(email=email),
                       #right now if User.objects doesn't have a name it will be empty, so this will ensure we have name?
                       author= str(request.user),
                       topic=topic,
                       startDate=start_date,
                       endDate=end_date,
                       description=description,
                       post_type='section')
        newPost.save()
    else:
        newPost = Post(course=course,
                       user = User.objects.get(email=email),
                           # right now if User.objects doesn't have a name it will be empty, so this will ensure we have name?
                           author=str(request.user),
                           topic=topic,
                           startDate=start_date,
                           endDate=end_date,
                           description=description,
                           post_type='course')
        newPost.save()

    return HttpResponseRedirect(reverse('studybuddy:coursefeed', args=(email, dept, course_number)))

def deletepost(request):
    if request.user.is_anonymous:
        return render(request, template_name="index.html")

    email = request.user.email
    target_post_pk = request.POST['post_pk']
    for post in Post.objects.filter(user=User.objects.get(email=email)):
        dept = post.course.subject
        course_number = post.course.course_number
        if str(post.pk) == target_post_pk:
            post.delete()

    request_source = request.POST['delete_source']

    if(request_source == 'course_feed'):
        return HttpResponseRedirect(reverse('studybuddy:coursefeed', args=(email, dept, course_number,)))
    # default return to myposts
    else:
        return HttpResponseRedirect(reverse('studybuddy:viewposts'))

def viewposts(request):
    if request.user.is_anonymous:
        return render(request, template_name="index.html")

    if request.POST.get('delete'):
        deletepost(request)

    email = request.user.email
    template_name = 'post/viewposts.html'
    user_posts = Post.objects.filter(user=User.objects.get(email=email)).distinct()
    enrolled_courses = EnrolledClass.objects.filter(student = User.objects.get(email=email))
    unenrolled_posts_pk = []

    for post in user_posts:
        print(enrolled_courses.filter(course=post.course).exists())
        if not enrolled_courses.filter(course=post.course).exists():
            # if the student is enrolled in the class remove it from unenrolled list
            unenrolled_posts_pk.append(post.pk)

    unenrolled_posts=None
    for pk in unenrolled_posts_pk:
        if unenrolled_posts is None:
            unenrolled_posts = Post.objects.filter(pk=pk)
        else:
            unenrolled_posts = unenrolled_posts | Post.objects.filter(pk=pk)

    if unenrolled_posts is None:
        context = {
            'user_posts': user_posts,
            'enrolled_courses' : enrolled_courses
        }
    else:
        print(unenrolled_posts)
        context = {
            'user_posts': user_posts,
            'enrolled_courses': enrolled_courses,
            'unenrolled_posts': unenrolled_posts
        }

    return render(request, template_name, context)