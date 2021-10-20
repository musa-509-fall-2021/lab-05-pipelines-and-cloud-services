"""
Load Process

Take the files that we've created and load them both into the database. You
should end up with two tables: addresses and geocoded_address_results.

CONVERT THIS SCRIPT TO USE GOOGLE CLOUD STORAGE TO RETRIEVE THE INPUTS AND SAVE
THE OUTPUTS INTO GOOGLE BIGQUERY.

This process should download the files from steps 1 and 2 from Google Cloud
Storage to local files, and then upload the data into tables on Google BigQuery.
Since we've installed the sqlalchemy-bigquery package, we can simply rely on
sqlalchemy to talk to BigQuery. The call to `create_engine` will need to be
updated to use a BigQuery data set connection string of the form:

    bigquery://GOOGLE_PROJECT_ID/BIGQUERY_DATASET_NAME

sqlalchemy-bigquery knows to use your GOOGLE_APPLICATION_CREDENTIALS environment
variable to connect to Google Cloud Platform.
"""

import datetime as dt
import pandas as pd
import sqlalchemy as sqa

db = sqa.create_engine('postgresql://postgres:postgres@localhost:5432/musa_509_2021_lab04')

addresses_column_names = [
    'address_id',
    'street_address',
    'city',
    'state',
    'zip',
]
addresses_df = pd.read_csv(f'data/addresses_{dt.date.today()}.csv', names=addresses_column_names)
addresses_df.to_sql('addresses', db, index=False, if_exists='replace')

geocoded_column_names = [
    'address_id',
    'input_address',
    'match_status',
    'match_type',
    'matched_address',
    'lon_lat',
    'tiger_line_id',
    'tiger_line_side',
]
geocoded_df = pd.read_csv(f'data/geocoded_addresses_{dt.date.today()}.csv', names=geocoded_column_names)
geocoded_df.to_sql('geocoded_address_results', db, index=False, if_exists='replace')
