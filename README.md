# Kosh Ticketing

A full-stack event ticketing application inspired by modern platforms like Madfun. Built with React, Flask, and SQLite.

## Tech Stack

- **Frontend**: React 18, React Router, Tailwind CSS, Framer Motion, React Query
- **Backend**: Flask, SQLAlchemy, Marshmallow, Flask-JWT-Extended
- **Database**: SQLite (easily switchable to PostgreSQL)

## Quick Start

### Backend

```bash
cd backend
python3 -m venv venv
source venv/bin/activate  
pip install -r requirements.txt
python3 seed_data.py       
python3 run.py             # Start server on http://localhost:5000
```

### Frontend

```bash
cd frontend
npm install
npm start                 # Start dev server on http://localhost:3000
```

## Demo Accounts

| Role | Email | Password |
|------|-------|----------|
| Admin | admin@koshticketing.com | admin123 |
| Organizer | organizer@koshticketing.com | organizer123 |
| Customer | customer@koshticketing.com | customer123 |

## Features

- Event discovery with search, filters, and categories
- Interactive ticket tier selection with real-time pricing
- 3-step checkout (Guest/Account -> Attendees -> Payment)
- Digital tickets with QR codes
- Organizer dashboard with sales analytics
- Responsive dark-themed UI
