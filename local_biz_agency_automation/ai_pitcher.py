"""
Enhanced AI Pitch & Offer Generator
Includes Market Gap, Future Scope, and Live Demo Website Link customized for the business.
"""

class PitchGenerator:
    @staticmethod
    def generate_pitch(lead_info, demo_url):
        name = lead_info.get("name", "Sir/Ma'am")
        city = lead_info.get("city", "City")
        category = lead_info.get("category", "Business")
        rating = lead_info.get("rating", 4.8)
        reviews = lead_info.get("reviews", 35)
        phone = lead_info.get("phone", "")

        pitch = f"""Namaste {name} ji 🙏

Aapka {category} {city} mein Google par kaafi accha perform kar raha hai (⭐ {rating}/5 - {reviews}+ Google Reviews)!

⚠️ **Market Gap & Problem:**
Aaj 75% naye buyers kisi bhi showroom jaane se pehle Google par models, price list aur phone number search karte hain. Official Website na hone ki wajah se aapki 30-40% direct leads aur high-paying customers competitors ke paas chale jaate hain.

🚀 **Future Scope:**
Ek modern digital website hone se aap:
1️⃣ Direct Google search se 2x-3x inquiries generate kar sakte hain.
2️⃣ WhatsApp & Direct Call Buttons se Instant customer booking le sakte hain.
3️⃣ Customers ka trust build hota hai aur competitor se aage rehte hain.

🎁 **Humne Aapke Showroom Ke Liye Ek Custom Live Demo Website Ready Ki Hai:**
Maine aapke Google Maps number ({phone}) aur details ke sath ek Sample Website banayi hai, jisme Direct Call aur WhatsApp Button active hai:

👉 **Aapki Live Demo Website Check Karein:**
🔗 {demo_url}

Agar aapko yeh design passand aaya aur ise apne domain par 2 din mein start karwana chahte hain, toh 'YES' ya 'CALL' likhkar reply karein! 😊"""
        return pitch

if __name__ == "__main__":
    test_lead = {
        "name": "GreenVolt EV Motors",
        "city": "Lucknow",
        "category": "EV Showroom",
        "rating": 4.9,
        "reviews": 56,
        "phone": "+91 9876543210"
    }
    demo_link = "https://manish-agency.github.io/demo-preview/greenvolt_ev_motors/"
    print(PitchGenerator.generate_pitch(test_lead, demo_link))
