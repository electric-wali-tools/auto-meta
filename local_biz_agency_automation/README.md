# 🤖 Local Biz Lead Automation Agent & CRM Web App

An autonomous AI Agent System designed to discover local businesses (EV Showrooms, Solar Installers, Modular Kitchen Dealers, etc.) missing a website, automatically build & host customized landing pages on GitHub Pages, pitch Market Gap & Future Scope, and alert the agency owner on Telegram/WhatsApp when a client requests a call.

---

## 🌟 Key Features

1. **Autonomous Lead Finder & Filter:**
   - Scans local businesses in target cities.
   - Isolates businesses lacking an official website or relying only on social media pages.

2. **Automated Custom Website Generator:**
   - Generates a mobile-responsive landing page tailored to the client's business name, location, and real Google Maps phone number.
   - Maps direct **Call (`tel:`)** and **WhatsApp Chat (`wa.me`)** buttons directly to the client's number.

3. **Instant GitHub Pages Deployment:**
   - Uploads generated landing pages directly to GitHub Pages via GitHub REST API for instant free live hosting.

4. **Market Gap & Future Scope Pitcher:**
   - Formulates personalized cold outreach messages highlighting lost online sales, competitor advantage, and includes the live demo link.

5. **Full Web App & CRM Dashboard:**
   - Master **Power ON/OFF** Switch.
   - **Active Hours Enforcement** (10:00 AM to 06:00 PM IST).
   - Interactive Lead CRM Table with status filtering (`NEW`, `DEMO_READY`, `PITCHED`, `HOT_LEAD`, `CLOSED_DEAL`).
   - Weekly & Monthly Analytics Graphs (Lead pipeline & Revenue growth).
   - Manual Agent Action Triggers ("Run Scanner", "Build Demos", "Send Pitches").

---

## 🚀 Quick Start Guide

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/local-biz-lead-agent.git
cd local-biz-lead-agent
```

### 2. Install Dependencies
```bash
pip install flask requests
```

### 3. Configure Environment Variables (`.env`)
Create a `.env` file in the root directory:
```env
GITHUB_TOKEN=your_github_personal_access_token
GITHUB_REPO=agency-demo-sites
MANISH_PHONE_NUMBER=+918299206433
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
TELEGRAM_CHAT_ID=your_telegram_chat_id
```

### 4. Run the Web Application & Agent
```bash
python app.py
```
Open your browser at: **`http://localhost:5000`**

---

## ☁️ Deploying Cloud 24/7 Autopilot (GitHub Actions)

A pre-configured GitHub Actions workflow is available at `.github/workflows/daily_outreach.yml`.
Add your secrets (`GH_PAT`, `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID`) under your GitHub Repository Settings -> Secrets, and the agent will run on autopilot every day!

---

## 📜 License
MIT License - Created for Agency Lead Automation.
