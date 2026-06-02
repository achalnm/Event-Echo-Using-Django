# EventEcho

EventEcho is an event management web app built with Django. Users can sign up, browse upcoming events, register for them and get a QR code ticket. Organisers can add events with seat limits and tags. There's also a recommendations feature that suggests events based on what you've registered for before, and a search/filter on the dashboard.

## Features

- User signup, login and logout
- Browse events and register
- Seat tracking, shows spots remaining
- QR code ticket on registration, printable
- Event recommendations based on past registrations and tags
- Search by name or location, filter by today / this week / free

## Screenshots

> Add screenshots here

## Setup

```bash
git clone https://github.com/achalnm/Event-Echo-Using-Django.git
cd Event-Echo-Using-Django
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Open `http://127.0.0.1:8000` in the browser.

For the admin panel run `python manage.py createsuperuser` first, then go to `http://127.0.0.1:8000/admin/`.

## Tech Stack

| Layer | Technology |
| --- | --- |
| Language | Python 3.13 |
| Framework | Django 6.0 |
| Database | SQLite |
| Recommendations | scikit-learn |
| QR Codes | qrcode, Pillow |
| Frontend | Bootstrap 5 |
