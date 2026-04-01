import requests
import json
import time
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

def get_badge_award_dates(user_id, badge_ids):
    if not badge_ids:
        return {}
    award_dates = {}
    total = len(badge_ids)
    print(f"[BADGE DATES] Fetching award dates for {total} badges...")
    for i in range(0, len(badge_ids), 50):
        batch = badge_ids[i:i+50]
        url = f"https://badges.roblox.com/v1/users/{user_id}/badges/awarded-dates?badgeIds={','.join(map(str, batch))}"
        print(f"[BADGE DATES] Requesting badges {i} to {i+len(batch)} of {total}...")
        
        max_retries = 5
        for attempt in range(max_retries):
            r = requests.get(url, headers=BASE_HEADERS)
            if r.status_code == 200:
                time.sleep(2)
                break
            elif r.status_code == 429:
                wait_time = ((attempt + 1) * 2) + 5
                print(f"[BADGE DATES] Rate limited! Waiting {wait_time}s before retry...")
                time.sleep(wait_time)
            else:
                print(f"[BADGE DATES] Error {r.status_code} for batch starting at {i}")
                break
        
        if r.status_code != 200:
            print(f"[BADGE DATES] Failed after {max_retries} retries for batch starting at {i}")
            continue
            
        data = r.json()
        count = len(data.get("data", []))
        print(f"[BADGE DATES] Got {count} award dates in this batch")
        for item in data.get("data", []):
            award_dates[item["badgeId"]] = item.get("awardedDate")
        time.sleep(1.5)
    print(f"[BADGE DATES] Done. Got {len(award_dates)} award dates total")
    return award_dates

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

def get_groups(user_id):
    url = f"https://groups.roblox.com/v2/users/{user_id}/groups/roles"
    r = requests.get(url, headers=BASE_HEADERS)
    if r.status_code == 200:
        data = r.json()
        return {"data": data.get("data", [])} if data.get("data") else {"data": []}
    return {"data": []}

def resolve_users(user_ids):
    if not user_ids:
        return []
    resolved = []
    for i in range(0, len(user_ids), 32):
        batch = user_ids[i:i+32]
        url = "https://users.roblox.com/v1/users"
        r = requests.post(url, headers=BASE_HEADERS, json={"userIds": batch})
        if r.status_code == 200:
            resolved.extend(r.json().get("data", []))
    return resolved

def calculate_age(created):
    created_date = datetime.fromisoformat(created.replace("Z", ""))
    return (datetime.utcnow() - created_date).days


def build_user_data(user_id):
    print("[STATUS] Loading user info...")
    user = get_user_info(user_id)
    print("[STATUS] Loading badges...")
    badges = get_badges(user_id)
    print("[STATUS] Loading inventory...")
    inv = get_inventory(user_id)
    print("[STATUS] Loading friends...")
    friends = get_friends(user_id)
    print("[STATUS] Loading followers...")
    followers = get_followers(user_id)
    print("[STATUS] Loading followings...")
    followings = get_followings(user_id)
    print("[STATUS] Loading groups...")
    groups = get_groups(user_id)

    friend_ids = [f["id"] for f in friends.get("data", [])]
    follower_ids = [fol["id"] for fol in followers.get("data", [])]
    following_ids = [fing["id"] for fing in followings.get("data", [])]

    print("[STATUS] Resolving friend usernames...")
    resolved = {u["id"]: u for u in resolve_users(friend_ids)}

    badge_ids = [b["id"] for b in badges.get("data", [])]
    print("[STATUS] Fetching badge award dates...")
    award_dates = get_badge_award_dates(user_id, badge_ids)

    print("[STATUS] Building final output...")

    return {
        "userId": user_id,
        "username": user.get("name") if user else None,
        "displayName": user.get("displayName") if user else None,
        "created": user.get("created") if user else None,
        "accountAge": calculate_age(user.get("created")) if user and user.get("created") else None,
        "badges": [{"id": b["id"], "name": b["name"], "placeId": b.get("awarder", {}).get("id"), "creatorId": b.get("creator", {}).get("id"), "creatorName": b.get("creator", {}).get("name"), "awardedDate": award_dates.get(b["id"])} for b in badges.get("data", [])] if badges else [],
        "inventory": [{"assetId": item["assetId"], "name": item["name"]} for item in inv.get("data", [])] if inv else [],
        "friends": [{"userId": f["id"], "username": resolved.get(f["id"], {}).get("name", ""), "displayName": resolved.get(f["id"], {}).get("displayName", "")} for f in friends.get("data", [])],
        "followers": [fo["id"] for fo in followers.get("data", [])],
        "followings": [fing["id"] for fing in followings.get("data", [])],
        "groups": [{"groupId": g["group"]["id"], "groupName": g["group"]["name"], "roleName": g["role"]["name"], "rank": g["role"]["rank"]} for g in groups.get("data", [])]
    }


user_id = input("Enter Roblox User ID: ")

data = build_user_data(user_id)

print("[STATUS] Done!")

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
            f.write(f"- ID: {fo}\n")
    else:
        f.write("No followers or private.\n")

    f.write("\n=== FOLLOWINGS ===\n")
    if data["followings"]:
        for fing in data["followings"]:
            f.write(f"- ID: {fing}\n")
    else:
        f.write("No followings or private.\n")

    f.write("\n=== GROUPS ===\n")
    if data["groups"]:
        for g in data["groups"]:
            f.write(f"- {g['groupName']} | {g['roleName']} (Rank: {g['rank']}) (ID: {g['groupId']})\n")
    else:
        f.write("No groups.\n")

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
        print(f"- ID: {fo}")
else:
    print("No followers or private.")

print("\n=== FOLLOWINGS ===")
if data["followings"]:
    for fing in data["followings"]:
        print(f"- ID: {fing}")
else:
    print("No followings or private.")

print("\n=== GROUPS ===")
if data["groups"]:
    for g in data["groups"]:
        print(f"- {g['groupName']} | {g['roleName']} (Rank: {g['rank']}) (ID: {g['groupId']})")
else:
    print("No groups.")

badge_check = input("\nCheck specific badge ID (or Enter to skip): ")
if badge_check:
    result = check_badge(user_id, badge_check)
    print("Badge check result:", result)

item_check = input("Check specific asset ID (or Enter to skip): ")
if item_check:
    result = check_item(user_id, item_check)
    print("Item check result:", result)