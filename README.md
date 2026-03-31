# ROBLOSINT

Roblox OSINT tool. Fetches user data, badges, inventory, friends, followers, and followings. Outputs to TXT and JSON so you can compare accounts and figure out if someone's an alt.

## Install

```bash
pip install requests
```

## Usage

```bash
python main.py
```

Enter a Roblox User ID when prompted. You'll get two files:
- `{username}.txt` - human readable
- `{username}.json` - for your scripts

## What it gets

- User info (username, display name, account age, created date)
- All badges
- Inventory/collectibles
- Friends (names resolved)
- Followers (IDs)
- Followings (IDs)

## JSON format

```json
{
  "userId": 123456,
  "username": "someguy",
  "displayName": "SomeGuy",
  "created": "2020-01-01T00:00:00Z",
  "accountAge": 1000,
  "badges": [{"id": 1, "name": "Badge Name"}],
  "inventory": [{"assetId": 1, "name": "Item Name"}],
  "friends": [{"userId": 111, "username": "friend1", "displayName": "Friend1"}],
  "followers": [222, 333, 444],
  "followings": [555, 777]
}
```

## Code example for doing shit with the .json it generates

```python
import json

with open("user1.json") as f:
    user1 = json.load(f)

with open("user2.json") as f:
    user2 = json.load(f)

# Check common badges
badges1 = set(b["id"] for b in user1["badges"])
badges2 = set(b["id"] for b in user2["badges"])
common = badges1 & badges2

# Check common friends
friends1 = set(f["userId"] for f in user1["friends"])
friends2 = set(f["userId"] for f in user2["friends"])
common_friends = friends1 & friends2

print(f"Common badges: {len(common)}")
print(f"Common friends: {len(common_friends)}")
```

## Notes

- Friend names are resolved in batches of 32 to avoid getting rate limited
- Followers/followings are just IDs
- No authentication needed. Thanks God Roblox API is wide open for reading public data
