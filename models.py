"""
EcoPulse-Ingestor — Phase 0
Modèles Pydantic V2 pour la validation des données météo et qualité de l'air.
"""

from datetime import datetime, timezone
from typing import Optional
from pydantic import BaseModel, field_validator, model_validator

class BaseRecord(BaseModel):
    city: str
    country: str
    timestamp: datetime

    @field_validator("city", "country")
    @classmethod
    def normalize_string(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("Le champ ne peut pas être vide.")
        return v.upper()

    @field_validator("timestamp")
    @classmethod
    def ensure_utc(cls, v: datetime) -> datetime:
        if v.tzinfo is None:
            return v.replace(tzinfo=timezone.utc)
        return v.astimezone(timezone.utc)

class WeatherRecord(BaseRecord):
    """Représente une mesure météorologique validée."""
    temperature_c: float
    humidity_pct: float
    wind_speed_kmh: float
    precipitation_mm: float
    weather_code: int

    @field_validator("humidity_pct")
    @classmethod
    def validate_humidity(cls, v: float) -> float:
        if not (0.0 <= v <= 100.0):
            raise ValueError(f"Humidité invalide : {v}. Doit être entre 0 et 100.")
        return v

    @field_validator("wind_speed_kmh", "precipitation_mm")
    @classmethod
    def validate_positive(cls, v: float) -> float:
        if v < 0:
            raise ValueError(f"La valeur ne peut pas être négative : {v}")
        return v


class AirQualityRecord(BaseRecord):
    """Représente une mesure de qualité de l'air validée."""

    pm25: Optional[float] = None     # Particules fines (µg/m³)
    pm10: Optional[float] = None     # Particules grossières (µg/m³)
    no2: Optional[float] = None      # Dioxyde d'azote (µg/m³)
    o3: Optional[float] = None       # Ozone (µg/m³)
    aqi: Optional[int] = None        # Indice qualité de l'air (0-500)

    @field_validator("pm25", "pm10", "no2", "o3")
    @classmethod
    def validate_concentration(cls, v: Optional[float]) -> Optional[float]:
        if v is not None and v < 0:
            raise ValueError(f"La concentration ne peut pas être négative : {v}")
        return v

    @field_validator("aqi")
    @classmethod
    def validate_aqi(cls, v: Optional[int]) -> Optional[int]:
        if v is not None and not (0 <= v <= 500):
            raise ValueError(f"AQI invalide : {v}. Doit être entre 0 et 500.")
        return v

    @model_validator(mode="after")
    def at_least_one_measure(self) -> "AirQualityRecord":
        measures = [self.pm25, self.pm10, self.no2, self.o3, self.aqi]
        if all(m is None for m in measures):
            raise ValueError("Au moins une mesure de qualité de l'air est requise.")
        return self
