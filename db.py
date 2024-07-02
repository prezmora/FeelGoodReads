from azure.cosmos import CosmosClient, PartitionKey
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Initialize the Cosmos client with connection string from .env file
connection_string = os.getenv("COSMOS_DB_CONNECTION_STRING")
client = CosmosClient.from_connection_string(connection_string)

# Create the database
database_name = 'FeelGoodReadsAppDB'
database = client.create_database_if_not_exists(id=database_name)

# Create containers
user_container_name = 'Users'
book_container_name = 'Books'
mood_container_name = 'Moods'
admin_container_name = 'Admins'

user_container = database.create_container_if_not_exists(
    id=user_container_name,
    partition_key=PartitionKey(path="/email"),
    offer_throughput=400
)

book_container = database.create_container_if_not_exists(
    id=book_container_name,
    partition_key=PartitionKey(path="/mood"),
    offer_throughput=400
)

mood_container = database.create_container_if_not_exists(
    id=mood_container_name,
    partition_key=PartitionKey(path="/id"),
    offer_throughput=400
)

admin_container = database.create_container_if_not_exists(
    id=admin_container_name,
    partition_key=PartitionKey(path="/username"),
    offer_throughput=400
)
