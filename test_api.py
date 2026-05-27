import requests

url = "https://air-quality-api.open-meteo.com/v1/air-quality"
params = {
    "latitude": 48.85,
    "longitude": 2.35,
    "current": "pm10,pm2_5,nitrogen_dioxide,ozone,european_aqi",
}

reponse = requests.get(url, params=params)
données = reponse.json()
print(données)
