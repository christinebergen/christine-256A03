from django.http import HttpResponseNotAllowed
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required, permission_required

from .models import Event, EventRegistration
from django.contrib import messages
from .forms import EventForm


@login_required        
def event_list(request):
    if request.method =='GET':
        events = Event.objects.all()
        return render(request, 'events.html', {'events': events, 'user': request.user,
        'groups': request.user.groups.all()})
    
@login_required    
@permission_required('events.add_event', raise_exception=True)
def event_create(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('events:event_list')  # Assuming you have an event list URL to redirect to
    else:
        form = EventForm()
    return render(request, 'create_event.html', {'form': form})
    
@login_required
@permission_required('events.change_event', raise_exception=True)
def event_update(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, 'Event updated successfully.')
            return redirect('events:event_list')  # Redirect to a URL where users can see the event list
    else:
        form = EventForm(instance=event)
    return render(request, 'create_event.html', {'form': form})

@login_required
@permission_required('events.delete_event', raise_exception=True)
def event_delete(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        event.delete()
        messages.success(request, 'Event deleted successfully.')
        return redirect('events:event_list')
    return HttpResponseNotAllowed(['POST'])

@login_required
@permission_required('events.can_register', raise_exception=True)
def event_register(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if not EventRegistration.objects.filter(event=event, user=request.user).exists():
        EventRegistration.objects.create(event=event, user=request.user)
        messages.success(request, "You have registered for the event.")
    else:
        messages.error(request, "You are already registered for this event.")
    return render(request, 'registered_events.html')

@login_required
def unregister(request, pk):
    event = get_object_or_404(Event, pk=pk)
    registration = EventRegistration.objects.filter(event=event, user=request.user)
    if registration.exists():
        registration.delete()
        messages.success(request, "You have unregistered from the event.")
    else:
        messages.error(request, "You were not registered for this event.")
    return redirect('events:event_list')

@login_required
def registered_events(request):
    # Fetch all registrations for the current user
    registrations = EventRegistration.objects.filter(user=request.user)
    # Extract just the events from those registrations
    events = [registration.event for registration in registrations]
    return render(request, 'registered_events.html', {'events': events})