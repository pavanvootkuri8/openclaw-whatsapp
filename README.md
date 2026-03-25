# openclaw-whatsapp
openclaw-whatsapp integration
# OpenClaw WhatsApp Integration

OpenClaw is a job aggregation and notification system that fetches job postings from various sources, filters them based on user-defined criteria, and sends notifications via WhatsApp.

## Features

- **Job Fetching**: Fetch jobs from platforms like Greenhouse, Lever, and Indeed.
- **Filtering**: Apply keyword, location, and exclusion filters to refine job results.
- **Notifications**: Send job alerts via WhatsApp using Twilio.
- **Web Interface**: View job postings in a simple web interface.

## Project Structure

openclaw/ ├── config/ # Configuration files ├── data/ # Job data and sent job records ├── fetcher/ # Job fetching scripts ├── notifier/ # Notification scripts ├── web/ # Web interface ├── docker-compose.yml # Docker Compose configuration ├── Dockerfile # Base Dockerfile ├── run.py # Main script for sending notifications └── .env # Environment variables


## Prerequisites

- Docker and Docker Compose
- Twilio account for WhatsApp notifications

## Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/openclaw-whatsapp.git
   cd openclaw-whatsapp

   Workspace
(rerun without)
Collecting workspace information



openclaw/ ├── config/ # Configuration files ├── data/ # Job data and sent job records ├── fetcher/ # Job fetching scripts ├── notifier/ # Notification scripts ├── web/ # Web interface ├── docker-compose.yml # Docker Compose configuration ├── Dockerfile # Base Dockerfile ├── run.py # Main script for sending notifications └── .env # Environment variables

whatsapp
Configure environment variables in .env:

TWILIO_ACCOUNT_SID=your_twilio_account_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
WHATSAPP_FROM=whatsapp:+your_twilio_number
WHATSAPP_TO=whatsapp:+recipient_number


Update config/config.yaml with your job filters and sources.

Usage
Run with Docker Compose
Build and start the services:

docker-compose up --build

Access the web interface at http://localhost:5001.

Fetch Jobs
The fetcher service periodically fetches jobs and saves them to data/jobs.yaml.

Send Notifications
The notifier service sends WhatsApp notifications for new jobs.

Web Interface
The web interface displays the fetched jobs in a table format. Access it at http://localhost:5001.


