#!/usr/bin/env python3
"""
views.py — Views for the 'vylety' Django application.

Handles user-facing pages including homepage, registration, login, event listings,
event detail, application forms and user's personal application history.
"""

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .models import Event, Application
from .forms import RegistrationForm, ApplicationForm

def index(request):
    """Render the homepage."""
    return render(request, 'index.html')

def event_list(request):
    """Displays a list of all available events ordered by date."""
    events = Event.objects.all().order_by('date')
    return render(request, 'events.html', {'events': events})

def event_detail(request, event_id):
    """Displays detailed information about a specific event.

    Args:
        request (HttpRequest): The incoming HTTP request.
        event_id (int): The primary key of the event to display.

    Returns:
        HttpResponse: Rendered HTML page with event details.
    """
    event = get_object_or_404(Event, id=event_id)
    return render(request, 'event_detail.html', {'event': event})

@login_required
def apply_to_event(request, event_id):
    """Handles the process of applying a logged-in user to a specific event.

    If user is already registered, redirect back to event detail.
    Otherwise, show or process the application form.
    """
    event = get_object_or_404(Event, id=event_id)
    if Application.objects.filter(user=request.user, event=event).exists():
        return redirect('event_detail', event_id=event.id)

    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.user = request.user
            application.event = event
            application.save()
            return redirect('my_applications')
    else:
        form = ApplicationForm()

    return render(request, 'apply.html', {'form': form, 'event': event})

@login_required
def my_applications(request):
    """Shows a logged-in user their list of applications to various events."""
    applications = Application.objects.filter(user=request.user).select_related('event')
    return render(request, 'my_applications.html', {'applications': applications})

def register(request):
    """Handles user registration. If form is valid, logs user in and redirects to events."""
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('event_list')
    else:
        form = RegistrationForm()

    return render(request, 'register.html', {'form': form})
