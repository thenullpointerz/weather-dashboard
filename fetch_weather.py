import requests
import json
import anthropic


def generate_summary(current, today):
    client = anthropic.Anthropic()

    prompt = (
        f"Current weather in Mexico City: {current['temperature']}°C, "
        f"wind {current['wind_speed']} km/h. "
        f"Today's forecast: high of {today['temp_max']}°C, low of {today['temp_min']}°C. "
        "Write one short, casual sentence (max 20 words) summarizing the weather "
        "for a dashboard header. No greeting, just the summary."
    )

    response = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=100,
        messages=[{"role": "user", "content": prompt}],
    )

    return response.content[0].text.strip()


def fetch_api_data():
    url = "https://api.open-meteo.com/v1/forecast?latitude=19.4326&longitude=-99.1332&current=temperature_2m,weather_code,wind_speed_10m&hourly=temperature_2m,weather_code&daily=temperature_2m_max,temperature_2m_min,weather_code&past_days=7&timezone=America%2FMexico_City"
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

    current = {
        "temperature": data["current"]["temperature_2m"],
        "weather_code": data["current"]["weather_code"],
        "wind_speed": data["current"]["wind_speed_10m"],
    }

    # daily_data[7] is "today" (index 7, right after the 7 past days).
    # If the Claude call fails for any reason (no API credit, rate limit,
    # network issue), don't let it take down the whole fetch — the rest of
    # the dashboard should keep updating even without the blurb.
    try:
        summary = generate_summary(current, daily_data[7])
    except Exception as e:
        print(f"Could not generate summary: {e}")
        summary = None

    output = {
        "current": current,
        "hourly": hourly_data,
        "daily": daily_data,
        "summary": summary,
    }

    with open("weather_data.json", "w") as f:
        json.dump(output, f, indent=2)


fetch_api_data()
