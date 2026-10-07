"""
Main Automation Orchestrator (Updated with Web Dashboard Control & 10 AM - 6 PM Schedule Enforcement)
"""
import os
import json
import time
import datetime
import logging
from config import TARGET_NICHES, TARGET_CITIES, MANISH_PHONE_NUMBER
from scraper import LeadScraper
from website_builder import WebsiteBuilder
from deployer import Publisher
from ai_pitcher import PitchGenerator
from outreach_notifier import OutreachNotifier

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
STATUS_FILE = os.path.join(os.path.dirname(__file__), "status.json")

def check_should_run():
    """Checks ON/OFF switch status and enforces 10 AM to 6 PM working window"""
    if os.path.exists(STATUS_FILE):
        try:
            with open(STATUS_FILE, "r") as f:
                status = json.load(f)
                if not status.get("is_running", True):
                    logging.info("🔴 Engine is TURNED OFF via Web Dashboard.")
                    return False
                
                start_h = status.get("start_hour", 10)
                end_h = status.get("end_hour", 18)
                now_h = datetime.datetime.now().hour
                
                if not (start_h <= now_h < end_h):
                    logging.info(f"🟡 Outside active operating hours ({start_h}:00 AM - {end_h}:00 PM). Pausing Engine.")
                    return False
        except Exception as e:
            logging.error(f"Error reading status.json: {e}")
    return True

def run_agency_automation(google_api_key=None, test_mode=True):
    if not check_should_run():
        print("⏸️ Engine is currently PAUSED or OFF. Toggle ON via Dashboard (http://localhost:5000).")
        return

    scraper = LeadScraper(api_key=google_api_key)
    publisher = Publisher()
    notifier = OutreachNotifier()

    print("==================================================================")
    print("🚀 AUTOMATED LOCAL BIZ WEBSITE AGENCY ENGINE (ACTIVE) 🚀")
    print("==================================================================")

    if test_mode:
        print("🧪 RUNNING DEMO SEQUENCE (RESPECTING ON/OFF DASHBOARD TOGGLE)...\n")
        sample_leads = [
            {
                "name": "Mahindra Electric EV Showroom",
                "city": "Lucknow",
                "phone": "+919876543210",
                "category": "EV Showroom",
                "address": "Hazratganj, Lucknow",
                "rating": 4.8,
                "reviews": 42,
                "has_website": False
            }
        ]
        
        for lead in sample_leads:
            print(f"📌 [STEP 1] Found Lead without Website: {lead['name']} ({lead['category']} - {lead['city']})")
            
            # Step 2: Build Custom Demo Website HTML with Client's Phone/WhatsApp
            filepath, slug = WebsiteBuilder.save_demo_website(lead)
            print(f"🖥️ [STEP 2] Custom Website Generated: {filepath}")

            # Step 3: Deploy & Get Hosted Live URL
            demo_url = publisher.get_live_demo_url(slug, filepath)
            print(f"🌐 [STEP 3] Hosted Demo Website Link: {demo_url}")

            # Step 4: Generate Pitch with Market Gap + Future Scope + Demo Link
            pitch = PitchGenerator.generate_pitch(lead, demo_url)
            print("\n📩 [STEP 4] Generated Pitch Message with Market Gap & Live Demo Link:")
            print("------------------------------------------------------------------")
            print(pitch)
            print("------------------------------------------------------------------\n")

            # Step 5: Simulate Client Reply & Lead Hand-off to Manish
            simulated_client_reply = "Aapki sample website achhi hai, mujhe call kijiye"
            print(f"💬 Client Replied: '{simulated_client_reply}'")

            is_handed_off = notifier.process_incoming_reply(lead, simulated_client_reply)
            if is_handed_off:
                print(f"✅ [STEP 5] Hand-off Triggered! Instant Alert sent to Manish ({MANISH_PHONE_NUMBER}) for '{lead['name']}'.")
            
            print("="*66)

if __name__ == "__main__":
    run_agency_automation(test_mode=True)
