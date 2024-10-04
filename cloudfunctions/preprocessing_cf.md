

1. First step : Grant access to SA to pubsub (do it only the first time, in this project, already done.)

```
PROJECT_ID=$(gcloud config get-value project)
PROJECT_NUMBER=$(gcloud projects list --filter="project_id:$PROJECT_ID" --format='value(project_number)')

SERVICE_ACCOUNT=$(gcloud storage service-agent --project=$PROJECT_ID)

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member serviceAccount:$SERVICE_ACCOUNT \
  --role roles/pubsub.publisher

```

2. Submit your cloud function

````
gcloud functions deploy preprocess-pdf \
--gen2 \
--runtime=python312 \
--region=europe-west1 \
--source=. \
--entry-point=preprocess \
--trigger-event-filters="type=google.cloud.storage.object.v1.finalized" \
--trigger-event-filters="bucket=prod-ragrules "
````

3. Check logs

````
gcloud functions logs read preprocess-pdf --region europe-west1 --gen2 --limit=20
````