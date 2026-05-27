from datetime import datetime, timezone
import pytest
from pydantic import ValidationError
from models import WeatherRecord, AirQualityRecord

# Données valides réutilisables
def valid_payload():
    return dict(
        city="Paris", country="FR",
        timestamp=datetime.now(timezone.utc),
        temperature_c=18.5, humidity_pct=72.0,
        wind_speed_kmh=15.0, precipitation_mm=0.0,
        weather_code=1,
    )   

# Test 1 : un enregistrement valide doit fonctionner
def test_valid_record():
    r = WeatherRecord(**valid_payload())
    assert r.city == "PARIS" 

# Test 2 : la ville doit être normalisée en majuscules
def test_city_normalized():
    r = WeatherRecord(**{**valid_payload(), "city": "  paris  "})
    assert r.city == "PARIS"

# Test 3 : humidité > 100 doit être rejetée
def test_humidity_above_100_rejected():
    with pytest.raises(ValidationError):
        WeatherRecord(**{**valid_payload(), "humidity_pct": 172.0})

# Test 4 : vent négatif doit être rejeté
def test_negative_wind_rejected():
    with pytest.raises(ValidationError):
        WeatherRecord(**{**valid_payload(), "wind_speed_kmh": -15.0})

# Test 5 : ville vide doit être rejetée
def test_empty_city_rejected():
    with pytest.raises(ValidationError):
        WeatherRecord(**{**valid_payload(), "city": " "})

# Test 6 : humidité à la limite basse (0) doit être acceptée
def test_humidity_boundary_0():
    r = WeatherRecord(**{**valid_payload(), "humidity_pct": 0.0})
    assert r.humidity_pct == 0

# Test 7 : humidité à la limite haute (100) doit être acceptée  
def test_humidity_boundary_100():
    r = WeatherRecord(**{**valid_payload(), "humidity_pct": 100.0})
    assert r.humidity_pct == 100.0

# Données valides réutilisables pour AirQualityRecord
def valid_air_payload():
    return dict(
        city="London", country="GB",
        timestamp=datetime.now(timezone.utc),
        pm25=12.5, pm10=22.0,
        no2=18.0, o3=55.0, aqi=48
    )

# Test 8 : enregistrement valide doit fonctionner
def test_air_valid_record():
    r = AirQualityRecord(**valid_air_payload())
    assert r.city == "LONDON" 

# Test 9 : ville normalisée en majuscules
def test_air_city_normalized():
    r = AirQualityRecord(**{**valid_air_payload(), "city": "  london  "})
    assert r.city == "LONDON"

# Test 10 : AQI > 500 doit être rejeté
def test_air_aqi_above_500_rejected():
    with pytest.raises(ValidationError):
        AirQualityRecord(**{**valid_air_payload(), "aqi": 550})

# Test 11 : PM2.5 négatif doit être rejeté
def test_air_negative_pm25_rejected():
    with pytest.raises(ValidationError):
        AirQualityRecord(**{**valid_air_payload(), "pm25": -12.5})

# Test 12 : tous les champs None doit être rejeté
def test_air_all_measures_none_rejected():
    with pytest.raises(ValidationError):
        AirQualityRecord(
            city="London",
            country="GB",
            timestamp=datetime.now(timezone.utc),
            pm25=None,
            pm10=None,
            no2=None,
            o3=None,
            aqi=None,
        )
