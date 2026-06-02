# EventEcho: Event Management Platform

Originally built as a third year mini project for the Bachelor of Engineering in Computer Science at Jyothy Institute of Technology, VTU, Bangalore. Later extended with AI-powered recommendations, QR code ticketing, seat capacity management, and real-time search.

---

## Features

- User signup, login and authentication
- Browse and register for events
- Seat capacity tracking with live spots remaining
- QR code ticket generated on registration, printable from browser
- AI event recommendations using TF-IDF cosine similarity on event tags
- Real-time search by name or location, filter by today, this week, or free events
- Responsive UI with Bootstrap 5
- 6 automated tests covering signup, login, event creation, capacity enforcement, QR generation, and recommendations

---

## Tech Stack

| Layer | Technology |
| --- | --- |
| Language | Python |
| Framework | Django 6.0 |
| Database | SQLite |
| AI / Recommendations | scikit-learn (TF-IDF, cosine similarity) |
| QR Codes | qrcode, Pillow |
| Frontend | Bootstrap 5 |

---

## Setup

```bash
git clone https://github.com/achalnm/Event-Echo-Using-Django.git
cd Event-Echo-Using-Django
python -m venv venv
venv\Scripts\activate   # Windows
source venv/bin/activate  # macOS/Linux
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Open `http://127.0.0.1:8000` in the browser.

To access the admin panel: `python manage.py createsuperuser` then go to `http://127.0.0.1:8000/admin/`

---

## Tests

```bash
python manage.py test
```

Runs 6 tests covering: signup, login, event creation, capacity enforcement, QR code file generation, and TF-IDF recommendation output.

---

## Project Notes

This project was originally submitted as a third year mini project with basic Django CRUD functionality. It was later revisited and extended with the features above as a learning exercise in web development, ML integration, and software testing.
