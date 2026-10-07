"""
Web Control Dashboard & ON/OFF Switch Server
Provides a browser interface to turn automation ON/OFF, set active hours (10 AM - 6 PM), and view Hot Leads.
"""
import os
import json
import time
import datetime
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from config import MANISH_PHONE_NUMBER

STATUS_FILE = os.path.join(os.path.dirname(__file__), "status.json")

def load_status():
    if os.path.exists(STATUS_FILE):
        try:
            with open(STATUS_FILE, "r") as f:
                return json.load(f)
        except Exception:
            pass
    return {
        "is_running": True,
        "start_hour": 10,
        "end_hour": 18,
        "total_scraped": 0,
        "sites_published": 0,
        "pitches_sent": 0,
        "hot_leads": 0
    }

def save_status(data):
    with open(STATUS_FILE, "w") as f:
        json.dump(data, f, indent=2)

class DashboardHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/api/status":
            status = load_status()
            now = datetime.datetime.now()
            current_hour = now.hour
            
            # Check time window (10 AM to 6 PM)
            within_hours = (status["start_hour"] <= current_hour < status["end_hour"])
            active = status["is_running"] and within_hours

            status["current_time"] = now.strftime("%I:%M %p")
            status["within_hours"] = within_hours
            status["active_status"] = "🟢 RUNNING" if active else ("🟡 PAUSED (OUTSIDE HOURS)" if not within_hours else "🔴 TURNED OFF")

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(status).encode("utf-8"))
            return

        # Render HTML UI
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        
        status = load_status()
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Agency Automation Control Center</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
</head>
<body class="bg-slate-900 text-slate-100 min-h-screen p-6 font-sans">

    <div class="max-w-4xl mx-auto space-y-6">
        <!-- Header -->
        <div class="flex justify-between items-center bg-slate-800 p-6 rounded-2xl border border-slate-700 shadow-xl">
            <div>
                <h1 class="text-2xl font-bold flex items-center gap-3 text-sky-400">
                    <i class="fa-solid fa-robot text-3xl"></i> Local Biz Lead Engine
                </h1>
                <p class="text-sm text-slate-400 mt-1">Configured for Manish ({MANISH_PHONE_NUMBER})</p>
            </div>
            <div id="statusBadge" class="px-4 py-2 rounded-full font-bold text-sm bg-emerald-500/20 text-emerald-400 border border-emerald-500/30">
                Checking Status...
            </div>
        </div>

        <!-- ON/OFF Switch & Working Hours -->
        <div class="grid md:grid-cols-2 gap-6">
            <!-- Toggle Switch Card -->
            <div class="bg-slate-800 p-6 rounded-2xl border border-slate-700 shadow-xl space-y-4">
                <h2 class="text-lg font-semibold text-slate-200 flex items-center gap-2">
                    <i class="fa-solid fa-power-off text-amber-400"></i> Master Power Switch
                </h2>
                <div class="flex items-center justify-between bg-slate-900 p-4 rounded-xl border border-slate-800">
                    <span class="font-bold text-slate-300">Automation Engine Status</span>
                    <button id="toggleBtn" onclick="toggleEngine()" class="px-6 py-2.5 rounded-xl font-bold text-white transition shadow-lg bg-emerald-600 hover:bg-emerald-500">
                        TURN ON
                    </button>
                </div>
            </div>

            <!-- Time Window Settings -->
            <div class="bg-slate-800 p-6 rounded-2xl border border-slate-700 shadow-xl space-y-4">
                <h2 class="text-lg font-semibold text-slate-200 flex items-center gap-2">
                    <i class="fa-solid fa-clock text-sky-400"></i> Active Hours (Default: 10 AM - 6 PM)
                </h2>
                <div class="grid grid-cols-2 gap-3 text-sm">
                    <div class="bg-slate-900 p-3 rounded-xl border border-slate-800 text-center">
                        <span class="text-xs text-slate-400 block mb-1">Start Time</span>
                        <span class="font-bold text-sky-400 text-lg">10:00 AM</span>
                    </div>
                    <div class="bg-slate-900 p-3 rounded-xl border border-slate-800 text-center">
                        <span class="text-xs text-slate-400 block mb-1">End Time</span>
                        <span class="font-bold text-sky-400 text-lg">06:00 PM</span>
                    </div>
                </div>
                <p class="text-xs text-slate-400 italic">Outside 10 AM - 6 PM, outreach automatically pauses to prevent late-night messages.</p>
            </div>
        </div>

        <!-- Live Metrics Grid -->
        <div class="grid grid-cols-2 sm:grid-cols-4 gap-4">
            <div class="bg-slate-800 p-4 rounded-xl border border-slate-700 text-center">
                <span class="text-2xl font-bold text-slate-100" id="statScraped">0</span>
                <span class="text-xs text-slate-400 block mt-1">Leads Scraped</span>
            </div>
            <div class="bg-slate-800 p-4 rounded-xl border border-slate-700 text-center">
                <span class="text-2xl font-bold text-sky-400" id="statSites">0</span>
                <span class="text-xs text-slate-400 block mt-1">Demo Sites Live</span>
            </div>
            <div class="bg-slate-800 p-4 rounded-xl border border-slate-700 text-center">
                <span class="text-2xl font-bold text-indigo-400" id="statPitches">0</span>
                <span class="text-xs text-slate-400 block mt-1">Pitches Sent</span>
            </div>
            <div class="bg-slate-800 p-4 rounded-xl border border-slate-700 text-center">
                <span class="text-2xl font-bold text-emerald-400" id="statHotLeads">0</span>
                <span class="text-xs text-slate-400 block mt-1">Hot Leads Handed Off</span>
            </div>
        </div>
    </div>

    <script>
        async function fetchStatus() {{
            try {{
                const res = await fetch('/api/status');
                const data = await res.json();
                
                document.getElementById('statusBadge').innerText = data.active_status;
                document.getElementById('statScraped').innerText = data.total_scraped;
                document.getElementById('statSites').innerText = data.sites_published;
                document.getElementById('statPitches').innerText = data.pitches_sent;
                document.getElementById('statHotLeads').innerText = data.hot_leads;

                const btn = document.getElementById('toggleBtn');
                if (data.is_running) {{
                    btn.innerText = 'POWER OFF';
                    btn.className = 'px-6 py-2.5 rounded-xl font-bold text-white transition shadow-lg bg-rose-600 hover:bg-rose-500';
                }} else {{
                    btn.innerText = 'POWER ON';
                    btn.className = 'px-6 py-2.5 rounded-xl font-bold text-white transition shadow-lg bg-emerald-600 hover:bg-emerald-500';
                }}
            }} catch(e) {{
                console.error(e);
            }}
        }}

        async function toggleEngine() {{
            const res = await fetch('/api/toggle', {{ method: 'POST' }});
            fetchStatus();
        }}

        fetchStatus();
        setInterval(fetchStatus, 3000);
    </script>
</body>
</html>"""
        self.wfile.write(html.encode("utf-8"))

    def do_POST(self):
        if self.path == "/api/toggle":
            status = load_status()
            status["is_running"] = not status["is_running"]
            save_status(status)
            
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"success": True, "is_running": status["is_running"]}).encode("utf-8"))

def run_dashboard_server(port=5000):
    server = HTTPServer(('0.0.0.0', port), DashboardHandler)
    print(f"🌐 Dashboard Control Panel live at: http://localhost:{port}")
    server.serve_forever()

if __name__ == "__main__":
    run_dashboard_server()
