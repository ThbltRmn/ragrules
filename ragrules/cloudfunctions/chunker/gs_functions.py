import json

from google.cloud import storage


def open_file(bucket_name, file_name):
    print("Opening")
    storage_client = storage.Client()
    blob = storage_client.bucket(bucket_name).blob(file_name)
    print("aft blob")
    data = json.loads(blob.download_as_string(client=None))
    print(data)
    return data


def upload_file(bucket_name, local_file_path, blob_file_path):
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(blob_file_path)
    blob.upload_from_filename(local_file_path)
