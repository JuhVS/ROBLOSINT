import requests
import json
from datetime import datetime

BASE_HEADERS = {"User-Agent": "Roblox/WinInet"}

def get_user_info(user_id):
    url = f"https://users.roblox.com/v1/users/{user_id}"
    r = requests.get(url, headers=BASE_HEADERS)
    return r.json() if r.status_code == 200 else None

def get_badges(user_id):
    all_badges = []
    cursor = None
    while True:
        url = f"https://badges.roblox.com/v1/users/{user_id}/badges?limit=100&sortOrder=Asc"
        if cursor:
            url += f"&cursor={cursor}"
        r = requests.get(url, headers=BASE_HEADERS)
        data = r.json() if r.status_code == 200 else None
        if not data or "data" not in data:
            break
        all_badges.extend(data["data"])
        cursor = data.get("nextPageCursor")
        if not cursor:
            break
    return {"data": all_badges} if all_badges else {"data": []}

def check_badge(user_id, badge_id):
    url = f"https://badges.roblox.com/v1/users/{user_id}/badges/awarded-dates?badgeIds={badge_id}"
    r = requests.get(url, headers=BASE_HEADERS)
    return r.json()

def get_inventory(user_id):
    all_items = []
    cursor = None
    while True:
        url = f"https://inventory.roblox.com/v1/users/{user_id}/assets/collectibles?limit=100"
        if cursor:
            url += f"&cursor={cursor}"
        r = requests.get(url, headers=BASE_HEADERS)
        data = r.json() if r.status_code == 200 else None
        if not data or "data" not in data:
            break
        all_items.extend(data["data"])
        cursor = data.get("nextPageCursor")
        if not cursor:
            break
    return {"data": all_items} if all_items else {"data": []}

def check_item(user_id, asset_id):
    url = f"https://inventory.roblox.com/v1/users/{user_id}/items/Asset/{asset_id}"
    r = requests.get(url, headers=BASE_HEADERS)
    return r.json()

def calculate_age(created):
    created_date = datetime.fromisoformat(created.replace("Z", ""))
    return (datetime.utcnow() - created_date).days


def build_user_data(user_id):
    user = get_user_info(user_id)
    badges = get_badges(user_id)
    inv = get_inventory(user_id)

    return {
        "userId": user_id,
        "username": user.get("name") if user else None,
        "displayName": user.get("displayName") if user else None,
        "created": user.get("created") if user else None,
        "accountAge": calculate_age(user.get("created")) if user and user.get("created") else None,
        "badges": badges.get("data", []) if badges else [],
        "inventory": inv.get("data", []) if inv else []
    }


user_id = input("Enter Roblox User ID: ")

user = get_user_info(user_id)

if not user:
    print("User not found.")
    exit()

filename = f"{user['name']}.txt"
json_filename = f"{user['name']}.json"

data = build_user_data(user_id)

with open(json_filename, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)

with open(filename, "w", encoding="utf-8") as f:
    f.write("=== USER INFO ===\n")
    f.write(f"Username: {user['name']}\n")
    f.write(f"Display Name: {user['displayName']}\n")
    f.write(f"Created: {user['created']}\n")
    f.write(f"Account Age: {calculate_age(user['created'])} days\n")

    f.write("\n=== BADGES ===\n")
    if data["badges"]:
        for b in data["badges"]:
            f.write(f"- {b['name']} (ID: {b['id']})\n")
    else:
        f.write("No badges or private.\n")

    f.write("\n=== INVENTORY ===\n")
    if data["inventory"]:
        for item in data["inventory"]:
            f.write(f"- {item['name']} (ID: {item['assetId']})\n")
    else:
        f.write("Inventory private or empty.\n")

print(f"\nResults saved to {filename} and {json_filename}")

print("\n=== USER INFO ===")
print(f"Username: {data['username']}")
print(f"Display Name: {data['displayName']}")
print(f"Created: {data['created']}")
print(f"Account Age: {data['accountAge']} days")

print("\n=== BADGES ===")
if data["badges"]:
    for b in data["badges"]:
        print(f"- {b['name']} (ID: {b['id']})")
else:
    print("No badges or private.")

print("\n=== INVENTORY ===")
if data["inventory"]:
    for item in data["inventory"]:
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