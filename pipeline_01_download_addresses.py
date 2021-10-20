"""
Extract Process #1

This process retrieves data from a URL, downloads that data, and then uploads
the data to a Google Cloud Storage bucket. The process expects the following
environment variables to be set:

* GOOGLE_APPLICATION_CREDENTIALS
* PIPELINE_DATA_BUCKET

"""

# Load process environment variables from file named ".env". Environment vars
# will be available in the os.environ dictionary.
from dotenv import load_dotenv
load_dotenv()

# Import additional required packages
import datetime as dt
import os
import requests
from google.cloud import storage

# Retrieve data from URL
print('Downloading the addresses data...')
response = requests.get('https://storage.googleapis.com/mjumbewu_musa_509/lab04_pipelines_and_web_services/get_latest_addresses')

# Save retrieved data to a local file
print('Saving addresses data to a file...')

outfile_path = f'data/addresses_{dt.date.today()}.csv'
with open(outfile_path, mode='wb') as outfile:
    outfile.write(response.content)

# Upload local file of data to Google Cloud Storage
print('Uploading addresses data to GCS...')
bucket_name = os.environ['PIPELINE_DATA_BUCKET']  # <-- retrieve the bucket name from the environment
blob_name = f'addresses_{dt.date.today()}.csv'

storage_robot = storage.Client()
bucket = storage_robot.bucket(bucket_name)
blob = bucket.blob(blob_name)
blob.upload_from_filename(outfile_path)

print('Done.')
