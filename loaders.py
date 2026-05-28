import os
from pathlib import Path
from google.cloud import storage

class GCSLoader:

    def __init__(self):
        # Lit le nom du bucket depuis la variable d'environnement
        self.bucket_name = os.environ.get("ECOPULSE_GCS_BUCKET", "ecopulse-raw")

    def upload(self, local_path: Path, dataset: str) -> str | None:
        """
        Upload un fichier Parquet vers GCS.
        Retourne l'URI GCS si succès, None si échec.
        
        Structure dans GCS :
        gs://ecopulse-raw/weather/year=2026/month=05/day=28/data.parquet
        """
        from datetime import datetime, timezone
        
        if not local_path.exists():
            print(f"Fichier introuvable : {local_path}")
            return None

        # Génère le chemin Hive automatiquement
        dt = datetime.now(timezone.utc)
        blob_path = (
            f"{dataset}/"
            f"year={dt.year}/"
            f"month={dt.month:02d}/"
            f"day={dt.day:02d}/"
            f"data.parquet"
        )

        try:
            client = storage.Client()
            bucket = client.bucket(self.bucket_name)
            blob = bucket.blob(blob_path)
            blob.upload_from_filename(str(local_path))

            gcs_uri = f"gs://{self.bucket_name}/{blob_path}"
            print(f"✅ Upload réussi : {gcs_uri}")
            return gcs_uri

        except Exception as e:
            print(f"❌ Échec upload : {e}")
            return None

if __name__ == "__main__":
    loader = GCSLoader()
    
    # Test avec le fichier weather qu'on a créé
    uri = loader.upload(
        local_path=Path("output/weather.parquet"),
        dataset="weather"
    )
    print("URI retournée :", uri)

    # Test avec le fichier weather qu'on a créé
    uri = loader.upload(
        local_path=Path("output/airquality.parquet"),
        dataset="airquality"
    )
    print("URI retournée :", uri)
