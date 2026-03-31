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


user_id = input("Enter Roblox User ID: ")

user = get_user_info(user_id)

if not user:
    print("User not found.")
    exit()

print("\n=== USER INFO ===")
print(f"Username: {user['name']}")
print(f"Display Name: {user['displayName']}")
print(f"Created: {user['created']}")
print(f"Account Age: {calculate_age(user['created'])} days")

print("\n=== BADGES (sample) ===")
badges = get_badges(user_id)

if badges and "data" in badges:
    for b in badges["data"][:5]:
        print(f"- {b['name']} (ID: {b['id']})")
else:
    print("No badges or private.")

print("\n=== INVENTORY (sample) ===")
inv = get_inventory(user_id)

if inv and "data" in inv:
    for item in inv["data"][:5]:
        print(f"- {item['name']} (ID: {item['assetId']})")
else:
    print("Inventory private or empty.")

badge_check = input("\nCheck specific badge ID (or Enter to skip): ")
if badge_check:
    result = check_badge(user_id, badge_check)
    print("Badge check result:", result)

item_check = input("Check specific asset ID (or Enter to skip): ")
if item_check:
    result = check_item(user_id, item_check)
    print("Item check result:", result)