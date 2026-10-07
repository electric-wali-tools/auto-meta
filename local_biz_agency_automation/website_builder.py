"""
Automated Custom Landing Page Generator
Generates mobile-responsive HTML/CSS landing pages customized with client's Google Maps data.
"""
import os
import re

class WebsiteBuilder:
    @staticmethod
    def clean_phone(phone_str):
        """Extract clean digits for WhatsApp & Tel links (e.g. +919876543210 -> 919876543210)"""
        if not phone_str:
            return "919999999999"
        digits = re.sub(r'\D', '', str(phone_str))
        if len(digits) == 10:
            digits = "91" + digits
        return digits

    @classmethod
    def generate_site_html(cls, lead_info):
        name = lead_info.get("name", "Exclusive Showroom")
        city = lead_info.get("city", "City")
        phone_raw = lead_info.get("phone", "+91 9999999999")
        phone_clean = cls.clean_phone(phone_raw)
        category = lead_info.get("category", "EV Showroom & Dealers")
        address = lead_info.get("address", f"Main Market, {city}")
        rating = lead_info.get("rating", 4.8)
        reviews = lead_info.get("reviews", 45)

        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{name} - Best {category} in {city}</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        .gradient-hero {{ background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0284c7 100%); }}
        .pulse-btn {{ animation: pulse 2s infinite; }}
        @keyframes pulse {{ 0% {{ transform: scale(1); }} 50% {{ transform: scale(1.05); }} 100% {{ transform: scale(1); }} }}
    </style>
</head>
<body class="bg-gray-50 text-gray-800 font-sans">

    <!-- Header Navigation -->
    <header class="bg-white shadow-sm sticky top-0 z-50">
        <div class="max-w-6xl mx-auto px-4 py-3 flex justify-between items-center">
            <div class="font-bold text-xl text-sky-600 flex items-center gap-2">
                <i class="fa-solid fa-bolt text-yellow-500"></i> {name}
            </div>
            <div class="flex gap-2">
                <a href="tel:+{phone_clean}" class="bg-emerald-600 text-white px-3 py-2 rounded-lg font-semibold text-sm flex items-center gap-1 hover:bg-emerald-700 transition">
                    <i class="fa-solid fa-phone"></i> Call Now
                </a>
                <a href="https://wa.me/{phone_clean}?text=Hi%20{name},%20I%20want%20more%20information" target="_blank" class="bg-green-500 text-white px-3 py-2 rounded-lg font-semibold text-sm flex items-center gap-1 hover:bg-green-600 transition">
                    <i class="fa-brands fa-whatsapp text-lg"></i> WhatsApp
                </a>
            </div>
        </div>
    </header>

    <!-- Hero Section -->
    <section class="gradient-hero text-white py-16 px-4">
        <div class="max-w-4xl mx-auto text-center space-y-6">
            <span class="bg-sky-500/20 text-sky-300 border border-sky-400/30 text-xs uppercase px-3 py-1 rounded-full font-bold tracking-wider">
                Authorized {category} • {city}
            </span>
            <h1 class="text-3xl md:text-5xl font-extrabold leading-tight">
                Welcome to <span class="text-sky-400">{name}</span>
            </h1>
            <p class="text-gray-300 text-lg md:text-xl max-w-2xl mx-auto">
                Discover top-quality models, best pricing, and instant test ride bookings in {city}.
            </p>
            
            <!-- Google Review Badge -->
            <div class="inline-flex items-center gap-2 bg-white/10 backdrop-blur-md px-4 py-2 rounded-full border border-white/20 text-yellow-400 font-semibold text-sm">
                <span>⭐ {rating} Rating</span>
                <span class="text-gray-300">({reviews}+ Google Reviews)</span>
            </div>

            <!-- CTA Buttons -->
            <div class="pt-4 flex flex-col sm:flex-row gap-4 justify-center">
                <a href="https://wa.me/{phone_clean}?text=Hi%20{name},%20I%20am%20interested%20in%20buying%20book%20test%20ride" target="_blank" class="pulse-btn bg-green-500 hover:bg-green-600 text-white font-bold py-3.5 px-8 rounded-xl shadow-lg transition flex items-center justify-center gap-2 text-lg">
                    <i class="fa-brands fa-whatsapp text-2xl"></i> Chat on WhatsApp
                </a>
                <a href="tel:+{phone_clean}" class="bg-sky-500 hover:bg-sky-600 text-white font-bold py-3.5 px-8 rounded-xl shadow-lg transition flex items-center justify-center gap-2 text-lg">
                    <i class="fa-solid fa-phone"></i> Call Showroom ({phone_raw})
                </a>
            </div>
        </div>
    </section>

    <!-- Market Advantage Section -->
    <section class="py-12 bg-white px-4">
        <div class="max-w-5xl mx-auto grid md:grid-cols-3 gap-6 text-center">
            <div class="p-6 rounded-2xl bg-gray-50 border border-gray-100 shadow-sm">
                <div class="text-sky-500 text-3xl mb-3"><i class="fa-solid fa-shield-halved"></i></div>
                <h3 class="font-bold text-lg mb-2">100% Guaranteed Quality</h3>
                <p class="text-sm text-gray-600">Official products with factory warranty & doorstep support.</p>
            </div>
            <div class="p-6 rounded-2xl bg-gray-50 border border-gray-100 shadow-sm">
                <div class="text-emerald-500 text-3xl mb-3"><i class="fa-solid fa-bolt"></i></div>
                <h3 class="font-bold text-lg mb-2">Instant Booking & Quotation</h3>
                <p class="text-sm text-gray-600">Get instant quotes directly on WhatsApp within 5 minutes.</p>
            </div>
            <div class="p-6 rounded-2xl bg-gray-50 border border-gray-100 shadow-sm">
                <div class="text-amber-500 text-3xl mb-3"><i class="fa-solid fa-location-dot"></i></div>
                <h3 class="font-bold text-lg mb-2">Prime Location in {city}</h3>
                <p class="text-sm text-gray-600">{address}</p>
            </div>
        </div>
    </section>

    <!-- Footer Sticky Floating Bar -->
    <div class="fixed bottom-0 left-0 right-0 bg-white border-t border-gray-200 p-3 flex gap-3 sm:hidden z-50">
        <a href="tel:+{phone_clean}" class="flex-1 bg-sky-600 text-white py-2.5 rounded-lg text-center font-bold text-sm flex items-center justify-center gap-2">
            <i class="fa-solid fa-phone"></i> Call
        </a>
        <a href="https://wa.me/{phone_clean}?text=Hi" target="_blank" class="flex-1 bg-green-500 text-white py-2.5 rounded-lg text-center font-bold text-sm flex items-center justify-center gap-2">
            <i class="fa-brands fa-whatsapp text-lg"></i> WhatsApp
        </a>
    </div>

</body>
</html>"""
        return html_content

    @classmethod
    def save_demo_website(cls, lead_info, output_dir="generated_sites"):
        """Save HTML file to disk"""
        slug = re.sub(r'[^a-zA-Z0-9]', '_', lead_info.get("name", "lead")).lower()
        client_dir = os.path.join(output_dir, slug)
        os.makedirs(client_dir, exist_ok=True)
        filepath = os.path.join(client_dir, "index.html")

        html_code = cls.generate_site_html(lead_info)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(html_code)
        
        return filepath, slug

if __name__ == "__main__":
    sample = {
        "name": "GreenVolt EV Motors",
        "city": "Lucknow",
        "phone": "+91 9876543210",
        "category": "EV Showroom",
        "address": "Hazratganj, Lucknow",
        "rating": 4.9,
        "reviews": 56
    }
    path, slug = WebsiteBuilder.save_demo_website(sample)
    print(f"Generated demo website at: {path}")
