<<<<<<< HEAD
# plexapi
plexapi
=======

# Plex API Project

Tautulli API integration for multiple Plex servers.

## Setup

1. Create virtual environment:
   ```sh
   python -m venv venv
   ```

2. Activate virtual environment:
   - On Windows:
     ```sh
     .\venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```sh
     source venv/bin/activate
     ```

3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

4. Set up environment variables in `.env` file:
   ```
   TAUTULLI_URL_KOREA=<your_korea_tautulli_url>
   TAUTULLI_KEY_KOREA=<your_korea_tautulli_api_key>
   TAUTULLI_URL_GERMAN=<your_german_tautulli_url>
   TAUTULLI_KEY_GERMAN=<your_german_tautulli_api_key>
   TAUTULLI_TOKEN=<your_tautulli_token>
   ```

5. Run the application:
   ```sh
   uvicorn app.main:app --reload
   ```

## Usage

### Monthly Usage
- Endpoint: `/api/tautulli/monthly_usage`
- Method: `GET`
- Description: Get monthly usage data.

### Daily Usage
- Endpoint: `/api/tautulli/daily_usage`
- Method: `GET`
- Description: Get daily usage data.

### User Stats
- Endpoint: `/api/tautulli/userstats`
- Method: `GET`
- Description: Get user statistics.
- Parameters:
  - `period`: Number of days to query.
  - `region`: Region to query (`통합`, `한국`, `독일`).

## Middleware

### Usage Tracking Middleware
- File: `app/middleware/usage_tracking.py`
- Description: Middleware to track page visits.

## Routes

### Tautulli Routes
- File: `app/routes/tautulli.py`
- Description: Routes for Tautulli API integration.

## Main Application
- File: `app/main.py`
- Description: Main FastAPI application setup.
>>>>>>> ad50bb3 (Initial commit)
