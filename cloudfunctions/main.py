from io import BytesIO
import json

from cloudevents.http import CloudEvent
import functions_framework
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
    print("extract_text_from_pdf : step0")

    storage_client = storage.Client()
    blob = storage_client.bucket(bucket_name).blob(file_name)
    print("extract_text_from_pdf : step1")

    file_stream = BytesIO()
    blob.download_to_file(file_stream)
    file_stream.seek(0)  # Reset the stream position to the beginning
    print("extract_text_from_pdf : step2")

    reader = PdfReader(file_stream)
    print("extract_text_from_pdf : step3")
    import time
    print("sleeping..")
    time.sleep(4)
    print("wakeup")
    text = ""
    for page in reader.pages:    
        print(f"here is a page before update : <{page}>")
        text += page.extract_text() + "\n"
        print(f"here is a page after apdate : <{page}>")

    print("extract_text_from_pdf : step4")

    return text


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
    print("save_text_to_bucket : step1")

    # Create a dictionary with the required keys
    data = {
        "name": file_path,
        "content": text
    }
    
    # Convert the dictionary to a JSON string
    json_data = json.dumps(data)
    
    # Upload the JSON string to the bucket
    blob.upload_from_string(json_data, content_type='application/json')

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
        return None


# [END functions_cloudevent_storage]







































# def main(request):
#     """Traite un fichier qui est déposé sur un bucket Cloud Storage.

#     Args:
#         request (flask.Request): La requête HTTP.

#     Returns:
#         flask.Response: La réponse HTTP.
#     """

#     # Récupérer les données de l'événement Cloud Storage
#     event = request.get_json()

#     # Récupérer le nom du bucket et du fichier
#     bucket_name = event['bucket']
#     file_name = event['name']

#     # Télécharger le fichier du bucket Cloud Storage
#     storage_client = storage.Client()
#     bucket = storage_client.bucket(bucket_name)
#     blob = bucket.blob(file_name)
#     contents = blob.download_as_string()

#     # Traiter le fichier (remplacez ceci par votre logique métier)
#     # Par exemple, décoder le fichier en base64
#     decoded_contents = base64.b64decode(contents)
    

#     # Effectuer l'action désirée avec le contenu du fichier décodés
#     # ...

#     # Créer la réponse HTTP
#     response = {
#         'message': 'Fichier traité avec succès.',
#     }
#     return json.dumps(response), 200



#     def extract_text_from_pdf(bucket_name, file_name, output_file_name):
#         """Extrait le texte d'un fichier PDF dans un bucket Google Storage et le sauvegarde dans un autre fichier.

#         Args:
#             bucket_name (str): Le nom du bucket.
#             file_name (str): Le chemin du fichier PDF dans le bucket.
#             output_file_name (str): Le chemin du fichier de sortie dans le bucket.
#         """
#         # Initialiser les clients Google Cloud Storage et Vision
#         storage_client = storage.Client()
#         vision_client = vision.ImageAnnotatorClient()

#         # Télécharger le fichier PDF du bucket Cloud Storage
#         bucket = storage_client.bucket(bucket_name)
#         blob = bucket.blob(file_name)
#         pdf_content = blob.download_as_bytes()

#         # Utiliser l'API Vision pour extraire le texte du PDF
#         pdf = vision.types.InputConfig(content=pdf_content, mime_type='application/pdf')
#         feature = vision.types.Feature(type=vision.enums.Feature.Type.DOCUMENT_TEXT_DETECTION)
#         request = vision.types.AnnotateFileRequest(input_config=pdf, features=[feature])

#         response = vision_client.batch_annotate_files(requests=[request])

#         # Extraire le texte des réponses
#         text = ""
#         for res in response.responses[0].responses:
#             text += res.full_text_annotation.text

#         # Sauvegarder le texte extrait dans un nouveau fichier dans le bucket
#         output_blob = bucket.blob(output_file_name)
#         output_blob.upload_from_string(text)

#         print(f"Texte extrait et sauvegardé dans {output_file_name}")

