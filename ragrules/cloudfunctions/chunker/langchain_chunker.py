import json
import os
import sys

import functions_framework
from chunker import Chunker
from langchain.text_splitter import RecursiveCharacterTextSplitter

from cloudevents.http import CloudEvent
from embedder import Embedder
from gs_functions import open_file, upload_file

CHUNKS_SIZE = 200


def process_file(data, is_cloud=False, with_embedding=True):
    """
    Processes a file either locally or in the cloud.

    Args:
        data (dict): Contains file content and metadata (e.g., name, bucket).
        is_cloud (bool): Indicates if the function is running in GCP.
    """
    target_path = "preprocessed"
    target_extension = ".json"

    file_path = data["name"]
    file_name = data["name"].split("/")[-1]
    print(file_name)

    # Check if the file is in the target path and has the target extension
    if file_name.startswith(target_path) and file_name.endswith(target_extension):
        print(f"Processing file: {file_name}")

        if is_cloud:
            # Read file from cloud storage
            file_content = open_file(bucket_name=data["bucket"], file_name=file_path)
            content = file_content["content"]
        else:
            # Read local file
            try:
                with open(file_path, encoding="utf-8") as f:
                    content = json.load(f)["content"]
            except Exception as e:
                print(f"Failed to read file {file_path}: {e}")
                return

        # Use LangChain's RecursiveCharacterTextSplitter for chunking
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=300,
            chunk_overlap=100,
        )
        chunks = text_splitter.split_text(content)
        for c in chunks[:30]:
            print(f"Chunk is : {c} \nSize : {len(c)}")
        print(len(chunks))
        #print(chunks)
        #print(f"Chunks created: {"\nCHUNK : ".join(chunks)}")
        #print(f"Number of chunks : {len(chunks)}")

        if chunks and with_embedding:
            embedder = Embedder()

            # Embed content
            for chunk in chunks:
                print(f"Processing chunk: {chunk}")
                result = embedder.embed_content(chunk)

                if result:
                    embedder.print_trimmed_embedding(result)
                    embedder.save_embedding(result, chunk, "./embeded.txt", "./sentences.txt")
                    print("One embedding saved.")
                else:
                    print("No embedding returned for this chunk.")

        print("All embeddings saved.")

        if is_cloud:
            # Upload to cloud storage
            upload_file("prod-ragrules", "./embeded.txt", "embeddings/embeded.txt")
            upload_file("prod-ragrules", "./sentences.txt", "embeddings/sentences.txt")
            print("Embeddings uploaded to GCS.")
        else:
            #os.rename("./embeded.txt",f"~/Documents/Projects/{file_name}_embedded.json")
            #os.rename("./embeded.txt",f"~/Documents/Projects/{file_name}_sentences.json")
            print("Processing finished locally.")
    else:
        print("File does not match the target criteria.")


# Cloud Function Entry Point
@functions_framework.cloud_event
def main_chunker(cloud_event: CloudEvent):
    """
    Entry point for GCP Cloud Function triggered by a CloudEvent.
    """
    data = cloud_event.data
    print(f"Triggered by CloudEvent: {cloud_event['id']}")

    process_file(data, is_cloud=True)


# Local Execution
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script.py <local_file_path>")
        sys.exit(1)

    local_file_path = sys.argv[1]
    if not os.path.exists(local_file_path):
        print(f"File not found: {local_file_path}")
        sys.exit(1)

    data = {
        "name": local_file_path,
    }
    process_file(data, is_cloud=False, with_embedding=True)
