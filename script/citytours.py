import json

input_file_path = "temp/input/citytours_data.json"
output_file_path = "src/profile/city_tour.json"

try:
    with open(input_file_path, "r", encoding="utf-8") as data_file:
        data = json.load(data_file)

    citytours_list = [tour for tour in data.get("cityTours", []) if tour]

    gauntlets = data.get("gauntlets", [])
    active_gauntlet = None

    if gauntlets:
        g = gauntlets[0]

        active_gauntlet = {
            "id": g.get("id"),
            "tiers": [
                {
                    "claimed": True,
                    "goal": tier.get("tokensRequired", 0),
                    "reward": {
                        "reward": {
                            "type": (
                                tier["reward"]["reward"]["type"]
                                if "type" in tier["reward"]["reward"]
                                else "Currency"
                            ),
                            "id": tier["reward"]["reward"]["id"],
                            "value": tier["reward"]["reward"]["value"],
                        }
                    },
                }
                for tier in g.get("tiers", [])
            ],
            "endDate": "2026-05-18T00:00:00Z",
            "startDate": "2026-05-17T16:11:00Z",
            "hasSeenInfo": True,
        }

    final_data = {
        "lastSaved": "1970-01-01T00:00:00Z",
        "cityTourInstances": {},
        "completedCityTours": citytours_list,
        "activeGauntletInstance": active_gauntlet if active_gauntlet else {},
        "completedGauntlets": [],
    }

    output_data = {"version": 1, "data": final_data}

    with open(output_file_path, "w", encoding="utf-8") as f:
        json.dump(output_data, f, indent=2)

except IOError as e:
    print(f"Error opening or accessing {input_file_path}: {e}")

except json.JSONDecodeError as e:
    print(f"Error decoding JSON from {input_file_path}: {e}")
