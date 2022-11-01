from studybuddy.views import views
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render

def index(request):
    template_name = 'index.html'

    if(request.user.is_anonymous):
        return render(request, template_name)
    else:
        email = request.user.email
        views.addAccount(request, email)

        return HttpResponseRedirect(reverse('studybuddy:index', args=(email,)))

def handler404(request, *args, **argv):
    response = render_to_response('index.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 404
    return response