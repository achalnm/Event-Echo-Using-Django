from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.utils import timezone
from django.contrib import messages
from django.db.models import Q
from django.urls import reverse
from datetime import timedelta
from io import BytesIO
import qrcode
from django.core.files import File

from .forms import SignUpForm, LoginForm, EventForm
from .models import Event, Registration


def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                next_url = request.POST.get('next') or request.GET.get('next')
                return redirect(next_url or 'dashboard')
            else:
                form.add_error(None, 'Invalid username or password.')
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def dashboard_view(request):
    from .recommendations import get_recommendations

    events = list(Event.objects.all())
    registered_ids = set(
        Registration.objects.filter(user=request.user).values_list('event_id', flat=True)
    )
    my_registrations = list(
        Registration.objects.filter(user=request.user).select_related('event')
    )

    for event in events:
        count = Registration.objects.filter(event=event).count()
        event.spots_remaining = event.capacity - count
        event.is_full = event.spots_remaining <= 0

    recommended = get_recommendations(request.user, events)

    registered_events = [e for e in events if e.id in registered_ids]
    all_tags = []
    for e in registered_events:
        if e.tags:
            all_tags.extend(t.strip() for t in e.tags.split(',') if t.strip())
    unique_tags = list(dict.fromkeys(all_tags))
    interest_label = ', '.join(unique_tags[:3]) if unique_tags else 'popular events'

    return render(request, 'accounts/dashboard.html', {
        'events': events,
        'registered_ids': registered_ids,
        'my_registrations': my_registrations,
        'recommended': recommended,
        'interest_label': interest_label,
    })


@login_required
def add_event_view(request):
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Event added successfully!')
            return redirect('dashboard')
    else:
        form = EventForm()
    return render(request, 'accounts/add_event.html', {'form': form})


@login_required
def event_detail_view(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    count = Registration.objects.filter(event=event).count()
    event.spots_remaining = event.capacity - count
    event.is_full = event.spots_remaining <= 0
    already_registered = Registration.objects.filter(user=request.user, event=event).exists()
    return render(request, 'events/event_detail.html', {
        'event': event,
        'already_registered': already_registered,
    })


@login_required
def register_for_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    count = Registration.objects.filter(event=event).count()
    spots_remaining = event.capacity - count

    if Registration.objects.filter(user=request.user, event=event).exists():
        messages.info(request, 'You are already registered for this event.')
        return redirect('dashboard')

    if spots_remaining <= 0:
        return render(request, 'events/register.html', {
            'event': event,
            'is_full': True,
            'spots_remaining': 0,
        })

    if request.method == 'POST':
        registration = Registration(user=request.user, event=event)
        registration.save()

        qr_data = (
            f"User: {request.user.username}\n"
            f"Event: {event.name}\n"
            f"Date: {event.date.strftime('%Y-%m-%d %H:%M')}\n"
            f"Registration ID: {registration.id}"
        )
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(qr_data)
        qr.make(fit=True)
        img = qr.make_image(fill_color='black', back_color='white')

        buffer = BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)
        registration.qr_code.save(f'registration_{registration.id}.png', File(buffer), save=True)

        messages.success(request, f'Successfully registered for {event.name}!')
        return redirect('dashboard')

    return render(request, 'events/register.html', {
        'event': event,
        'is_full': False,
        'spots_remaining': spots_remaining,
    })


@login_required
def ticket_view(request, registration_id):
    registration = get_object_or_404(Registration, id=registration_id, user=request.user)
    return render(request, 'events/ticket.html', {'registration': registration})


def search_events(request):
    query = request.GET.get('q', '')
    filter_type = request.GET.get('filter', 'all')
    events = Event.objects.all()

    if query:
        events = events.filter(Q(name__icontains=query) | Q(location__icontains=query))

    now = timezone.now()
    if filter_type == 'today':
        events = events.filter(date__date=now.date())
    elif filter_type == 'week':
        events = events.filter(date__gte=now, date__lte=now + timedelta(days=7))
    elif filter_type == 'free':
        events = events.filter(price=0)

    registered_ids = set()
    if request.user.is_authenticated:
        registered_ids = set(
            Registration.objects.filter(user=request.user).values_list('event_id', flat=True)
        )

    data = []
    for event in events:
        count = Registration.objects.filter(event=event).count()
        spots_remaining = event.capacity - count
        data.append({
            'id': event.id,
            'name': event.name,
            'description': event.description[:100] + ('...' if len(event.description) > 100 else ''),
            'date': event.date.strftime('%b %d, %Y'),
            'location': event.location,
            'price': float(event.price),
            'image_url': event.image.url if event.image else '',
            'spots_remaining': spots_remaining,
            'is_full': spots_remaining <= 0,
            'is_registered': event.id in registered_ids,
            'detail_url': reverse('event_detail', args=[event.id]),
            'register_url': reverse('register_for_event', args=[event.id]),
        })

    return JsonResponse({'events': data})
