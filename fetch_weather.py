import requests
import json


def fetch_api_data():

    url = "https://api.open-meteo.com/v1/forecast?latitude=19.4326&longitude=-99.1332&current=temperature_2m,weather_code,wind_speed_10m&hourly=temperature_2m,weather_code&daily=temperature_2m_max,temperature_2m_min,weather_code&timezone=America%2FMexico_City"

    response = requests.get(url)
    response.raise_for_status

    data = response.json()

    hourly_data = []
    for t, temp, code in zip(
        data["hourly"]["time"],
        data["hourly"]["temperature_2m"],
        data["hourly"]["weather_code"],
    ):
        hourly_data.append({"time": t, "temp": temp, "code": code})

    daily_data = []
    for d, tmax, temp_min, code in zip(
        data["daily"]["time"],
        data["daily"]["temperature_2m_max"],
        data["daily"]["temperature_2m_min"],
        data["daily"]["weather_code"],
    ):
        daily_data.append(
            {"date": d, "temp_max": tmax, "temp_min": temp_min, "code": code}
        )

    output = {
        "current": {
            "temperature": data["current"]["temperature_2m"],
            "weather_code": data["current"]["weather_code"],
            "wind_speed": data["current"]["wind_speed_10m"],
        },
        "hourly": hourly_data,
        "daily": daily_data,
    }

    with open("weather_data.json", "w") as f:
         json.dump(output, f, indent=2)
pass

fetch_api_data()
