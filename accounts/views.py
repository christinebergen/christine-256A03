from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, permission_required

from django.contrib import messages
from django.contrib.auth.models import Group
from .forms import CustomUserCreationForm, AuthForm

from events.models import Event, EventRegistration

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            group_name = 'Registrant'
            group, created = Group.objects.get_or_create(name=group_name)
            group.user_set.add(user)
            auth_login(request, user)  # Corrected usage
            return redirect('events:event_list')  # Adjust this as needed
        else:
            return render(request, 'register.html', {'form': form})
    else:
        if request.user.is_authenticated:
            return redirect('events:event_list')
        form = CustomUserCreationForm()
        return render(request, 'register.html', {'form': form})

def login(request):
    if request.method == 'POST':
        form = AuthForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)  # Use the imported login function
            return redirect('events:event_list')  # Adjusted redirect
        else:
            return render(request, 'login.html', {'form': form})
    else:
        if request.user.is_authenticated:
            return redirect('events:event_list')  # Redirect if already logged in
        form = AuthForm(request)
        return render(request, 'login.html', {'form': form})
    
@login_required    
  
def reports(request):
    if request.method == 'GET':
        return render (request, 'reports.html')
    
@login_required    
@permission_required('events.add_event', raise_exception=True)
def user_list(request):
    users = User.objects.all()
    return render(request, 'user_list.html', {'users': users})

@login_required    
@permission_required('events.add_event', raise_exception=True)
def admin_events_list(request):
    events = Event.objects.all()
    events_with_registrants = []
    for event in events:
        registrants = EventRegistration.objects.filter(event=event).select_related('user')
        events_with_registrants.append((event, registrants))

    return render(request, 'admin_events_list.html', {'events_with_registrants': events_with_registrants})

def logoutaccount(request):
    auth_logout(request)
    return redirect('accounts:login')
