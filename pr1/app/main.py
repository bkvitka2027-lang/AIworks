from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse, JSONResponse

from .openmeteo import get_current_weather, WeatherError

app = FastAPI(title="Weather App")

INDEX_HTML = """<!DOCTYPE html>
<html lang="uk">
<head>
<meta charset="utf-8">
<title>Погода</title>
<style>
  body { font-family: system-ui, sans-serif; max-width: 520px; margin: 60px auto; padding: 0 16px; }
  input, button { font-size: 16px; padding: 8px 12px; }
  #result { margin-top: 24px; font-size: 18px; }
  .error { color: #c0392b; }
</style>
</head>
<body>
  <h1>Поточна погода</h1>
  <form id="form">
    <input id="city" placeholder="Введіть місто" required>
    <button type="submit">Дізнатися</button>
  </form>
  <div id="result"></div>
<script>
document.getElementById('form').addEventListener('submit', async (e) => {
  e.preventDefault();
  const city = document.getElementById('city').value.trim();
  const out = document.getElementById('result');
  out.textContent = 'Завантаження...';
  out.className = '';
  try {
    const r = await fetch('/weather?city=' + encodeURIComponent(city));
    const data = await r.json();
    if (!r.ok) {
      out.className = 'error';
      out.textContent = 'Помилка: ' + (data.detail || 'невідома');
      return;
    }
    out.textContent = `${data.city}, ${data.country}: ${data.temperature}${data.units.temperature}, вітер ${data.wind_speed} ${data.units.wind_speed}`;
  } catch (err) {
    out.className = 'error';
    out.textContent = 'Помилка мережі';
  }
});
</script>
</body>
</html>"""


@app.get("/", response_class=HTMLResponse)
def index():
    return INDEX_HTML


@app.get("/weather")
def weather(city: str = Query(..., min_length=1)):
    try:
        return JSONResponse(get_current_weather(city))
    except WeatherError as e:
        return JSONResponse({"detail": e.message}, status_code=e.status_code)