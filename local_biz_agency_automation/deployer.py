"""
Deployer & GitHub API Publisher Module (Zero External Dependencies)
Uses standard urllib to publish custom demo sites to GitHub Pages.
"""
import os
import json
import base64
import urllib.request
import urllib.error
import logging
from config import GITHUB_USERNAME, GITHUB_TOKEN, GITHUB_REPO

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class Publisher:
    def __init__(self, username=GITHUB_USERNAME, token=GITHUB_TOKEN, repo=GITHUB_REPO):
        self.username = username or GITHUB_USERNAME
        self.token = token or GITHUB_TOKEN
        self.repo = repo or GITHUB_REPO
        self._ensure_repo_exists()

    def _make_github_request(self, url, method="GET", payload=None):
        headers = {
            "Authorization": f"token {self.token}",
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "Python-Agency-App"
        }
        data_bytes = None
        if payload is not None:
            data_bytes = json.dumps(payload).encode("utf-8")
            headers["Content-Type"] = "application/json"

        req = urllib.request.Request(url, data=data_bytes, headers=headers, method=method)
        try:
            with urllib.request.urlopen(req) as res:
                body = res.read().decode("utf-8")
                return res.status, json.loads(body) if body else {}
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8")
            return e.code, json.loads(body) if body else {}
        except Exception as e:
            return 500, {"error": str(e)}

    def _ensure_repo_exists(self):
        if not self.token or not self.username:
            return

        check_url = f"https://api.github.com/repos/{self.username}/{self.repo}"
        status, res = self._make_github_request(check_url, method="GET")

        if status == 404:
            logging.info(f"📁 Repository '{self.repo}' not found. Auto-creating on GitHub...")
            create_url = "https://api.github.com/user/repos"
            payload = {
                "name": self.repo,
                "description": "Auto-generated local business demo websites",
                "private": False,
                "auto_init": True
            }
            c_status, c_res = self._make_github_request(create_url, method="POST", payload=payload)
            if c_status == 201:
                logging.info(f"✅ Repository '{self.repo}' created!")
                self._enable_github_pages()

    def _enable_github_pages(self):
        url = f"https://api.github.com/repos/{self.username}/{self.repo}/pages"
        payload = {"source": {"branch": "main", "path": "/"}}
        self._make_github_request(url, method="POST", payload=payload)

    def publish_to_github(self, slug, local_filepath):
        if not self.token or not self.username:
            return f"https://demo.github.io/{self.repo}/{slug}/"

        with open(local_filepath, "r", encoding="utf-8") as f:
            content = f.read()

        b64_content = base64.b64encode(content.encode("utf-8")).decode("utf-8")
        path_in_repo = f"{slug}/index.html"
        url = f"https://api.github.com/repos/{self.username}/{self.repo}/contents/{path_in_repo}"

        # Get SHA if exists
        g_status, g_res = self._make_github_request(url, method="GET")
        sha = g_res.get("sha") if g_status == 200 else None

        payload = {
            "message": f"Auto-generated demo website for {slug}",
            "content": b64_content
        }
        if sha:
            payload["sha"] = sha

        p_status, p_res = self._make_github_request(url, method="PUT", payload=payload)
        if p_status in [200, 201]:
            live_url = f"https://{self.username}.github.io/{self.repo}/{slug}/"
            logging.info(f"✅ Published live demo website to GitHub: {live_url}")
            return live_url
        else:
            logging.error(f"❌ Failed to publish to GitHub: {p_status} - {p_res}")
            return f"https://{self.username}.github.io/{self.repo}/{slug}/"

    def get_live_demo_url(self, slug, local_filepath):
        return self.publish_to_github(slug, local_filepath)

if __name__ == "__main__":
    pub = Publisher()
    print(f"Publisher ready for user: {pub.username}")
