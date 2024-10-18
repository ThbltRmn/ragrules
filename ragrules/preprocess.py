import json
from io import BytesIO

from google.cloud import storage
from pypdf import PdfReader


def extract_text_from_pdf(bucket_name, file_name):
    """
    Extrait le texte d'un fichier PDF dans un bucket Google Storage.

    Args:
        bucket_name (str): Le nom du bucket.
        file_name (str): Le chemin du fichier PDF dans le bucket.

    Returns:
        str: Le texte extrait du fichier PDF.
    """
    storage_client = storage.Client()
    blob = storage_client.bucket(bucket_name).blob(file_name)
    file_stream = BytesIO()
    blob.download_to_file(file_stream)
    file_stream.seek(0)  # Reset the stream position to the beginning

    reader = PdfReader(file_stream)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"

    return text


test = extract_text_from_pdf("prod-ragrules", "raw/e1-crack-list-regle.pdf")


def save_text_to_bucket(bucket_name, file_path, text):
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


save_text_to_bucket("prod-ragrules", "preprocessed/e1-crack-list-regle.json", test)
