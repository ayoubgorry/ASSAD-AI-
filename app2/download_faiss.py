import os
from google.cloud import storage
import subprocess

FAISS_BUCKET = os.environ.get("FAISS_BUCKET", "")
FAISS_DIR = os.environ.get("FAISS_DIR", "faiss_index_can2025")

if FAISS_BUCKET and not os.path.exists(FAISS_DIR):
    print(f"Downloading FAISS index from {FAISS_BUCKET} to {FAISS_DIR}...")
    client = storage.Client()
    bucket_name, prefix = FAISS_BUCKET.replace("gs://","").split("/",1)
    bucket = client.bucket(bucket_name)
    blobs = client.list_blobs(bucket_name, prefix=prefix)
    os.makedirs(FAISS_DIR, exist_ok=True)
    for b in blobs:
        dest_path = os.path.join(FAISS_DIR, os.path.relpath(b.name, prefix))
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)
        b.download_to_filename(dest_path)
    print("FAISS index downloaded.")
else:
    print("No FAISS bucket provided or index already present.")