import requests
from environs import Env

env = Env()
env.read_env()

API_KEY = env("WEATHERAPI")



def get_data(place, forecast_days):
    url = "https://api.openweathermap.org/data/2.5/" \
          f"forecast?q={place}&" \
          f"appid={API_KEY}"
    response = requests.get(url)
    data = response.json()
    filtered_data = data['list']
    num_values = 8 * forecast_days
    filtered_data = filtered_data[:num_values]
    return filtered_data


if __name__ == "__main__":
    print(get_data(place="Denver", forecast_days=3))
