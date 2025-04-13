#!/bin/bash
set -e

echo "Starting ETL process..."
python /app/main.py

echo "Creating Metabase views..."
PGPASSWORD=$DB_PASSWORD psql -h $DB_HOST -U $DB_USER -d $DB_NAME -f /app/metabase_views.sql

echo "ETL process completed successfully"
