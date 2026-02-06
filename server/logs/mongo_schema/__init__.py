import os
import mongoengine

MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "forgestack_logs")
MONGO_HOST = os.getenv("MONGO_HOST", "127.0.0.1")
MONGO_PORT = int(os.getenv("MONGO_PORT", 27017))

mongoengine.connect(
    db=MONGO_DB_NAME,
    host=MONGO_HOST,
    port=MONGO_PORT,
    username=os.getenv("MONGO_USER", None),
    password=os.getenv("MONGO_PASSWORD", None),
    authentication_source="admin",  # adjust if needed
)
