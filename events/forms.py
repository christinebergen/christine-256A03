# events/forms.py
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