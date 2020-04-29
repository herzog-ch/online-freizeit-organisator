from django.shortcuts import redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.template import loader
from django.contrib.auth.models import User
from django.core.mail import send_mail
from .forms import NewEventForm, ProposalForm, DetermineEventForm
from .models import Event, STATUS_OPEN, STATUS_DECIDED, Status, Proposal


@login_required(login_url='/login')  # login is required for showing the details of an event
def detail(request, event_id):
    """The view for showing details about a specific event.
    If the required event doesn't exist, the user is redirected to the "overview" view.
    """
    try:
        event = Event.objects.get(pk=event_id)
    except Event.DoesNotExist:
        return redirect('overview')

    # check if the logged in user is also the organisator of the event
    if event.organisator == request.user:
        is_organisator = True
    else:
        is_organisator = False

    # if the event is still open for proposals and the user is the organisator of the event,
    # show the DetermineEventForm for the organisator. Otherwise set the determine_event_form to "none"
    # If the form data for the DetermineEventForm is received and it is valid, then update the status, date, time,
    # place of the event and set it to "STATUS_DECIDED"
    if is_organisator and event.status.status == STATUS_OPEN:
        if request.method == 'POST':
            determine_event_form = DetermineEventForm(request.POST)
            if determine_event_form.is_valid():
                event.status = Status.objects.get(status=STATUS_DECIDED)
                event.date = determine_event_form.cleaned_data['date']
                event.time = determine_event_form.cleaned_data['time']
                event.place = determine_event_form.cleaned_data['place']
                event.comment = determine_event_form.cleaned_data['comment']
                event.save()
                event.refresh_from_db()
                determine_event_form = None
        else:
            determine_event_form = DetermineEventForm()
    else:
        determine_event_form = None

    # retrieve all proposals from other users for the event
    try:
        Proposal.objects.filter(event=event).get(author=request.user)
        user_did_proposal = True
    except Proposal.DoesNotExist:
        user_did_proposal = False

    # if the current user is invited to the event and didn't give a proposal yet, render the ProposalForm
    # If the form data is received, create a new proposal in the database.
    if not is_organisator and not user_did_proposal and event.status.status == STATUS_OPEN:
        if request.method == 'POST':
            proposal_form = ProposalForm(request.POST)
            if proposal_form.is_valid():
                new_proposal = Proposal.objects.create(event=event, date=proposal_form.cleaned_data['date'],
                                                       time=proposal_form.cleaned_data['time'],
                                                       place=proposal_form.cleaned_data['place'],
                                                       comment=proposal_form.cleaned_data['comment'],
                                                       author=request.user)
                user_did_proposal = True
                # message success
        else:
            proposal_form = ProposalForm()
    else:
        proposal_form = None

    # String to show for the status of the event
    status = 'Offen für Vorschläge' if event.status == Status.objects.get(status=STATUS_OPEN) else 'Termin festgelegt'

    proposals = Proposal.objects.filter(event=event)

    # all invited users
    guests = event.guests.all()

    # setup context for the "events/events_detail.html" template
    context = {'proposal_form': proposal_form, 'determine_event_form': determine_event_form,
               'is_organisator': is_organisator, 'user_did_proposal': user_did_proposal,
               'event': event, 'guests': guests, 'status': status, 'proposals': proposals,
               'is_open_for_proposals': event.status.status == STATUS_OPEN}
    template = loader.get_template('events/events_detail.html')
    return HttpResponse(template.render(context, request))


@login_required(login_url='/login')  # login is required for showing the events for the user
def overview(request):
    """
    The view for showing all the events that you are invited to and the events that you organised.
    Both event types are loaded from the db and then given to the context of the template events/events_overview.html
    """

    # load events invited
    events_invited = Event.objects.filter(guests=request.user)

    # load events organised by user
    events_organised = Event.objects.filter(organisator=request.user)

    context = {'events_invited': events_invited, 'events_organised': events_organised}
    template = loader.get_template('events/events_overview.html')
    return HttpResponse(template.render(context, request))


@login_required(login_url='/login')   # login is required for creating new events
def new_event(request):
    """
    The view for creating a new event.
    The NewEventForm form from forms.py is rendered here. If the form data is received via POST
    and is valid a new event is created.
    Also the invititation email is sent to recipient list here
    """

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
            event = Event.objects.create(title=title, organisator=organisator, status=status, date=date, time=time,
                                         duration=duration, place=place)
            recipient_list = []
            for key, value in request.POST.items():
                if key.startswith('guest-'):
                    # the "input hidden" field IDs for the guests start with "guest-" and have the username as the
                    # value. This can be found in events/static/events/js/user_search.js
                    new_user = value
                    try:
                        new_user = User.objects.get(username=value)
                        event.guests.add(new_user)

                        event.save()
                        recipient_list.append({'email': new_user.email, 'username': new_user.username})
                    except User.DoesNotExist:
                        continue

            # determine the url to the events, e.g. localhost/events/5
            event_href = request.META['HTTP_HOST'] + '/events/' + str(event.pk)
            for recipient in recipient_list:
                html_message = 'Hallo ' + recipient['username'] + '!<br><br>Du wurdest von ' + organisator.username + \
                               ' zu einem Treffen im ofo - Online-Freizeit-Organisator eingeladen!<br>' \
                               'Klicke <a href="' + event_href + '">hier</a>, um mehr zu dem Treffen zu erfahren!<br>' \
                                                                 '<br><br>Falls der Link bei dir nicht funktioniert, ' \
                                                                 'gib einfach folgenden Link in den Browser ein:' \
                                                                 '<br><br>' + event_href + '<br><br>' \
                               'Viel Spaß!'
                send_mail(
                    subject='Neue Einladung - Online Freizeit Organisator',
                    html_message=html_message,
                    message=html_message,
                    from_email='online-freizeit-organisator@web.de',
                    # [recipient['email']],
                    recipient_list=['chr-herzog@web.de'],
                    fail_silently=False
                )
            return redirect('overview')
    else:
        form = NewEventForm()

    context = {'form': form}
    template = loader.get_template('events/events_new.html')
    return HttpResponse(template.render(context, request))


def user_search(request):
    """
    Endpoint for the live user search for the ajax request in events/static/events/js/user_search.js
    Searches for usernames in the database that start with the given "q" query parameter.
    The users are rendered in the events/search_result_partial.html template and the html output returned as a
    JsonResponse to the client
    """
    url_parameter = request.GET.get('q')
    if url_parameter:
        if request.is_ajax() or True:
            # search for usernames that start with the url_parameter
            users = User.objects.filter(username__startswith=url_parameter)
            if len(users) > 5:
                users = users[0:5]
            html = loader.render_to_string(template_name='events/search_result_partial.html', context={'users': users})
            data_return = {'html': html}
            return JsonResponse(data=data_return)
    data_return = {'html': ''}
    return JsonResponse(data=data_return)


@login_required(login_url='/login')
def delete_event(request):
    """
    Only logged-in users are allowed to delete events.
    It is also checked if the user is the organisator of the event. Otherwise the user is redirected to the
    overview view without deleting the event
    """
    url_parameter = request.GET.get('k')
    if url_parameter:
        try:
            event = Event.objects.get(pk=url_parameter)
        except Event.DoesNotExist:
            return redirect('overview')

        if not request.user == event.organisator:
            return redirect('overview')

        event.delete()
        return redirect('overview')
