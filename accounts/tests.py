import os
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.conf import settings
from django.utils import timezone

from .models import Event, Registration
from .recommendations import get_recommendations


class SignupTest(TestCase):
    def test_signup(self):
        response = self.client.post(reverse('signup'), {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'EventEcho2024!',
            'password2': 'EventEcho2024!',
        })
        self.assertRedirects(response, reverse('dashboard'))
        self.assertTrue(User.objects.filter(username='newuser').exists())


class LoginTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='loginuser', password='EventEcho2024!')

    def test_login(self):
        response = self.client.post(reverse('login'), {
            'username': 'loginuser',
            'password': 'EventEcho2024!',
        })
        self.assertRedirects(response, reverse('dashboard'))


class EventCreationTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='eventuser', password='EventEcho2024!')
        self.client.force_login(self.user)

    def test_event_creation(self):
        response = self.client.post(reverse('add_event'), {
            'name': 'Test Concert',
            'description': 'A great concert event',
            'date': '2026-12-01 18:00',
            'location': 'Main Stage',
            'price': '0.00',
            'capacity': '100',
            'tags': 'music, concert',
        })
        self.assertRedirects(response, reverse('dashboard'))
        self.assertTrue(Event.objects.filter(name='Test Concert').exists())


class RegistrationCapacityTest(TestCase):
    def setUp(self):
        self.event = Event.objects.create(
            name='Limited Event',
            description='Only 1 seat',
            location='Venue',
            capacity=1,
        )
        self.user1 = User.objects.create_user(username='cap_user1', password='EventEcho2024!')
        self.user2 = User.objects.create_user(username='cap_user2', password='EventEcho2024!')

    def test_registration_capacity(self):
        self.client.force_login(self.user1)
        response = self.client.post(reverse('register_for_event', args=[self.event.id]))
        self.assertRedirects(response, reverse('dashboard'))
        self.assertEqual(Registration.objects.filter(event=self.event).count(), 1)

        self.client.force_login(self.user2)
        self.client.post(reverse('register_for_event', args=[self.event.id]))
        self.assertEqual(Registration.objects.filter(event=self.event).count(), 1)


class QRCodeTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='qruser', password='EventEcho2024!')
        self.event = Event.objects.create(
            name='QR Event',
            description='QR test',
            location='Test Venue',
            capacity=10,
        )

    def test_qr_code_generated(self):
        self.client.force_login(self.user)
        self.client.post(reverse('register_for_event', args=[self.event.id]))
        registration = Registration.objects.get(user=self.user, event=self.event)
        self.assertTrue(bool(registration.qr_code))
        qr_path = os.path.join(settings.MEDIA_ROOT, registration.qr_code.name)
        self.assertTrue(os.path.exists(qr_path))

    def tearDown(self):
        for reg in Registration.objects.filter(user=self.user):
            if reg.qr_code:
                path = os.path.join(settings.MEDIA_ROOT, reg.qr_code.name)
                if os.path.exists(path):
                    os.remove(path)


class RecommendationsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='recuser', password='EventEcho2024!')
        future = timezone.now().replace(year=2030)
        self.music_event = Event.objects.create(
            name='Jazz Night', description='Jazz evening', location='Jazz Club',
            capacity=50, tags='music, jazz', date=future,
        )
        self.rock_event = Event.objects.create(
            name='Rock Concert', description='Rock show', location='Arena',
            capacity=50, tags='music, rock', date=future,
        )
        self.art_event = Event.objects.create(
            name='Art Exhibition', description='Modern art', location='Gallery',
            capacity=50, tags='art, visual, painting', date=future,
        )

    def test_recommendations(self):
        Registration.objects.create(user=self.user, event=self.music_event)
        all_events = list(Event.objects.all())
        recommendations = get_recommendations(self.user, all_events)

        rec_ids = [e.id for e in recommendations]
        self.assertNotIn(self.music_event.id, rec_ids)
        self.assertIn(self.rock_event.id, rec_ids)
