from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from studybuddy.models import Room, Message, User, Post

@csrf_exempt
def rooms(request):
    if request.user.is_anonymous:
        return render(request, template_name="index.html")

    context = {
        'rooms': Room.objects.filter(users=User.objects.get(email=request.user.email)),
        'student_name': User.objects.get(email=request.user.email).name,
    }

    if User.objects.get(email=request.user.email).name == "":
        context['student_name'] = request.user

    if request.GET.get('leave'):
        room_pk = request.GET['room_pk']
        if Room.objects.filter(pk=room_pk):
            room = Room.objects.get(pk=room_pk)
            if room.users.count() == 1:
                room.delete()
            else:
                room.users.remove(User.objects.get(email=request.user.email))

    return render(request, 'studybuddy/rooms.html', context)


def room(request, roomNumber):
    if request.user.is_anonymous:
        return render(request, template_name="index.html")

    room = Room.objects.get(pk=roomNumber)
    messages = Message.objects.filter(room=room)[0:25]

    context = {
        'room': room,
        'messages': messages,
        'username': User.objects.get(email=request.user.email).username,
        'student_name': User.objects.get(email=request.user.email).name,
    }

    if User.objects.get(email=request.user.email).name == "":
        context['student_name'] = request.user

    return render(request, 'studybuddy/room.html', context)


def addRoom(request):
    post_pk = request.POST['post_pk']
    post = Post.objects.get(pk=post_pk)
    # If there is no rooms current associated to this room, make a new room
    if not Room.objects.filter(post=post):
        # create a new object with the owner of the post
        Room.objects.create(post=post, name=post.topic)
        Room.objects.get(post=post).users.add(User.objects.get(email=post.user.email))
        # add the new user who wants to join to the room
    # add the new user into the room (this will happen after a new made room or just added to the already existing room)
    Room.objects.get(post=post).users.add(User.objects.get(email=request.user.email))

    # return room(request, roomNumber=Room.objects.get(post=post).pk)
    return Room.objects.get(post=post).pk
