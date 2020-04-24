from django import forms
from datetime import date, datetime


class NewEventForm(forms.Form):
    title = forms.CharField(label='Titel', max_length=100)
    place = forms.CharField(label='Vorschlag Ort', max_length=50)
    duration = forms.IntegerField(label='Dauer (Minuten)', initial=30, min_value=15)
    date = forms.DateField(label='Datum', initial=datetime.now().strftime("%Y-%m-%d"), widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    time = forms.TimeField(label='Uhrzeit', initial=datetime.now().strftime("%H:%M"), widget=forms.widgets.TimeInput(attrs={'type': 'time'}))
    # guests = forms.CharField(label='Teilnehmer', widget=forms.HiddenInput)

    def clean_date(self):
        date_input = self.cleaned_data['date']
        if date_input < date.today():
            raise forms.ValidationError('Das Datum darf nicht in der Vergangenheit liegen')
        return date_input


class ProposalForm(forms.Form):
    date = forms.DateField(label='Datum', initial=datetime.now().strftime("%Y-%m-%d"),
                           widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    time = forms.TimeField(label='Uhrzeit', initial=datetime.now().strftime("%H:%M"),
                           widget=forms.widgets.TimeInput(attrs={'type': 'time'}))
    place = forms.CharField(label='Vorschlag Ort', max_length=50)
    comment = forms.CharField(label='Kommentar', max_length=200)


class DetermineEventForm(forms.Form):
    date = forms.DateField(label='Datum festlegen', initial=datetime.now().strftime("%Y-%m-%d"),
                           widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    time = forms.TimeField(label='Uhrzeit festlegen', initial=datetime.now().strftime("%H:%M"),
                           widget=forms.widgets.TimeInput(attrs={'type': 'time'}))
    place = forms.CharField(label='Ort festlegen', max_length=50)
    comment = forms.CharField(label='Kommentar', max_length=200, widget=forms.widgets.Textarea)
