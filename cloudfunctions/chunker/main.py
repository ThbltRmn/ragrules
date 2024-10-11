import chunker
import functions_framework
import gs_functions
from cloudevents.http import CloudEvent
from embedder import Embedder


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

        chunked = chunker.Chunker(chunk_size=100).get_chunks(data["content"])

        print("RES")
        print(data["name"])
        print(chunked)
    else:
        print("Else")

    if chunked:
        embedder = Embedder()

        contents = data["content"]

        # Embed content ; TODO replace by a batch embedding
        for content in contents:
            result = embedder.embed_content(
                content
            )

            # Print the first 50 characters of the embedding
            if result:
                embedder.print_trimmed_embedding(result)
            else:
                print("No embedding returned.")

            if result:
                embedder.save_embedding(content, result, "./embeded.txt", "./sentences.txt")
    print("All embeddings saved")

    gs_functions.upload_file("prod-ragrules","./embeded.txt","embeddings/embeded.txt")
    gs_functions.upload_file("prod-ragrules","./sentences.txt","embeddings/sentences.txt")


    #gcloud functions deploy chunker --gen2 --runtime=python312 --region=europe-west1 --source=. --entry-point=main_chunker --trigger-event-filters="type=google.cloud.storage.object.v1.finalized" --trigger-event-filters="bucket=prod-ragrules"


