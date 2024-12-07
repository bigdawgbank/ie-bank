from azure.identity import DefaultAzureCredential
import psycopg2

credential = DefaultAzureCredential()
token = credential.get_token("https://ossrdbms-aad.database.windows.net").token

print(token)

connection = psycopg2.connect(
    dbname="dkumlin-db-dev",
    user="dkumlin-be-dev",  # Managed Identity Username
    host="dkumlin-dbsrv-dev.postgres.database.azure.com",
    sslmode="require",
    password=token,
)

print("Connected successfully")
connection.close()
