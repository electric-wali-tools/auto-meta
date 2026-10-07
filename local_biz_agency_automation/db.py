"""
Database Handler for Agency AI Lead Automation System
Uses SQLite to store lead records, generated sites, outreach history, and analytics.
"""
import os
import sqlite3
import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), "database.db")

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()

    # Leads Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS leads (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        category TEXT NOT NULL,
        city TEXT NOT NULL,
        phone TEXT,
        address TEXT,
        rating REAL DEFAULT 0.0,
        reviews INTEGER DEFAULT 0,
        demo_url TEXT,
        status TEXT DEFAULT 'NEW',
        pitch_sent_at TIMESTAMP,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        notes TEXT
    )
    """)

    # Settings Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS settings (
        key TEXT PRIMARY KEY,
        value TEXT
    )
    """)

    # Default Settings
    default_settings = {
        "is_running": "true",
        "start_hour": "10",
        "end_hour": "18",
        "manish_phone": "+918299206433"
    }

    for k, v in default_settings.items():
        cursor.execute("INSERT OR IGNORE INTO settings (key, value) VALUES (?, ?)", (k, v))

    # Insert sample seed leads if database is empty for rich UI demonstration
    cursor.execute("SELECT COUNT(*) as count FROM leads")
    if cursor.fetchone()["count"] == 0:
        sample_leads = [
            ("Mahindra Electric Showroom", "EV Showroom", "Lucknow", "+919876543210", "Hazratganj, Lucknow", 4.8, 42, "https://manish-agency.github.io/agency-demo-sites/mahindra_ev/", "HOT_LEAD", "Client replied: 'Call me for pricing'"),
            ("GreenVolt Scooter Hub", "Electric Scooter Dealer", "Kanpur", "+919876543211", "Mall Road, Kanpur", 4.6, 28, "https://manish-agency.github.io/agency-demo-sites/greenvolt_scooter/", "DEMO_READY", "Website published on GitHub"),
            ("Surya Solar Systems", "Rooftop Solar Panel Installer", "Indore", "+919123456789", "Vijay Nagar, Indore", 4.9, 65, "https://manish-agency.github.io/agency-demo-sites/surya_solar/", "CLOSED_DEAL", "Deal closed for Rs 25,000!"),
            ("Urban Touch Modular Kitchen", "Modular Kitchen Dealer", "Bhopal", "+919988776655", "MP Nagar, Bhopal", 4.7, 34, "https://manish-agency.github.io/agency-demo-sites/urban_touch/", "PITCHED", "Pitch sent via WhatsApp"),
            ("Apex Heavy Machinery", "Industrial Machinery Supplier", "Patna", "+919456781234", "Boring Road, Patna", 4.5, 19, "", "NEW", "Filtered without website")
        ]
        cursor.executemany("""
        INSERT INTO leads (name, category, city, phone, address, rating, reviews, demo_url, status, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, sample_leads)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("Database initialized successfully.")
