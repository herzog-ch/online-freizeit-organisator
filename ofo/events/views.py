from django.shortcuts import redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.template import loader
from .forms import NewEventForm, ProposalForm, DetermineEventForm
from .models import Event, STATUS_OPEN, STATUS_DECIDED, Status, Proposal
from django.contrib.auth.models import User
from django.core.mail import send_mail


@login_required(login_url='/login')
def detail(request, event_id):
    try:
        event = Event.objects.get(pk=event_id)
    except Event.DoesNotExist:
        return redirect('overview')

    if event.organisator == request.user:
        is_organisator = True
    else:
        is_organisator = False

    if is_organisator and event.status.status == STATUS_OPEN:
        if request.method == 'POST':
            determine_event_form = DetermineEventForm(request.POST)
            if determine_event_form.is_valid():
                event.status = Status.objects.get(status=STATUS_DECIDED)
                event.date = determine_event_form.cleaned_data['date']
                event.time = determine_event_form.cleaned_data['time']
                event.place = determine_event_form.cleaned_data['place']
                event.save()
                event.refresh_from_db()
                determine_event_form = None
        else:
            determine_event_form = DetermineEventForm()
    else:
        determine_event_form = None

    try:
        Proposal.objects.filter(event=event).get(author=request.user)
        user_did_proposal = True
    except Proposal.DoesNotExist:
        user_did_proposal = False

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

    status = 'Offen für Vorschläge' if event.status == Status.objects.get(status=STATUS_OPEN) else 'Termin festgelegt'

    proposals = Proposal.objects.filter(event=event)

    guests = event.guests.all()

    context = {'proposal_form': proposal_form, 'determine_event_form': determine_event_form,
               'is_organisator': is_organisator, 'user_did_proposal': user_did_proposal,
               'event': event, 'guests': guests, 'status': status, 'proposals': proposals,
               'is_open_for_proposals': event.status.status == STATUS_OPEN}
    template = loader.get_template('events/events_detail.html')
    return HttpResponse(template.render(context, request))


@login_required(login_url='/login')
def overview(request):

    # load events invited
    events_invited = Event.objects.filter(guests=request.user)

    # load events organised by user
    events_organised = Event.objects.filter(organisator=request.user)

    context = {'events_invited': events_invited, 'events_organised': events_organised}
    template = loader.get_template('events/events_overview.html')
    return HttpResponse(template.render(context, request))


@login_required(login_url='/login')
def new_event(request):

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
                    new_user = value
                    try:
                        new_user = User.objects.get(username=value)
                        event.guests.add(new_user)
                        event.save()
                        recipient_list.append({'email': new_user.email, 'username': new_user.username})
                    except User.DoesNotExist:
                        continue

            for recipient in recipient_list:
                html_message = 'Hallo ' + recipient['username'] + ',\nDu wurdest zu einem neuen Treffen eingeladen!\n' \
                                                   'Klicke <a href="#disc">Hier</a>'
                send_mail(
                subject='Neue Einladung - Online Freizeit Organisator',
                html_message=html_message,
                message=html_message,
                from_email='online-freizeit-organisator@web.de',
                # [recipient['email']],
                recipient_list=['chr-herzog@web.de'],
                fail_silently=False
            )
            # request.META['HTTP_HOST']
            return redirect('overview')
    else:
        form = NewEventForm()

    context = {'form': form}
    template = loader.get_template('events/new_event.html')
    return HttpResponse(template.render(context, request))


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


@login_required(login_url='/login')
def delete_event(request):
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
