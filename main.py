import requests
from datetime import datetime

BASE_HEADERS = {"User-Agent": "Roblox/WinInet"}

def get_user_info(user_id):
    url = f"https://users.roblox.com/v1/users/{user_id}"
    r = requests.get(url, headers=BASE_HEADERS)
    return r.json() if r.status_code == 200 else None

def get_badges(user_id):
    url = f"https://badges.roblox.com/v1/users/{user_id}/badges?limit=10"
    r = requests.get(url, headers=BASE_HEADERS)
    return r.json() if r.status_code == 200 else None

def check_badge(user_id, badge_id):
    url = f"https://badges.roblox.com/v1/users/{user_id}/badges/awarded-dates?badgeIds={badge_id}"
    r = requests.get(url, headers=BASE_HEADERS)
    return r.json()

def get_inventory(user_id):
    url = f"https://inventory.roblox.com/v1/users/{user_id}/assets/collectibles?limit=10"
    r = requests.get(url, headers=BASE_HEADERS)
    return r.json() if r.status_code == 200 else None

def check_item(user_id, asset_id):
    url = f"https://inventory.roblox.com/v1/users/{user_id}/items/Asset/{asset_id}"
    r = requests.get(url, headers=BASE_HEADERS)
    return r.json()

def calculate_age(created):
    created_date = datetime.fromisoformat(created.replace("Z", ""))
    return (datetime.utcnow() - created_date).days

