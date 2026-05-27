import requests
from models import WeatherRecord, AirQualityRecord
from datetime import datetime

class BaseExtractor:
    
    def extract(self):
        raise NotImplementedError("À implémenter dans les sous-classes")
    
    def _get(self, url: str, params: dict):
        """Effectue une requête GET avec gestion d'erreurs.
        Retourne le JSON si succès, None si échec."""
        try:
            reponse = requests.get(url, params=params, timeout=10)
            reponse.raise_for_status()
            return reponse.json()
        except requests.exceptions.ConnectionError:
            print(f"Erreur réseau : impossible de joindre {url}")
            return None
        except requests.exceptions.Timeout:
            print(f"Timeout : {url} ne répond pas")
            return None
        except requests.exceptions.HTTPError as e:
            print(f"Erreur HTTP {e.response.status_code}")
            return None

class OpenMeteoExtractor(BaseExtractor):
    
    def __init__(self):
        self.url = "https://api.open-meteo.com/v1/forecast"
        #self.url = "https://api.open-meteo-FAUSSE-URL.com/v1/forecast"
        self.cities = [
            {"city": "Paris",  "country": "FR", "lat": 48.85, "lon": 2.35},
            {"city": "London", "country": "GB", "lat": 51.50, "lon": -0.12},
            {"city": "Berlin",  "country": "DE", "lat": 52.5200, "lon": 13.4050},
            {"city": "Madrid",  "country": "ES", "lat": 40.4168, "lon": -3.7038},
        ]
    
    def extract(self) -> list[WeatherRecord]:
        records = []
        for city in self.cities:
    
            # Étape 1 : appelle l'API
            
            # mais remplace latitude/longitude par city["lat"] et city["lon"]
            #url = "https://api.open-meteo.com/v1/forecast"
            params = {
                "latitude": city["lat"],
                "longitude": city["lon"],
                "current": "temperature_2m,relative_humidity_2m,wind_speed_10m,precipitation,weather_code",
                "timezone": "UTC",
            }
            

            données = self._get(self.url, params=params)
            if données is None:
               continue  # ← passe à la ville suivante sans crasher

            # reponse = requests.get(self.url, params=params)
    
            # Étape 2 : récupère le JSON
            # données = reponse.json()
    
            # Étape 3 : extrait les valeurs qui t'intéressent
            current = données["current"]
            temperature = current["temperature_2m"]
            humidity_pct=current["relative_humidity_2m"]
            wind_speed_kmh=current["wind_speed_10m"]
            precipitation_mm=current["precipitation"]
            weather_code=current["weather_code"]
    
            # Étape 4 : crée le WeatherRecord
            record = WeatherRecord(
                city=city["city"],
                country=city["country"],
                timestamp=datetime.fromisoformat(current["time"]),
                temperature_c=temperature,
                humidity_pct= humidity_pct,
                wind_speed_kmh=wind_speed_kmh,
                precipitation_mm=precipitation_mm,
                weather_code=weather_code,
           )
    
            # Étape 5 : ajoute à la liste
            records.append(record)

        return records

class OpenAQExtractor(BaseExtractor):

    def __init__(self):
        self.url = "https://air-quality-api.open-meteo.com/v1/air-quality"
        #self.url = "https://air-quality-api.open-meteo-FAUSSE-URL.com/v1/forecast"
        self.cities = [
            {"city": "Paris",  "country": "FR", "lat": 48.85, "lon": 2.35},
            {"city": "London", "country": "GB", "lat": 51.50, "lon": -0.12},
            {"city": "Berlin",  "country": "DE", "lat": 52.5200, "lon": 13.4050},
            {"city": "Madrid",  "country": "ES", "lat": 40.4168, "lon": -3.7038},

        ]


    def extract(self) -> list[AirQualityRecord]:
        records = []
        for city in self.cities:
    
            # Étape 1 : appelle l'API
            # (reprends ton code de test_api.py ici)
            # mais remplace latitude/longitude par city["lat"] et city["lon"]
            #url = "https://api.open-meteo.com/v1/forecast"
            params = {
                "latitude": city["lat"],
                "longitude": city["lon"],
                "current": "pm10,pm2_5,nitrogen_dioxide,ozone,european_aqi",
            }
            

            données = self._get(self.url, params=params)
            if données is None:
               continue  # ← passe à la ville suivante sans crasher

            # reponse = requests.get(self.url, params=params)
    
            # Étape 2 : récupère le JSON
            # données = reponse.json()
    
            # Étape 3 : extrait les valeurs qui t'intéressent
            current = données["current"]
            pm25  = current["pm2_5"]
            pm10  = current["pm10"]
            no2   = current["nitrogen_dioxide"]
            o3    = current["ozone"]
            aqi   = current["european_aqi"]
    
            # Étape 4 : crée le WeatherRecord
            record = AirQualityRecord(
                city=city["city"],
                country=city["country"],
                timestamp=datetime.fromisoformat(current["time"]),
                pm25=pm25,
                pm10=pm10,
                no2=no2,
                o3=o3,
                aqi=aqi,
           )
    
            # Étape 5 : ajoute à la liste
            records.append(record)

        return records


if __name__ == "__main__":
    print("\n--- Qualité de l'air ---")
    extractor_aq = OpenAQExtractor()
    records_aq = extractor_aq.extract()
    for r in records_aq:
        print(r.city, "AQI:", r.aqi, "PM2.5:", r.pm25)
    
    
