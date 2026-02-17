import requests
from google.cloud import storage


def stream_to_gcs():
    BUCKET_NAME = "de-zoomcamp-483921-analytics-bucket"
    MONTHS = [f"{i:02d}" for i in range(1, 13)]
    
    for month in MONTHS:
        FILE_NAME = f"fhv_tripdata_2019-{month}.csv.gz"
        FILE_URL = f"https://github.com/DataTalksClub/nyc-tlc-data/releases/download/fhv/{FILE_NAME}"
        TABLE_ID = FILE_NAME
        BLOB_NAME = f"fhv/{FILE_NAME}"  # path in GCS

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
    stream_to_gcs()

