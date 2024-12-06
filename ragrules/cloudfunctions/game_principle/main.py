import json
import os
from io import BytesIO

import functions_framework
from cloudevents.http import CloudEvent
from google.cloud import storage
from pypdf import PdfReader

import google.generativeai as genai

genai.configure(api_key=os.environ["GEMINI_API_KEY"])


def ask_llm_for_summary(text, api_key):
    
    prompt = (
        "The following is a set of board game rules. Extract and summarize the game principle, "
        "focusing on the objective and how players interact with the game, and the game vocabulary.\n\n"
        "Summarize the game principle in one concise paragraph:"
        f"{text}\n\n"
    )
    
    result = genai.embed_content(
            model=self.model,
            content=content,
            task_type=self.task_type,
            title=title if title else "Embedding of content",
        )
    
    return response['choices'][0]['message']['content']


def save_text_to_bucket(bucket_name: str, file_path: str, text: str) -> None:
    """
    Sauvegarde le texte dans un fichier JSON dans un bucket Google Storage.

    Args:
        bucket_name (str): Le nom du bucket.
        file_path (str): Le chemin du fichier où sauvegarder le texte dans le bucket.
        text (str): Le texte à sauvegarder.
    """
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(file_path)

    # Create a dictionary with the required keys
    data = {"name": file_path, "content": text}

    # Convert the dictionary to a JSON string
    json_data = json.dumps(data)

    # Upload the JSON string to the bucket
    blob.upload_from_string(json_data, content_type="application/json")

def open_file(bucket_name, file_name):
    print("Opening")
    storage_client = storage.Client()
    blob = storage_client.bucket(bucket_name).blob(file_name)
    print("aft blob")
    data = json.loads(blob.download_as_string(client=None))
    print(data)
    return data


# Triggered by a change in a storage bucket
@functions_framework.cloud_event
def preprocess(cloud_event: CloudEvent) -> tuple:
    """This function is triggered by a change in a storage bucket.

    Args:
        cloud_event: The CloudEvent that triggered this function.
    Returns:
        The event ID, event type, bucket, name, metageneration, and timeCreated.
    """
    data = cloud_event.data

    event_id = cloud_event["id"]
    event_type = cloud_event["type"]

    bucket = data["bucket"]
    name = data["name"]
    metageneration = data["metageneration"]
    timeCreated = data["timeCreated"]
    updated = data["updated"]

    # Define the path and extension to filter
    target_path = "raw/"
    target_extension = ".pdf"

    # Check if the file is in the target path and has the target extension
    if name.startswith(target_path) and name.endswith(target_extension):
        print(f"Event ID: {event_id}")
        print(f"Event type: {event_type}")
        print(f"Bucket: {bucket}")
        print(f"File: {name}")
        print(f"Metageneration: {metageneration}")
        print(f"Created: {timeCreated}")
        print(f"Updated: {updated}")

        filename = name.split("/")[-1].split(".")[0]

        print(f"running extract_text_from_pdf with bucket : <{bucket}> and name : <{name}>")
        extracted_rules = extract_text_from_pdf(bucket, name)
        print("text extracted")
        save_text_to_bucket(bucket, f"preprocessed/{filename}.json", extracted_rules)
        print(f"text saved to preprocessed/{filename}.json")

        return event_id, event_type, bucket, name, metageneration, timeCreated, updated
    else:
        print(f"File {name} does not match the target path and extension.")
        return None, None, None, None, None, None, None
