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

filename = f"{user['name']}.txt"

badges = get_badges(user_id)
inv = get_inventory(user_id)

with open(filename, "w", encoding="utf-8") as f:
    f.write("=== USER INFO ===\n")
    f.write(f"Username: {user['name']}\n")
    f.write(f"Display Name: {user['displayName']}\n")
    f.write(f"Created: {user['created']}\n")
    f.write(f"Account Age: {calculate_age(user['created'])} days\n")

    f.write("\n=== BADGES (sample) ===\n")
    if badges and "data" in badges:
        for b in badges["data"][:5]:
            f.write(f"- {b['name']} (ID: {b['id']})\n")
    else:
        f.write("No badges or private.\n")

    f.write("\n=== INVENTORY (sample) ===\n")
    if inv and "data" in inv:
        for item in inv["data"][:5]:
            f.write(f"- {item['name']} (ID: {item['assetId']})\n")
    else:
        f.write("Inventory private or empty.\n")

print(f"\nResults saved to {filename}")

print("\n=== USER INFO ===")
print(f"Username: {user['name']}")
print(f"Display Name: {user['displayName']}")
print(f"Created: {user['created']}")
print(f"Account Age: {calculate_age(user['created'])} days")

print("\n=== BADGES (sample) ===")
if badges and "data" in badges:
    for b in badges["data"][:5]:
        print(f"- {b['name']} (ID: {b['id']})")
else:
    print("No badges or private.")

print("\n=== INVENTORY (sample) ===")
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