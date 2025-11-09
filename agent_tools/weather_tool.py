from agents import function_tool
import requests



@function_tool
def get_weather(city: str):
    """Fetch the weather of current city"""
    print(f"Calling weather for: {city}")
    url = f"https://wttr.in/{city}?format=j1"
    response = requests.get(url)
    parse_data = response.json()
    data = parse_data["current_condition"][0]
    return data