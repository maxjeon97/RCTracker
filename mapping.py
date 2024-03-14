import os
import requests
from dotenv import load_dotenv

load_dotenv()

MAPQUEST_API_KEY = os.environ.get('MAPQUEST_API_KEY')


def get_map_url(address, city, state):
    """Get MapQuest URL for a static map for this location."""

    base = f"https://www.mapquestapi.com/staticmap/v5/map?key={MAPQUEST_API_KEY}"
    where = f"{address},{city},{state}"
    return f"{base}&center={where}&size=@2x&zoom=15&locations={where}"


def save_map(id, address, city, state):
    """Get static map and save in static/maps directory of this app."""

    path = os.path.join(os.path.abspath(
        os.path.dirname(__file__)), f'static/maps/{id}.jpg')

    url = get_map_url(address, city, state)

    response = requests.get(url)

    if response.status_code == 200:
        with open(path, 'wb') as file:
            file.write(response.content)


def delete_map_secure(id):
    """Delete a map image securely from the static/maps directory of this app."""

    path = os.path.join(os.path.abspath(
        os.path.dirname(__file__)), f"static/maps/{id}.jpg")

    try:
        if os.path.exists(path):
            os.remove(path)

    except Exception as e:
        print(f"An error occurred: {e}")
