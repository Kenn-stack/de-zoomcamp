#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import pyarrow.dataset as ds
import pyarrow.fs as fs
import fsspec
from sqlalchemy import create_engine
from tqdm.auto import tqdm
import click


dtype = {
    "VendorID": "Int64",
    "passenger_count": "Int64",
    "trip_distance": "float64",
    "RatecodeID": "Int64",
    "store_and_fwd_flag": "string",
    "PULocationID": "Int64",
    "DOLocationID": "Int64",
    "payment_type": "Int64",
    "fare_amount": "float64",
    "extra": "float64",
    "mta_tax": "float64",
    "tip_amount": "float64",
    "tolls_amount": "float64",
    "improvement_surcharge": "float64",
    "total_amount": "float64",
    "congestion_surcharge": "float64"
}

parse_dates = [
    "tpep_pickup_datetime",
    "tpep_dropoff_datetime"
]

def ingest_parquet_data(url: str, engine, target_table: str)-> pd.DataFrame:

    # filesystem = fs.FileSystem.from_uri(url)[0]

    # dataset = ds.dataset(url, filesystem=filesystem, format="parquet")

    # first = True
    # for batch in dataset.to_batches(batch_size=100_000):        
    #     df_chunk = batch.to_pandas()
    #     if first:
    #         df_chunk.head(0).to_sql(
    #     name=target_table,
    #     con=engine,
    #     if_exists="replace"
    # )

    #     print(f"Table {target_table} created")

    #     df_chunk.to_sql(
    #         name=target_table,
    #         con=engine,
    #         if_exists="append"
    #     )

    #     print(f"Inserted first chunk: {len(df_chunk)}")
    #     first = False

    df = pd.read_parquet(url)
    df.to_sql(
            name=target_table,
            con=engine,
            if_exists="replace"
        )
    print(f'done ingesting to {target_table}')




def ingest_csv_data(
        url: str,
        engine,
        target_table: str,
        chunksize: int = 100000,
) -> pd.DataFrame:
    df_iter = pd.read_csv(
        url,
        iterator=True,
        chunksize=chunksize
    )

    first_chunk = next(df_iter)

    first_chunk.head(0).to_sql(
        name=target_table,
        con=engine,
        if_exists="replace"
    )

    print(f"Table {target_table} created")

    first_chunk.to_sql(
        name=target_table,
        con=engine,
        if_exists="append"
    )

    print(f"Inserted first chunk: {len(first_chunk)}")

    for df_chunk in tqdm(df_iter):
        df_chunk.to_sql(
            name=target_table,
            con=engine,
            if_exists="append"
        )
        print(f"Inserted chunk: {len(df_chunk)}")

    print(f'done ingesting to {target_table}')

@click.command()
@click.option('--pg-user', default='root', help='PostgreSQL username')
@click.option('--pg-pass', default='root', help='PostgreSQL password')
@click.option('--pg-host', default='localhost', help='PostgreSQL host')
@click.option('--pg-port', default='5432', help='PostgreSQL port')
@click.option('--pg-db', default='ny_taxi', help='PostgreSQL database name')
@click.option('--year', default=2021, type=int, help='Year of the data')
@click.option('--month', default=1, type=int, help='Month of the data')
@click.option('--chunksize', default=100000, type=int, help='Chunk size for ingestion')
@click.option('--parquet-target-table', default='green_taxi_data', help='Target table name')
@click.option('--csv-target-table', default='zones', help='Target table name')


def main(pg_user, pg_pass, pg_host, pg_port, pg_db, year, month, chunksize, parquet_target_table, csv_target_table):

    engine = create_engine(f'postgresql://{pg_user}:{pg_pass}@{pg_host}:{pg_port}/{pg_db}')
    # url_prefix = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow'

    parquet_url = "https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2025-11.parquet"
    csv_url = "https://github.com/DataTalksClub/nyc-tlc-data/releases/download/misc/taxi_zone_lookup.csv"


    ingest_parquet_data(url=parquet_url, engine=engine, target_table=parquet_target_table)

    ingest_csv_data(
        url=csv_url,
        engine=engine,
        target_table=csv_target_table,
        chunksize=chunksize
    )


if __name__ == '__main__':
    main()