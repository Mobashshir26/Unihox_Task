import os
import requests
from hashlib import sha256

def download_documents(url):
    local_filename = os.path.join("downloads", os.path.basename(url))
    try:
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(local_filename, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        return local_filename
    except Exception as e:
        print(f"Failed to download {url}: {e}")
        return None

def compute_checksum(file_path):
    h = sha256()
    with open(file_path, "rb") as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()
