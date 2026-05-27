from unittest.mock import patch, MagicMock
from extractors import OpenMeteoExtractor, OpenAQExtractor

@patch("extractors.requests.get")
def test_extract_retourne_des_records(mock_get):

    # On définit ce que la fausse API retourne
    mock_get.return_value = MagicMock(
        status_code=200,
        raise_for_status=lambda: None,
        json=lambda: {
            "current": {
                "time": "2025-06-01T12:00",
                "temperature_2m": 18.5,
                "relative_humidity_2m": 72.0,
                "wind_speed_10m": 15.0,
                "precipitation": 0.0,
                "weather_code": 1,
            }
        }
    )

    # On lance l'extracteur — il va utiliser la FAUSSE API
    extractor = OpenMeteoExtractor()
    records = extractor.extract()

    # On vérifie le résultat
    assert len(records) == 4        # 4 villes
    assert records[0].city == "PARIS"

@patch("extractors.requests.get")
# Test 2 : la température doit être correctement parsée
def test_temperature_correctement_parsee(mock_get):
    mock_get.return_value = MagicMock(
        status_code=200,
        raise_for_status=lambda: None,
        json=lambda: {
            "current": {
                "time": "2025-06-01T12:00",
                "temperature_2m": 18.5,
                "relative_humidity_2m": 72.0,
                "wind_speed_10m": 15.0,
                "precipitation": 0.0,
                "weather_code": 1,
            }
        }
    )

    # On lance l'extracteur — il va utiliser la FAUSSE API
    extractor = OpenMeteoExtractor()
    records = extractor.extract()

    # On vérifie le résultat
    assert len(records) == 4        # 4 villes
    assert records[0].temperature_c == 18.5
    # même mock que test_extract_retourne_des_records
    # mais vérifie que records[0].temperature_c == 18.5

# Test 3 : si l'API retourne None, la liste doit être vide
@patch("extractors.requests.get")
def test_api_indisponible_retourne_liste_vide(mock_get):
    # Indice : simule une erreur réseau comme ça :
    import requests
    mock_get.side_effect = requests.exceptions.ConnectionError()
    
    extractor = OpenMeteoExtractor()
    records = extractor.extract()
    assert records == records == []

# Test 4 : la ville doit être en majuscules
@patch("extractors.requests.get")
def test_city_en_majuscules(mock_get):
    mock_get.return_value = MagicMock(
        status_code=200,
        raise_for_status=lambda: None,
        json=lambda: {
            "current": {
                "time": "2025-06-01T12:00",
                "temperature_2m": 18.5,
                "relative_humidity_2m": 72.0,
                "wind_speed_10m": 15.0,
                "precipitation": 0.0,
                "weather_code": 1,
            }
        }
    )

    # On lance l'extracteur — il va utiliser la FAUSSE API
    extractor = OpenMeteoExtractor()
    records = extractor.extract()

    # On vérifie le résultat
    assert len(records) == 4        # 4 villes
    assert records[0].city == "PARIS"
    # même mock, vérifie records[0].city == "PARIS"

# Test 5 : on definit la ville que ça doit retourner
@patch("extractors.requests.get")
def test_aq_extract_retourne_des_records(mock_get):
    mock_get.return_value = MagicMock(
        status_code=200,
        raise_for_status=lambda: None,
        json=lambda: {
            "current": {
                "time": "2025-06-01T12:00",
                "pm2_5": 12.5,
                "pm10": 22.0,
                "nitrogen_dioxide": 18.0,
                "ozone": 55.0,
                "european_aqi": 48,
            }
        }
    )
    extractor = OpenAQExtractor()
    records = extractor.extract()
    assert len(records) == 4
    assert records[0].city == "PARIS"

# Test 6 : la Particules fine doit être correctement parsée
@patch("extractors.requests.get")
def test_aq_pm25_correctement_parsee(mock_get):
    mock_get.return_value = MagicMock(
        status_code=200,
        raise_for_status=lambda: None,
        json=lambda: {
            "current": {
                "time": "2025-06-01T12:00",
                "pm2_5": 12.5,
                "pm10": 22.0,
                "nitrogen_dioxide": 18.0,
                "ozone": 55.0,
                "european_aqi": 48,
            }
        }
    )
    extractor = OpenAQExtractor()
    records = extractor.extract()
    assert records[0].pm25 == 12.5

# Test 7 : si l'API retourne None, la liste doit être vide
@patch("extractors.requests.get")
def test_aq_api_indisponible_retourne_liste_vide(mock_get):
    import requests
    mock_get.side_effect = requests.exceptions.ConnectionError()
    extractor = OpenAQExtractor()
    records = extractor.extract()
    assert records == records == []