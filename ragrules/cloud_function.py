def main(request):
    """Traite un fichier qui est déposé sur un bucket Cloud Storage.

    Args:
        request (flask.Request): La requête HTTP.

    Returns:
        flask.Response: La réponse HTTP.
    """

    # Récupérer les données de l'événement Cloud Storage
    event = request.get_json()

    # Récupérer le nom du bucket et du fichier
    bucket_name = event['bucket']
    file_name = event['name']

    # Télécharger le fichier du bucket Cloud Storage
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(file_name)
    contents = blob.download_as_string()

    # Traiter le fichier (remplacez ceci par votre logique métier)
    # Par exemple, décoder le fichier en base64
    decoded_contents = base64.b64decode(contents)
    

    # Effectuer l'action désirée avec le contenu du fichier décodés
    # ...

    # Créer la réponse HTTP
    response = {
        'message': 'Fichier traité avec succès.',
    }
    return json.dumps(response), 200



    def extract_text_from_pdf(bucket_name, file_name, output_file_name):
        """Extrait le texte d'un fichier PDF dans un bucket Google Storage et le sauvegarde dans un autre fichier.

        Args:
            bucket_name (str): Le nom du bucket.
            file_name (str): Le chemin du fichier PDF dans le bucket.
            output_file_name (str): Le chemin du fichier de sortie dans le bucket.
        """
        # Initialiser les clients Google Cloud Storage et Vision
        storage_client = storage.Client()
        vision_client = vision.ImageAnnotatorClient()

        # Télécharger le fichier PDF du bucket Cloud Storage
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(file_name)
        pdf_content = blob.download_as_bytes()

        # Utiliser l'API Vision pour extraire le texte du PDF
        pdf = vision.types.InputConfig(content=pdf_content, mime_type='application/pdf')
        feature = vision.types.Feature(type=vision.enums.Feature.Type.DOCUMENT_TEXT_DETECTION)
        request = vision.types.AnnotateFileRequest(input_config=pdf, features=[feature])

        response = vision_client.batch_annotate_files(requests=[request])

        # Extraire le texte des réponses
        text = ""
        for res in response.responses[0].responses:
            text += res.full_text_annotation.text

        # Sauvegarder le texte extrait dans un nouveau fichier dans le bucket
        output_blob = bucket.blob(output_file_name)
        output_blob.upload_from_string(text)

        print(f"Texte extrait et sauvegardé dans {output_file_name}")

