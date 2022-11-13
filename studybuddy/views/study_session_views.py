import datetime
from django.utils import timezone
from django.shortcuts import render
from studybuddy.models import Room, StudySession, User


def schedule(request, roomNumber):
    if request.user.is_anonymous:
        return render(request, template_name="index.html")

    template_name = "schedule_sessions/schedule.html"

    if Room.objects.filter(pk=roomNumber):
        room = Room.objects.get(pk=roomNumber)

        context = {
            'room': room,
            'student': User.objects.get(email=request.user.email),
        }
    else:
        context = {
            'noRoom': roomNumber,
            'student': User.objects.get(email=request.user.email),
        }

    return render(request, template_name, context)


def upcomingSessions(request):
    if request.user.is_anonymous:
        return render(request, template_name="index.html")

    template_name = "schedule_sessions/upcomingSessions.html"
    if request.POST.get('accept'):
        acceptSession(request)
    elif request.POST.get('decline'):
        declineSession(request)
    elif request.POST.get('delete'):
        deleteSession(request)
    elif request.POST.get('schedule'):
        # all values mst exist for form to be submitted. No need to check validity
        date = request.POST.get('date')
        start = request.POST.get('start')
        end = request.POST.get('end')
        room_pk = request.POST.get('room_pk')

        room = Room.objects.get(pk=room_pk)

        # if not StudySession.objects.filter(date=date, start=start, end=end, name=room.name).exists():
        session = StudySession.objects.create(date=date,
                                                  start=start,
                                                  end=end,
                                                  name=room.name,
                                                  post=room.post)
        for user in room.users.all():
            session.users.add(user)

    user_sessions = StudySession.objects.filter(users=User.objects.get(email=request.user.email))

    for session in StudySession.objects.all():
        print(session.users)
    print(user_sessions)

    context = {
        'study_sessions': user_sessions.filter(accepted='yes'),
        'pending_sessions': user_sessions.filter(accepted='?'),
        'declined_sessions': user_sessions.filter(accepted='no'),
        'student': User.objects.get(email=request.user.email),
    }

    return render(request, template_name, context)


def deleteSession(request):
    '''
    delete a study sessions
    '''
    email = request.user.email
    target_session_pk = request.POST['session_pk']
    # There shouldn't be a case where this called and post_pk doesn't exist because this is
    # method and not a url call. Putting in guards just in case
    # update after getting room association
    # if StudySession.objects.filter(user=User.objects.get(email=email), pk=target_session_pk).exists():
    if StudySession.objects.filter(pk=target_session_pk).exists():
        # StudySession.objects.get(user=User.objects.get(email=email), pk=target_session_pk).delete()
        StudySession.objects.get(pk=target_session_pk).delete()


def acceptSession(request):
    '''
    when a user schedules ones, the other user in the chat room should be able to choose accept or decline
    '''
    email = request.user.email
    target_session_pk = request.POST['session_pk']
    # update after getting room association
    # if StudySession.objects.filter(user=User.objects.get(email=email), pk=target_session_pk).exists():
    if StudySession.objects.filter(pk=target_session_pk).exists():
        # StudySession.objects.get(user=User.objects.get(email=email), pk=target_session_pk).delete()
        StudySession.objects.filter(pk=target_session_pk).update(accepted='yes')


def declineSession(request):
    email = request.user.email
    target_session_pk = request.POST['session_pk']
    if StudySession.objects.filter(pk=target_session_pk).exists():
        session = StudySession.objects.filter(pk=target_session_pk)
        session.update(accepted='no')
        session.update(date=(timezone.now() + datetime.timedelta(days=1)))
