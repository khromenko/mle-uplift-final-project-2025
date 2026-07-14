export $(cat .env | xargs)

DB_URL=postgresql://$DB_DESTINATION_USER:$DB_DESTINATION_PASSWORD@$DB_DESTINATION_HOST:$DB_DESTINATION_PORT/$DB_DESTINATION_NAME?sslmode=require

mlflow server \
  --backend-store-uri $DB_URL \
  --registry-store-uri $DB_URL \
  --default-artifact-root s3://$S3_BUCKET_NAME