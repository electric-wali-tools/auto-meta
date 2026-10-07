"""
Outreach & Instant Lead Notification Engine (Zero External Dependencies)
Uses standard urllib to send Telegram alerts.
"""
import json
import urllib.request
import urllib.error
import logging
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, MANISH_PHONE_NUMBER

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class OutreachNotifier:
    def __init__(self, bot_token=TELEGRAM_BOT_TOKEN, chat_id=TELEGRAM_CHAT_ID, owner_phone=MANISH_PHONE_NUMBER):
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.owner_phone = owner_phone

    def send_telegram_alert(self, lead_info, client_reply):
        client_phone = lead_info.get('phone', 'N/A')
        clean_client_phone = ''.join(filter(str.isdigit, str(client_phone)))

        message = f"""🔥 **HOT LEAD ALERT! (Client Wants to Talk)** 🔥

🏢 **Business Name:** {lead_info.get('name')}
📍 **City:** {lead_info.get('city')}
📞 **Client Phone Number:** `{client_phone}`
🏷️ **Category:** {lead_info.get('category')}
⭐ **Rating:** {lead_info.get('rating')} ({lead_info.get('reviews')} reviews)

💬 **Client's Reply:** "{client_reply}"

⚡ **ACTION FOR MANISH ({self.owner_phone}):**
👇 Click below to instantly call or message the client:
📞 **Direct WhatsApp Client Link:** https://wa.me/{clean_client_phone}?text=Namaste%20{lead_info.get('name')}%20ji,%20Aapne%20website%20ke%20liye%20contact%20kiya%20tha.
"""
        logging.info(f"\n=======================================================")
        logging.info(f"🔔 ALERT TRIGGERED FOR MANISH ({self.owner_phone})")
        logging.info(f"📱 Lead Phone: {client_phone}")
        logging.info(f"=======================================================\n")

        if self.bot_token and self.bot_token != "YOUR_TELEGRAM_BOT_TOKEN":
            url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
            payload = {
                "chat_id": self.chat_id,
                "text": message,
                "parse_mode": "Markdown"
            }
            data_bytes = json.dumps(payload).encode("utf-8")
            headers = {"Content-Type": "application/json"}
            req = urllib.request.Request(url, data=data_bytes, headers=headers, method="POST")
            try:
                with urllib.request.urlopen(req) as res:
                    if res.status == 200:
                        logging.info("✅ Instant Telegram Alert delivered to Manish!")
                        return True
            except Exception as e:
                logging.error(f"❌ Telegram alert failed: {e}")

        return True

    def process_incoming_reply(self, lead_info, reply_text):
        positive_keywords = ["yes", "call", "interested", "ha", "haan", "batao", "price", "kitna", "details", "contact", "sample"]
        reply_lower = reply_text.lower()
        if any(keyword in reply_lower for keyword in positive_keywords):
            logging.info(f"🎉 Lead '{lead_info.get('name')}' is INTERESTED! Triggering alert to Manish...")
            self.send_telegram_alert(lead_info, reply_text)
            return True
        return False

if __name__ == "__main__":
    notifier = OutreachNotifier()
    print("OutreachNotifier ready.")
