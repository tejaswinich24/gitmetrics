import requests
from config import GITHUB_TOKEN

BASE_URL = "https://api.github.com"
HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json"
}

def get_user_profile(username):
    resp = requests.get(f"{BASE_URL}/users/{username}", headers=HEADERS, timeout=10)
    resp.raise_for_status()
    return resp.json()

def get_user_repos(username):
    resp = requests.get(
        f"{BASE_URL}/users/{username}/repos",
        headers=HEADERS,
        params={"sort": "updated", "per_page": 15},
        timeout=10
    )
    resp.raise_for_status()
    return resp.json()

def get_repo_languages(owner, repo):
    resp = requests.get(f"{BASE_URL}/repos/{owner}/{repo}/languages", headers=HEADERS, timeout=10)
    resp.raise_for_status()
    return resp.json()

def get_user_events(username):
    resp = requests.get(f"{BASE_URL}/users/{username}/events/public", headers=HEADERS, timeout=10)
    resp.raise_for_status()
    return resp.json()