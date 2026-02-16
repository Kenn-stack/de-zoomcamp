import requests
from google.cloud import storage


def stream_to_gcs(colour, year):
    BUCKET_NAME = "de-zoomcamp-483921-analytics-bucket"
    MONTHS = [f"{i:02d}" for i in range(1, 13)]
    
    for month in MONTHS:
        FILE_NAME = f"{colour}_tripdata_{year}-{month}.csv.gz"
        FILE_URL = f"https://github.com/DataTalksClub/nyc-tlc-data/releases/download/{colour}/{FILE_NAME}"
        TABLE_ID = FILE_NAME
        BLOB_NAME = FILE_NAME  # path in GCS

        # -----------------------------
        # 1️⃣ Check if CSV exists in GCS
        # -----------------------------
        storage_client = storage.Client(project='de-zoomcamp-483921')
        bucket = storage_client.bucket(BUCKET_NAME)
        blob = bucket.blob(BLOB_NAME)

        if blob.exists():
            print(f"File {BLOB_NAME} already exists in GCS. Skipping upload.")
        else:
            # -----------------------------
            # 2️⃣ Stream CSV to GCS
            # -----------------------------
            print(f"Streaming {FILE_URL} to GCS...")
            with requests.get(FILE_URL, stream=True) as response:
                response.raise_for_status()
                with blob.open("wb") as f:
                    for chunk in response.iter_content(chunk_size=1024*1024):
                        if chunk:
                            f.write(chunk)
            print("Upload complete.")


if __name__ == "__main__":
    stream_to_gcs("yellow", "2019")

