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

def get_friends(user_id):
    all_friends = []
    cursor = None
    while True:
        url = f"https://friends.roblox.com/v1/users/{user_id}/friends?limit=100"
        if cursor:
            url += f"&cursor={cursor}"
        r = requests.get(url, headers=BASE_HEADERS)
        data = r.json() if r.status_code == 200 else None
        if not data or "data" not in data:
            break
        all_friends.extend(data["data"])
        cursor = data.get("nextPageCursor")
        if not cursor:
            break
    return {"data": all_friends} if all_friends else {"data": []}

def get_followers(user_id):
    all_followers = []
    cursor = None
    while True:
        url = f"https://friends.roblox.com/v1/users/{user_id}/followers?limit=100"
        if cursor:
            url += f"&cursor={cursor}"
        r = requests.get(url, headers=BASE_HEADERS)
        data = r.json() if r.status_code == 200 else None
        if not data or "data" not in data:
            break
        all_followers.extend(data["data"])
        cursor = data.get("nextPageCursor")
        if not cursor:
            break
    return {"data": all_followers} if all_followers else {"data": []}

def get_followings(user_id):
    all_followings = []
    cursor = None
    while True:
        url = f"https://friends.roblox.com/v1/users/{user_id}/followings?limit=100"
        if cursor:
            url += f"&cursor={cursor}"
        r = requests.get(url, headers=BASE_HEADERS)
        data = r.json() if r.status_code == 200 else None
        if not data or "data" not in data:
            break
        all_followings.extend(data["data"])
        cursor = data.get("nextPageCursor")
        if not cursor:
            break
    return {"data": all_followings} if all_followings else {"data": []}

def resolve_users(user_ids):
    if not user_ids:
        return []
    url = "https://users.roblox.com/v1/users"
    r = requests.post(url, headers=BASE_HEADERS, json={"userIds": user_ids})
    if r.status_code == 200:
        return r.json().get("data", [])
    return []

def calculate_age(created):
    created_date = datetime.fromisoformat(created.replace("Z", ""))
    return (datetime.utcnow() - created_date).days


def build_user_data(user_id):
    user = get_user_info(user_id)
    badges = get_badges(user_id)
    inv = get_inventory(user_id)
    friends = get_friends(user_id)
    followers = get_followers(user_id)
    followings = get_followings(user_id)

    friend_ids = [f["id"] for f in friends.get("data", [])]
    follower_ids = [fol["id"] for fol in followers.get("data", [])]
    following_ids = [fing["id"] for fing in followings.get("data", [])]

    all_ids = list(set(friend_ids + follower_ids + following_ids))
    resolved = {u["id"]: u for u in resolve_users(all_ids)}

    return {
        "userId": user_id,
        "username": user.get("name") if user else None,
        "displayName": user.get("displayName") if user else None,
        "created": user.get("created") if user else None,
        "accountAge": calculate_age(user.get("created")) if user and user.get("created") else None,
        "badges": badges.get("data", []) if badges else [],
        "inventory": inv.get("data", []) if inv else [],
        "friends": [{"userId": f["id"], "username": resolved.get(f["id"], {}).get("name", ""), "displayName": resolved.get(f["id"], {}).get("displayName", "")} for f in friends.get("data", [])],
        "followers": [{"userId": fo["id"], "username": resolved.get(fo["id"], {}).get("name", ""), "displayName": resolved.get(fo["id"], {}).get("displayName", "")} for fo in followers.get("data", [])],
        "followings": [{"userId": fing["id"], "username": resolved.get(fing["id"], {}).get("name", ""), "displayName": resolved.get(fing["id"], {}).get("displayName", "")} for fing in followings.get("data", [])]
    }


user_id = input("Enter Roblox User ID: ")

data = build_user_data(user_id)

if not data["username"]:
    print("User not found.")
    exit()

filename = f"{data['username']}.txt"
json_filename = f"{data['username']}.json"

with open(json_filename, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)

with open(filename, "w", encoding="utf-8") as f:
    f.write("=== USER INFO ===\n")
    f.write(f"Username: {data['username']}\n")
    f.write(f"Display Name: {data['displayName']}\n")
    f.write(f"Created: {data['created']}\n")
    f.write(f"Account Age: {data['accountAge']} days\n")

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

    f.write("\n=== FRIENDS ===\n")
    if data["friends"]:
        for fr in data["friends"]:
            f.write(f"- {fr['username'] or fr['userId']} (ID: {fr['userId']})\n")
    else:
        f.write("No friends or private.\n")

    f.write("\n=== FOLLOWERS ===\n")
    if data["followers"]:
        for fo in data["followers"]:
            f.write(f"- {fo['username'] or fo['userId']} (ID: {fo['userId']})\n")
    else:
        f.write("No followers or private.\n")

    f.write("\n=== FOLLOWINGS ===\n")
    if data["followings"]:
        for fing in data["followings"]:
            f.write(f"- {fing['username'] or fing['userId']} (ID: {fing['userId']})\n")
    else:
        f.write("No followings or private.\n")

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

print("\n=== FRIENDS ===")
if data["friends"]:
    for fr in data["friends"]:
        print(f"- {fr['username'] or fr['userId']} (ID: {fr['userId']})")
else:
    print("No friends or private.")

print("\n=== FOLLOWERS ===")
if data["followers"]:
    for fo in data["followers"]:
        print(f"- {fo['username'] or fo['userId']} (ID: {fo['userId']})")
else:
    print("No followers or private.")

print("\n=== FOLLOWINGS ===")
if data["followings"]:
    for fing in data["followings"]:
        print(f"- {fing['username'] or fing['userId']} (ID: {fing['userId']})")
else:
    print("No followings or private.")

badge_check = input("\nCheck specific badge ID (or Enter to skip): ")
if badge_check:
    result = check_badge(user_id, badge_check)
    print("Badge check result:", result)

item_check = input("Check specific asset ID (or Enter to skip): ")
if item_check:
    result = check_item(user_id, item_check)
    print("Item check result:", result)