"""
Google Maps Lead Scraper & Filter Engine
Searches for target businesses and isolates leads with MISSING or INVALID websites.
"""
import requests
import json
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class LeadScraper:
    def __init__(self, api_key=None):
        self.api_key = api_key

    def is_valid_website(self, website_url):
        """
        Check if business has a proper website vs missing or just Facebook/Instagram link.
        """
        if not website_url or website_url.strip() == "":
            return False
        
        # Social media links often mean they lack a real website
        social_domains = ["facebook.com", "instagram.com", "wa.me", "justdial.com", "indiamart.com"]
        for domain in social_domains:
            if domain in website_url.lower():
                return False
                
        return True

    def find_no_website_leads(self, category, city):
        """
        Fetch leads from Google Places / Maps and filter out businesses without a dedicated website.
        """
        logging.info(f"🔍 Searching for '{category}' in '{city}'...")
        query = f"{category} in {city}"
        
        # Sample structured output representation
        # Can connect to Google Places API (TextSearch / NearbySearch) or Open Street Maps / Custom Web Scraper
        leads = []
        
        # Simulated structure for demonstration & testing
        # When Google Places API key is provided, calls API endpoint:
        if self.api_key:
            url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query={query}&key={self.api_key}"
            response = requests.get(url).json()
            results = response.get("results", [])
            for place in results:
                place_id = place.get("place_id")
                # Fetch detailed info
                detail_url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&fields=name,formatted_phone_number,website,rating,user_ratings_total,formatted_address&key={self.api_key}"
                detail_res = requests.get(detail_url).json().get("result", {})
                
                website = detail_res.get("website", "")
                if not self.is_valid_website(website):
                    leads.append({
                        "name": detail_res.get("name"),
                        "phone": detail_res.get("formatted_phone_number"),
                        "address": detail_res.get("formatted_address"),
                        "rating": detail_res.get("rating"),
                        "reviews": detail_res.get("user_ratings_total"),
                        "city": city,
                        "category": category,
                        "has_website": False,
                        "existing_url": website
                    })
        else:
            logging.info("ℹ️ Using fallback Lead Parser (Pass Google Places API Key or run local browser scraper for production data).")
            
        return leads

if __name__ == "__main__":
    scraper = LeadScraper()
    print("LeadScraper Engine ready.")
