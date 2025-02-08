import mongoengine
from decouple import config
import sys
from django.core.management.base import BaseCommand

connection_established = False

def connect_to_mongodb():
    global connection_established
    if connection_established:
        return

    # Read the full MongoDB URI from the environment variable
    MONGO_URI = config("MONGO_URI")
    
    # Connect using the URI
    mongoengine.connect(host=MONGO_URI)
    connection_established = True
    sys.stdout.write(BaseCommand().style.SUCCESS("Mongo DB Connection Established\n"))

connect_to_mongodb()