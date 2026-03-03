# AI Job Alert Agent 🚀

A Python-based backend agent designed to run as a Cron Job on Render. Every hour, it fetches remote entry-level jobs in India using SerpAPI (Google Jobs), filters out duplicates using a PostgreSQL database, and sends you an email via Gmail SMTP.

## Directory Structure

```plaintext
ai_job_agent/
│
├── .env.example
├── database.py
├── email_service.py
├── main.py
├── models.py
├── README.md
├── render.yaml
├── requirements.txt
└── scraper.py
```

## Features

- **Automated Hourly Cron** (`0 * * * *`) tailored for a free-tier Render account.
- **SerpAPI Integeration** finding highly targeted remote/fresher jobs.
- **Duplicate Prevention** via Render's free PostgreSQL hosting using SQLAlchemy ORM.
- **Gmail SMTP Alerts**, safely handling plain-text updates to avoid complicated HTML parsing issues.
- **Rate-Limiting Protection** by incorporating pauses between SerpAPI endpoint accesses.

---

## 🛠 Set up Environment (Local Testing)

1. Clone or copy everything into a new folder.
2. Initialize virtualenv (Optional but recommended):
  ```bash
  python -m venv venv
  source venv/bin/activate  # On Windows: venv\Scripts\activate
  ```
3. Install dependencies:
  ```bash
  pip install -r requirements.txt
  ```
4. Set up Env Variables:
  - Copy `.env.example` to a new file named `.env`.
  - Enter your database URL, SerpAPI Key, and Email Credentials in `.env`. (If you leave `DATABASE_URL` empty, it creates `local_jobs.db` via SQLite for testing).

5. Run:
  ```bash
  python main.py
  ```

---

## ☁️ Step-by-Step Render Deployment Guide

### 1. Pre-requisites
- **GitHub**: Make a repository and push this code there.
- **SerpAPI Key**: Grab a free API key from [serpapi.com](https://serpapi.com).
- **Gmail App Passwords**:
  1. Go to your Google Account Settings > Security.
  2. Enable "2-Step Verification" if not active.
  3. Search for "App Passwords" in the Security search bar.
  4. Create a new one named "JobAlertAgent". Copy the 16-character string.

### 2. Connect to Render
Instead of manually clicking around, simply connect to Render using Blueprint mode.

1. Go to the [Render Dashboard](https://dashboard.render.com/) and create an account.
2. Click **New** -> **Blueprint**.
3. Connect your GitHub repository containing these files.
4. Render will detect the `render.yaml` file and automatically configure:
   - A **PostgreSQL database** (job_agent_db).
   - A **Cron Job** (ai_job_agent_cron) set to run every 1 hour (`0 * * * *`).

### 3. Add Environment Variables
The blueprint knows you need variables, but you need to paste their real values.

1. Go to your new **Cron Job service** inside the Dashboard.
2. Click on the **Environment** tab on the left.
3. Add the missing keys if they prompt or paste their missing Sync values:
   - `SERPAPI_KEY` = your SerpAPI generated Key
   - `EMAIL_ADDRESS` = your gmail (e.g., you@gmail.com)
   - `EMAIL_PASSWORD` = your Google 16-char App Password
   - `RECEIVER_EMAIL` = where you want to receive the alerts
   - *(Note: Your `DATABASE_URL` is automatically securely mapped!)*

### 4. Create Render Cron Job (Manual Method - if avoiding Blueprint)
If you do not want to use Blueprint:
1. Click **New** -> **PostgreSQL**. Create the DB, wait until live. Scroll down to copy "Internal Database URL".
2. Click **New** -> **Cron Job**.
3. Connect Repo.
4. Language: `Python`, Build Command: `pip install -r requirements.txt`, Start Command: `python main.py`, Schedule: `0 * * * *`.
5. Enter all environment variables described above. Paste Database URL replacing `postgres://` with `postgresql://`.
6. Save and Deploy.

---

## Future Scaling to SaaS

If you want to move beyond personal use:
1. **Frontend Dashboard**: Add a FastAPI/Next.js stack to accept more users' queries.
2. **Dynamic Jobs Database**: Scale database, replace local JSON configuration variables with dynamic user profiles.
3. **Dedicated Email Domain**: Swap `smtplib`/Gmail for SendGrid or AWS SES to handle bulk emails without being flagged as Spam.
4. **Proxy rotation**: SerpAPI free limits will expire with more users. You'd need a paid proxy manager.
