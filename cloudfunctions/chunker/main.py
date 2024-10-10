from cloudevents.http import CloudEvent

import functions_framework
import chunker
import gs_functions

# Triggered by a change in a storage bucket
@functions_framework.cloud_event
def main_chunker(cloud_event: CloudEvent):

    data = cloud_event.data

    event_id = cloud_event["id"]
    event_type = cloud_event["type"]

    bucket = data["bucket"]
    name = data["name"]
    metageneration = data["metageneration"]
    timeCreated = data["timeCreated"]
    updated = data["updated"]

    # Define the path and extension to filter
    target_path = "preprocessed/"
    target_extension = ".json"

    # Check if the file is in the target path and has the target extension
    if name.startswith(target_path) and name.endswith(target_extension):
        print(f"Event ID: {event_id}")
        print(f"Event type: {event_type}")
        print(f"Bucket: {bucket}")
        print(f"File: {name}")
        print(f"Metageneration: {metageneration}")
        print(f"Created: {timeCreated}")
        print(f"Updated: {updated}")

        data = gs_functions.open_file(bucket_name=bucket,file_name=name)
        print(data)

        chunked = chunker.Chunker(chunk_size=100).get_chunks(data["content"])

        print("RES")
        print(data["name"])
        print(chunked)
    else:
        print("Else")
        
    print(" LESGOOO ")

    #gcloud functions deploy chunker --gen2 --runtime=python312 --region=europe-west1 --source=. --entry-point=main_chunker --trigger-event-filters="type=google.cloud.storage.object.v1.finalized" --trigger-event-filters="bucket=prod-ragrules"


