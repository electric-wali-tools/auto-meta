import os
import json
import urllib.request
import urllib.error

# Load .env file manually
env_path = os.path.join(os.path.dirname(__file__), ".env")
if os.path.exists(env_path):
    with open(env_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ[k.strip()] = v.strip()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")
GITHUB_REPO = os.getenv("GITHUB_REPO", "agency-demo-sites")
MANISH_PHONE_NUMBER = os.getenv("MANISH_PHONE_NUMBER", "+918299206433")

# Auto-detect GitHub Username using standard urllib
GITHUB_USERNAME = os.getenv("GITHUB_USERNAME", "")
if GITHUB_TOKEN and not GITHUB_USERNAME:
    try:
        req = urllib.request.Request(
            "https://api.github.com/user",
            headers={"Authorization": f"token {GITHUB_TOKEN}", "User-Agent": "Python-Agency-App"}
        )
        with urllib.request.urlopen(req) as response:
            if response.status == 200:
                data = json.loads(response.read().decode("utf-8"))
                GITHUB_USERNAME = data.get("login", "")
                os.environ["GITHUB_USERNAME"] = GITHUB_USERNAME
    except Exception:
        pass

# Low-Competition & High-Ticket Niches
TARGET_NICHES = [
    "EV Showroom",
    "Electric Scooter Dealer",
    "Rooftop Solar Panel Installer",
    "Modular Kitchen Dealer",
    "Interior Designer Contractor",
    "Commercial AC Repair Service",
    "Industrial Machinery Supplier",
    "Banquet Hall Event Planner"
]

# Target Cities
TARGET_CITIES = [
    "Lucknow", "Kanpur", "Indore", "Bhopal", "Patna", "Ranchi", 
    "Varanasi", "Nagpur", "Coimbatore", "Chandigarh", "Jaipur"
]

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "YOUR_TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "YOUR_TELEGRAM_CHAT_ID")
