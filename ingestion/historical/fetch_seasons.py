import requests
import json

BASE_URL = "https://api.jolpi.ca/ergast/f1"

def fetch_season_results(year: int):
    """Fetch all race results for a given F1 season."""
    url = f"{BASE_URL}/{year}/results.json?limit=1000"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

if __name__ == "__main__":
    data = fetch_season_results(2026)
    races = data["MRData"]["RaceTable"]["Races"]
    print(f"Fetched {len(races)} races for 2024")
    print(json.dumps(races[0], indent=2)[:500])