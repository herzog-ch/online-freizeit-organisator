from django import forms
from datetime import date, datetime


class NewEventForm(forms.Form):
    title = forms.CharField(label='Titel', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control',
                                                                                  'placeholder': 'Titel'}))
    place = forms.CharField(label='Vorschlag Ort', max_length=50, widget=forms.TextInput(attrs={'class': 'form-control',
                                                                                         'placeholder': 'Vorschlag Ort'}))
    duration = forms.IntegerField(label='Dauer (Minuten)', initial=30, min_value=15, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    date = forms.DateField(label='Datum', initial=datetime.now().strftime("%Y-%m-%d"), widget=forms.widgets.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    time = forms.TimeField(label='Uhrzeit', initial=datetime.now().strftime("%H:%M"), widget=forms.widgets.TimeInput(attrs={'class': 'form-control', 'type': 'time'}))

    def clean_date(self):
        date_input = self.cleaned_data['date']
        if date_input < date.today():
            raise forms.ValidationError('Das Datum darf nicht in der Vergangenheit liegen.')
        return date_input


class ProposalForm(forms.Form):
    date = forms.DateField(label='Datum vorschlagen', initial=datetime.now().strftime("%Y-%m-%d"),
                           widget=forms.widgets.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    time = forms.TimeField(label='Uhrzeit vorschlagen', initial=datetime.now().strftime("%H:%M"),
                           widget=forms.widgets.TimeInput(attrs={'class': 'form-control', 'type': 'time'}))
    place = forms.CharField(label='Ort vorschlagen', max_length=50, widget=forms.TextInput(attrs={'class': 'form-control',
                                                                                         'placeholder': 'Vorschlag Ort'}))
    comment = forms.CharField(label='Kommentar', max_length=200, widget=forms.widgets.Textarea(attrs={'class': 'form-control', 'placeholder': 'Kommentar eingeben..', 'rows': '3'}))


class DetermineEventForm(forms.Form):
    date = forms.DateField(label='Datum festlegen', initial=datetime.now().strftime("%Y-%m-%d"),
                           widget=forms.widgets.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    time = forms.TimeField(label='Uhrzeit festlegen', initial=datetime.now().strftime("%H:%M"),
                           widget=forms.widgets.TimeInput(attrs={'class': 'form-control', 'type': 'time'}))
    place = forms.CharField(label='Ort festlegen', max_length=50, widget=forms.TextInput(attrs={'class': 'form-control',
                                                                                         'placeholder': 'Ort'}))
    comment = forms.CharField(label='Kommentar', max_length=200, widget=forms.widgets.Textarea(attrs={'class': 'form-control', 'placeholder': 'Kommentar eingeben..', 'rows': '3'}))
