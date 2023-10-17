import qdrant_client

import os

def qdrant():
    client = qdrant_client.QdrantClient(
    os.getenv("QDRANT_HOST"),
    api_key=os.getenv("QDRANT_API_KEY"),
    timeout=500
    )

    return client
