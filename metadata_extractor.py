import os
from downloader import compute_checksum
from datetime import datetime
import fitz  # PyMuPDF

def extract_metadata(file_path, url):
    doc_id = os.path.splitext(os.path.basename(file_path))[0]
    checksum = compute_checksum(file_path)
    site = url.split("/")[2]
    metadata = {
        "site": site,
        "document_id": doc_id,
        "title": os.path.basename(file_path),
        "authors": ["Unknown"],
        "pub_year": "Unknown",
        "language": "Unknown",
        "download_url": url,
        "checksum": checksum,
        "scraped_at": datetime.utcnow().isoformat() + "Z"
    }
    try:
        if file_path.endswith(".pdf"):
            with fitz.open(file_path) as doc:
                meta = doc.metadata
                metadata["title"] = meta.get("title") or metadata["title"]
                metadata["authors"] = [meta.get("author")] if meta.get("author") else ["Unknown"]
                metadata["pub_year"] = meta.get("creationDate")[:4] if meta.get("creationDate") else "Unknown"
    except Exception as e:
        print(f"Metadata error for {file_path}: {e}")
    return metadata
