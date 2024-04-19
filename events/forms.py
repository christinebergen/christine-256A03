from django import forms
from .models import Event, EventRegistration

class EventRegistrationForm(forms.ModelForm):
    class Meta:
        model = EventRegistration
        fields = ['event']  # You might want to allow users to select the event, or handle it in the view.

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'description', 'date', 'location', 'organizer']
        labels = {
            'name': 'Event Title',
            'description': 'Event Description',
            'date': 'Event Date',
            'location': 'Event Location',
            'organizer': 'Event Organizer'
        }
        widgets = {
            'name': forms.TextInput(attrs={ 'class': 'input input-bordered border-2'}),
            'description': forms.Textarea(attrs={'rows': 2, 'cols': 40, 'class': 'textarea textarea-bordered border-2 mt-4'}),
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class':'border-2 mt-4'}),
            'location': forms.TextInput(attrs={'class': 'input input-bordered border-2 mt-4'}),
            'organizer': forms.Select(attrs={'class': 'select select-bordered border-2 mt-4 mb-4'}),

        }