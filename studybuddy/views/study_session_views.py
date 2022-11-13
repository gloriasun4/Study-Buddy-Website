import datetime
from django.utils import timezone
from django.shortcuts import render
from studybuddy.models import Room, StudySession


def schedule(request, roomname):
    if request.user.is_anonymous:
        return render(request, template_name="index.html")

    template_name = "schedule_sessions/schedule.html"

    if Room.objects.filter(slug=roomname):
        room = Room.objects.get(slug=roomname)

        context = {
            'room': room
        }
    else:
        context = {
            'noRoom': roomname
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
        roomName = request.POST.get('roomName')

        if not StudySession.objects.filter(date=date, start=start, end=end, name=roomName).exists():
            StudySession.objects.create(date=date, start=start, end=end, name=roomName)

    context = {
        'study_sessions': StudySession.objects.filter(accepted='yes'),
        'pending_sessions': StudySession.objects.filter(accepted='?'),
        'declined_sessions' : StudySession.objects.filter(accepted='no')
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