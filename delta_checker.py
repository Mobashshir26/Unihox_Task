import os
import json
from downloader import compute_checksum

STATE_FILE = "checksums.json"

def load_previous_checksums():
    if not os.path.exists(STATE_FILE):
        return {}
    with open(STATE_FILE, "r") as f:
        return json.load(f)

def save_checksums(checksums):
    with open(STATE_FILE, "w") as f:
        json.dump(checksums, f, indent=2)

def get_delta_documents(file_urls):
    prev = load_previous_checksums()
    new_links = []

    for url in file_urls:
        filename = os.path.join("downloads", os.path.basename(url))
        if os.path.exists(filename):
            checksum = compute_checksum(filename)
            if url not in prev or prev[url] != checksum:
                new_links.append(url)
                prev[url] = checksum
        else:
            new_links.append(url)

    save_checksums(prev)
    return new_links
