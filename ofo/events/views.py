from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from django.template import loader
from django.contrib.auth.models import User
from .forms import NewEventForm
from .models import Event, STATUS_OPEN, Status
from django.contrib.auth.models import User



@login_required(login_url='login/login/')
def new_event(request):
    # if not request.user.is_authenticated:
    #    return redirect('%s?next=%s' % ('/login/login', request.path))

    if request.method == 'POST':
        form = NewEventForm(request.POST)

        if form.is_valid():
            title = form.cleaned_data['title']
            place = form.cleaned_data['place']
            duration = form.cleaned_data['duration']
            date = form.cleaned_data['date']
            time = form.cleaned_data['time']
            status = Status.objects.get(status=STATUS_OPEN)
            organisator = User.objects.get(username=request.user.username)
            event = Event.objects.create(title=title, organisator=organisator, status=status, date=date, time=time, duration=duration, place=place)
            for key, value in request.POST.items():
                if key.startswith('guest-'):
                    new_user = value
                    try:
                        new_user = User.objects.get(username=value)
                        event.guests.add(new_user)
                        event.save()
                    except User.DoesNotExist:
                        continue

    else:
        form = NewEventForm()

    context = {'form': form}
    template = loader.get_template('events/new_event.html')
    return HttpResponse(template.render(context, request))
    # return render(request, 'events/new_event.html', context)


def user_search(request):
    url_parameter = request.GET.get('q')
    if url_parameter:
        if request.is_ajax() or True:
            users = User.objects.filter(username__startswith=url_parameter)
            if len(users) > 5:
                users = users[0:5]
            html = loader.render_to_string(template_name='events/search_result_partial.html', context={'users': users})
            data_return = {'html': html}
            return JsonResponse(data=data_return)
    data_return = {'html': ''}
    return JsonResponse(data=data_return)
