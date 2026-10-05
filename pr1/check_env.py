import sys
import requests

GEO_URL = "https://geocoding-api.open-meteo.com/v1/search"
WEATHER_URL = "https://api.open-meteo.com/v1/forecast"


def check_python():
    v = sys.version_info
    print(f"Python: {v.major}.{v.minor}.{v.micro}")
    if v.major < 3 or (v.major == 3 and v.minor < 10):
        print("  ! Рекомендовано Python 3.10+")
        return False
    print("  OK")
    return True


def check_imports():
    ok = True
    for name in ("fastapi", "uvicorn", "requests"):
        try:
            __import__(name)
            print(f"{name}: OK")
        except ImportError:
            print(f"{name}: НЕ ВСТАНОВЛЕНО (pip install -r requirements.txt)")
            ok = False
    return ok


def check_geocoding():
    try:
        r = requests.get(GEO_URL, params={"name": "Kyiv", "count": 1}, timeout=5)
        r.raise_for_status()
        data = r.json()
        if data.get("results"):
            print("Geocoding API: OK")
            return True
        print("Geocoding API: відповідь без results")
        return False
    except Exception as e:
        print(f"Geocoding API: ПОМИЛКА ({e})")
        return False


def check_weather():
    try:
        r = requests.get(
            WEATHER_URL,
            params={
                "latitude": 50.45,
                "longitude": 30.52,
                "current": "temperature_2m,wind_speed_10m",
            },
            timeout=5,
        )
        r.raise_for_status()
        data = r.json()
        if "current" in data:
            print("Weather API: OK")
            return True
        print("Weather API: відповідь без 'current'")
        return False
    except Exception as e:
        print(f"Weather API: ПОМИЛКА ({e})")
        return False


def main():
    print("=== Перевірка середовища ===")
    results = [
        check_python(),
        check_imports(),
        check_geocoding(),
        check_weather(),
    ]
    print("===========================")
    if all(results):
        print("Все готово до роботи.")
    else:
        print("Деякі перевірки не пройдено — див. вище.")


if __name__ == "__main__":
    main()