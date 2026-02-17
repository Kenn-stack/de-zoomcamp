from google.cloud import bigquery

def load_to_bq(taxi_type):
    PROJECT_ID = "de-zoomcamp-483921"
    BUCKET_NAME = "de-zoomcamp-483921-analytics-bucket"
    DATASET_ID = "nytaxi"


    gcs_uri = f"gs://{BUCKET_NAME}/fhv/fhv_tripdata*"
    bq_client = bigquery.Client(project=PROJECT_ID)
    dataset_id_full = f"{PROJECT_ID}.{DATASET_ID}"
    dataset = bigquery.Dataset(dataset_id_full)
    dataset.location = "us-central1"  # set your location
    bq_client.create_dataset(dataset, exists_ok=True)
    table_ref = f"{PROJECT_ID}.{DATASET_ID}.fhv_tripdata"

    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.CSV,
        skip_leading_rows=1,
        autodetect=True,
        write_disposition="WRITE_APPEND",
    )

    load_job = bq_client.load_table_from_uri(gcs_uri, table_ref, job_config=job_config)
    load_job.result()

    print("Load into BigQuery complete")



if __name__ == "__main__":
    load_to_bq("green")
