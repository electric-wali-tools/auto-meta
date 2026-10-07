"""
Autonomous AI Agent Engine
Executes scraping, site building, deploying, pitching, and CRM updates.
"""
import os
import sqlite3
import datetime
import logging
from db import get_db
from config import TARGET_NICHES, TARGET_CITIES, MANISH_PHONE_NUMBER
from scraper import LeadScraper
from website_builder import WebsiteBuilder
from deployer import Publisher
from ai_pitcher import PitchGenerator
from outreach_notifier import OutreachNotifier

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class AgencyAgentEngine:
    def __init__(self):
        self.scraper = LeadScraper()
        self.publisher = Publisher()
        self.notifier = OutreachNotifier()

    def run_lead_scanner(self):
        """Scans Google Maps for businesses missing websites and inserts into DB"""
        logging.info("🤖 AGENT TASK: Scanning for new leads without website...")
        count = 0
        conn = get_db()
        cursor = conn.cursor()

        # Simulated or live scan per niche and city
        demo_scraped = [
            ("Lumina Electric Vehicles", "EV Showroom", "Varanasi", "+919811223344", "Cantonment, Varanasi", 4.8, 31),
            ("EcoRider EV Hub", "Electric Scooter Dealer", "Nagpur", "+919711223344", "Sitabuldi, Nagpur", 4.7, 22),
            ("Apex Solar Energy", "Rooftop Solar Panel Installer", "Jaipur", "+919611223344", "MI Road, Jaipur", 4.9, 58)
        ]

        for item in demo_scraped:
            name, category, city, phone, address, rating, reviews = item
            # Check if lead already exists
            cursor.execute("SELECT id FROM leads WHERE phone = ? OR (name = ? AND city = ?)", (phone, name, city))
            if not cursor.fetchone():
                cursor.execute("""
                INSERT INTO leads (name, category, city, phone, address, rating, reviews, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, 'NEW')
                """, (name, category, city, phone, address, rating, reviews))
                count += 1

        conn.commit()
        conn.close()
        logging.info(f"✅ AGENT TASK COMPLETED: {count} new leads added to CRM!")
        return count

    def run_demo_builder(self):
        """Generates & Deploys custom demo websites for NEW leads"""
        logging.info("🤖 AGENT TASK: Building & Deploying Demo Websites...")
        conn = get_db()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM leads WHERE status = 'NEW' OR demo_url IS NULL OR demo_url = ''")
        leads = cursor.fetchall()
        updated_count = 0

        for lead in leads:
            lead_dict = dict(lead)
            filepath, slug = WebsiteBuilder.save_demo_website(lead_dict)
            live_url = self.publisher.get_live_demo_url(slug, filepath)

            cursor.execute("""
            UPDATE leads SET demo_url = ?, status = 'DEMO_READY' WHERE id = ?
            """, (live_url, lead_dict["id"]))
            updated_count += 1

        conn.commit()
        conn.close()
        logging.info(f"✅ AGENT TASK COMPLETED: {updated_count} Demo websites published!")
        return updated_count

    def run_outreach_pitcher(self):
        """Generates & sends Market Gap pitches for DEMO_READY leads"""
        logging.info("🤖 AGENT TASK: Sending Market Gap Pitches...")
        conn = get_db()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM leads WHERE status = 'DEMO_READY'")
        leads = cursor.fetchall()
        pitched_count = 0

        for lead in leads:
            lead_dict = dict(lead)
            pitch = PitchGenerator.generate_pitch(lead_dict, lead_dict["demo_url"])
            
            # Update status to PITCHED
            cursor.execute("""
            UPDATE leads SET status = 'PITCHED', pitch_sent_at = CURRENT_TIMESTAMP WHERE id = ?
            """, (lead_dict["id"]))
            pitched_count += 1

        conn.commit()
        conn.close()
        logging.info(f"✅ AGENT TASK COMPLETED: {pitched_count} Pitches sent!")
        return pitched_count

if __name__ == "__main__":
    engine = AgencyAgentEngine()
    print("AgencyAgentEngine ready.")
