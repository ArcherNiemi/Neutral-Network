import csv
import random
import time

import requests

# ==========================================
# CONFIG
# ==========================================

TBA_KEY = ""

EVENTS = [
    # Regionals/District Championships
    "2026iacf",
    "2026txcmp1",
    "2026code",
    "2026onosh",
    "2026flor",
    "2026mndu",
    "2026pncmp",
    "2026nyli2",
    "2026mokc",
    "2026utwv",
    "2026orwil",
    "2026ohcl",
    "2026flwp",
    "2026nvlv",
    "2026nyny",
    "2026alhu",
    "2026chcmp",
    "2026cancmp",
    "2026nccmp",

    # Championship Divisions
    "2026mil",
    "2026cur",
    "2026gal",
]

TESTING_MATCHES = 300

TRAINING_FILE = "FRCTrainingData.csv"
TESTING_FILE = "FRCTestingData.csv"

HEADERS = {
    "X-TBA-Auth-Key": TBA_KEY
}


# ==========================================
# API FUNCTIONS
# ==========================================

def get_json(url):
    r = requests.get(url, headers=HEADERS)

    if r.status_code != 200:
        raise Exception(f"Error {r.status_code}: {url}")

    return r.json()


def get_event_oprs(event):
    return get_json(
        f"https://www.thebluealliance.com/api/v3/event/{event}/oprs"
    )["oprs"]


def get_matches(event):
    return get_json(
        f"https://www.thebluealliance.com/api/v3/event/{event}/matches"
    )


# ==========================================
# COLLECT MATCHES
# ==========================================

rows = []

for event in EVENTS:

    print(f"Loading {event}...")

    oprs = get_event_oprs(event)
    matches = get_matches(event)

    for match in matches:

        # Qualification matches only
        if match["comp_level"] != "qm":
            continue

        # Skip unplayed matches
        if match["winning_alliance"] == "":
            continue

        # Skip ties
        if match["winning_alliance"] == "":
            continue

        red = match["alliances"]["red"]["team_keys"]
        blue = match["alliances"]["blue"]["team_keys"]

        if len(red) != 3 or len(blue) != 3:
            continue

        # Convert team numbers to OPRs
        red_oprs = sorted(
            [oprs.get(team, 0.0)/400 for team in red],
            reverse=True
        )

        blue_oprs = sorted(
            [oprs.get(team, 0.0)/400 for team in blue],
            reverse=True
        )

        red_win = 1 if match["winning_alliance"] == "red" else 0
        blue_win = 1 if match["winning_alliance"] == "blue" else 0

        rows.append(
            red_oprs +
            blue_oprs +
            [red_win, blue_win]
        )

    # Small delay so TBA isn't spammed
    time.sleep(0.2)

print(f"\nCollected {len(rows)} qualification matches.")

# ==========================================
# SHUFFLE AND SPLIT
# ==========================================

random.shuffle(rows)

testing_rows = rows[:TESTING_MATCHES]
training_rows = rows[TESTING_MATCHES:]

print(f"Training: {len(training_rows)}")
print(f"Testing : {len(testing_rows)}")

# ==========================================
# SAVE CSVs
# ==========================================

header = [
    "Red 1",
    "Red 2",
    "Red 3",
    "Blue 1",
    "Blue 2",
    "Blue 3",
    "Red Win",
    "Blue Win",
]

with open(TRAINING_FILE, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerows(training_rows)

with open(TESTING_FILE, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerows(testing_rows)

print("\nDone!")
print(f"Training data saved to {TRAINING_FILE}")
print(f"Testing data saved to {TESTING_FILE}")