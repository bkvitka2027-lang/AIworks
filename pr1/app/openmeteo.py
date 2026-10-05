import requests

GEO_URL = "https://geocoding-api.open-meteo.com/v1/search"
WEATHER_URL = "https://api.open-meteo.com/v1/forecast"
TIMEOUT = 5


class WeatherError(Exception):
    def __init__(self, message, status_code=502):
        super().__init__(message)
        self.message = message
        self.status_code = status_code


def _get_json(url, params):
    try:
        response = requests.get(url, params=params, timeout=TIMEOUT)
    except requests.Timeout:
        raise WeatherError("Сервіс погоди не відповів вчасно", 504)
    except requests.ConnectionError:
        raise WeatherError("Немає з'єднання із сервісом погоди", 503)
    except requests.RequestException:
        raise WeatherError("Помилка звернення до сервісу погоди", 502)

    if 400 <= response.status_code < 500:
        raise WeatherError(f"Некоректний запит до API ({response.status_code})", 400)
    if response.status_code >= 500:
        raise WeatherError(f"Сервіс погоди тимчасово недоступний ({response.status_code})", 502)

    try:
        return response.json()
    except ValueError:
        raise WeatherError("Сервіс повернув некоректний JSON", 502)


def geocode_city(city: str):
    data = _get_json(GEO_URL, {"name": city, "count": 1, "language": "uk", "format": "json"})
    results = data.get("results")
    if not results:
        raise WeatherError(f"Місто '{city}' не знайдено", 404)
    first = results[0]
    return {
        "name": first.get("name", city),
        "country": first.get("country", ""),
        "latitude": first.get("latitude"),
        "longitude": first.get("longitude"),
    }


def get_current_weather(city: str):
    location = geocode_city(city)
    data = _get_json(WEATHER_URL, {
        "latitude": location["latitude"],
        "longitude": location["longitude"],
        "current": "temperature_2m,wind_speed_10m",
        "timezone": "auto",
    })

    current = data.get("current")
    if not current or "temperature_2m" not in current or "wind_speed_10m" not in current:
        raise WeatherError("Несподіваний формат відповіді від сервісу погоди", 502)

    return {
        "city": location["name"],
        "country": location["country"],
        "temperature": current["temperature_2m"],
        "wind_speed": current["wind_speed_10m"],
        "units": {
            "temperature": data.get("current_units", {}).get("temperature_2m", "°C"),
            "wind_speed": data.get("current_units", {}).get("wind_speed_10m", "km/h"),
        },
    }