from pathlib import Path
import pandas as pd
from extractors import OpenAQExtractor
from loaders import GCSLoader

OUTPUT_DIR = Path("output")

def run():
    # Étape 1 : crée le dossier output si inexistant
    OUTPUT_DIR.mkdir(exist_ok=True)

    # Étape 2 : extrais les données
    extractor = OpenAQExtractor()
    records = extractor.extract()

    # Étape 3 : vérifie qu'on a des données
    if not records:
        print("Aucun enregistrement valide.")
        return

    # Étape 4 : convertis en DataFrame pandas
    # Indice : pd.DataFrame([r.model_dump() for r in records])
    df = pd.DataFrame([r.model_dump() for r in records])

    # Étape 5 : exporte en Parquet
    out_path = OUTPUT_DIR / "airquality.parquet"
    df.to_parquet(out_path, index=False)

    # Étape 6 : upload vers GCS
    loader = GCSLoader()
    loader.upload(out_path, dataset="airquality")

    print(f"✅ {len(df)} lignes exportées → {out_path}")
    print(df)

if __name__ == "__main__":
    run()

