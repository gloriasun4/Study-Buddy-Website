import datetime
from django.urls import reverse
from django.utils import timezone
from django.shortcuts import render
from django.http import HttpResponseRedirect
from studybuddy.models import Post, Course, User

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

    # If user chooses to not provide values, then the default values will be used
    if(start_date == ""):
        start_date = Post._meta.get_field('startDate').get_default()

    if (end_date == ""):
        end_date = Post._meta.get_field('endDate').get_default()

    if(topic == ""):
        topic = Post._meta.get_field('topic').get_default()

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
                       endDate=end_date)
        newPost.save()
    else:
        for course in Course.objects.filter(subject=course.subject, catalog_number=course.catalog_number):
            newPost = Post(course=course,
                           user = User.objects.get(email=email),
                           # right now if User.objects doesn't have a name it will be empty, so this will ensure we have name?
                           author=str(request.user),
                           topic=topic,
                           startDate=start_date,
                           endDate=end_date)
            newPost.save()

    return HttpResponseRedirect(reverse('studybuddy:coursefeed', args=(email, dept, course_number)))

def deletepost(request, email):
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
        return HttpResponseRedirect(reverse('studybuddy:viewposts', args=(email,)))

def viewposts(request, email):
    if request.user.is_anonymous:
        return render(request, template_name="index.html")

    if request.POST.get('delete'):
        deletepost(request, email)

    template_name = ('post/viewposts.html')
    email = request.user.email
    user_posts = Post.objects.filter(user=User.objects.get(email=email)).distinct()

    # Make use of enrolled model to display posts

    return render(request, template_name, {'user_posts' : user_posts})