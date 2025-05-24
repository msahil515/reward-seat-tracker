# Reward Seat Flights Tracker

A tool to track and monitor reward seat availability across multiple airlines.

## Features

- Track reward seat availability for multiple routes
- Support for major airlines (Virgin Atlantic, British Airways, etc.)
- Email/SMS notifications when seats become available
- Price tracking and historical data
- Web scraping with Playwright

## Tech Stack

- Python 3.9+
- Playwright for web automation
- FastAPI for web interface
- SQLite for data storage
- Celery for background tasks

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Install Playwright browsers:
```bash
playwright install
```

3. Run the application:
```bash
python main.py
```

## Configuration

Edit `config.json` to add routes and notification preferences.