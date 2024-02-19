import io
import requests
import pandas as pd
import pyarrow.parquet as pq
from io import BytesIO


if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@data_loader
def load_data_from_api(*args, **kwargs):
    
    df = pd.DataFrame()

    # construct the year-month inputs..
    years = ['2022'] 
    months = ['01','02','03','04','05','06','07','08','09','10','11','12']

    for year in years:
        for month in months:

            
            url = f'https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_{year}-{month}.parquet'
            
            df_rows = len(df)
            print(f'Nr rows in df: {df_rows}')
            
            # download the file
            response = requests.get(url)
            parquet_data = BytesIO(response.content)

            col_dtypes =  {
                'VendorID': pd.Int64Dtype(), 
                'lpep_pickup_datetime': str,
                'lpep_dropoff_datetime': str,
                'store_and_fwd_flag': str,
                'RatecodeID': pd.Int64Dtype(), 
                'PULocationID': pd.Int64Dtype(), 
                'DOLocationID': pd.Int64Dtype(), 
                'passenger_count': pd.Int64Dtype(), 
                'trip_distance': float, 
                'fare_amount': float,
                'extra': float,
                'mta_tax': float,
                'tip_amount': float,
                'tolls_amount': float,
                'payment_type': pd.Int64Dtype(), 
                'ehail_fee': float,
                'improvement_surcharge': float,
                'total_amount': float,
                'payment_type': pd.Int64Dtype(),
                'trip_type': pd.Int64Dtype(),
                'congestion_surcharge': float
            }
            
            temp_df = pq.read_table(parquet_data).to_pandas()

            # Apply data type conversion to DataFrame columns
            for col, dtype in col_dtypes.items():
                temp_df[col] = temp_df[col].astype(dtype)
            
            # change date cols to date datatype
            parse_dates = ['lpep_pickup_datetime', 'lpep_dropoff_datetime']
            for date_col in parse_dates:
                temp_df[date_col] = pd.to_datetime(temp_df[date_col])
            
            df = pd.concat([df, temp_df], ignore_index=True)
            
            #temp_df = pd.read_csv(url, sep=',', compression='gzip', dtype=taxi_dtypes, parse_dates=parse_dates)
            #df = pd.concat([df, temp_df], ignore_index=True)
    
    return df


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
