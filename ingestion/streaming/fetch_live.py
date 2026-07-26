import requests

def fetch_latest_session():
    """Grab the most recent F1 session (race, practice, qualifying) to inspect its shape."""
    url = "https://api.openf1.org/v1/sessions?session_key=latest"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def fetch_car_data(session_key: int, driver_number: int):
    url = f"https://api.openf1.org/v1/car_data?session_key={session_key}&driver_number={driver_number}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

if __name__ == "__main__":
    session = fetch_latest_session()
    print(session)