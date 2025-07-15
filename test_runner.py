import os
import json
from text_extractor import extract_text
from metadata_extractor import extract_metadata
from downloader import compute_checksum
from utils import save_json
from jsonschema import validate, ValidationError
from crawler import crawl_site
from downloader import download_documents

SCHEMA = {
    "type": "object",
    "properties": {
        "site": {"type": "string"},
        "document_id": {"type": "string"},
        "title": {"type": "string"},
        "authors": {"type": "array"},
        "pub_year": {"type": "string"},
        "language": {"type": "string"},
        "download_url": {"type": "string"},
        "checksum": {"type": "string"},
        "scraped_at": {"type": "string"},
        "content": {"type": "string"}
    },
    "required": ["site", "document_id", "title", "authors", "pub_year", "language", "download_url", "checksum", "scraped_at", "content"]
}

def TC1_crawl_input():
    print("\n====== ✅ TC1: Crawl Basic Page ======")
    url = input("🔗 Enter a URL to crawl (e.g., https://ayushportal.nic.in/default.aspx): ").strip()
    if not url:
        print("❌ No URL provided.")
        return
    links = crawl_site(url)
    print(f"✅ Found {len(links)} links.")
    pdf_links = [link for link in links if link.endswith(".pdf")]
    if pdf_links:
        print(f"✅ {len(pdf_links)} PDF links found:")
        for l in pdf_links[:5]:
            print("   -", l)
    else:
        print("❌ No PDF links found.")

def TC2_metadata_input():
    print("\n====== ✅ TC2: Metadata JSON ======")
    path = input("📄 Enter path to a PDF with embedded text: ").strip()
    if not os.path.isfile(path):
        print("❌ File not found.")
        return
    url = input("🔗 Enter the source URL of this document: ").strip()
    metadata = extract_metadata(path, url)
    print("📑 Extracted Metadata:")
    print(json.dumps(metadata, indent=2))

def TC3_ocr_input():
    print("\n====== ✅ TC3: OCR Extraction ======")
    path = input("📄 Enter path to a scanned PDF (image-only): ").strip()
    if not os.path.isfile(path):
        print("❌ File not found.")
        return
    text = extract_text(path)
    print("\n📄 OCR Output (first 500 chars):")
    print(text[:500] if text else "❌ OCR failed or empty text.")

def TC4_checksum_input():
    print("\n====== ✅ TC4: Checksum & Delta ======")
    original = input("📄 Enter path to original PDF: ").strip()
    modified = input("📄 Enter path to modified PDF: ").strip()
    if not os.path.isfile(original) or not os.path.isfile(modified):
        print("❌ One or both files not found.")
        return
    checksum1 = compute_checksum(original)
    checksum2 = compute_checksum(modified)
    print(f"🔍 Original Checksum: {checksum1}")
    print(f"🆕 Modified Checksum: {checksum2}")
    if checksum1 != checksum2:
        print("✅ Detected change — file should be reprocessed.")
    else:
        print("⚠️ No difference detected in checksums.")

def TC5_json_validation():
    print("\n====== ✅ TC5: JSON Schema Validation ======")
    json_path = input("📄 Enter path to the JSON file to validate: ").strip()
    if not os.path.isfile(json_path):
        print("❌ File not found.")
        return
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        validate(instance=data, schema=SCHEMA)
        print("✅ JSON record is valid against schema.")
    except ValidationError as e:
        print("❌ JSON schema validation failed:")
        print(e)
    except Exception as e:
        print("❌ Failed to load/parse JSON:")
        print(e)

def menu():
    print("\n📋 Select a Test Case to Run:")
    print("1. TC1 - Crawl a Page (provide URL)")
    print("2. TC2 - Metadata Extraction (upload PDF)")
    print("3. TC3 - OCR Extraction (upload scanned PDF)")
    print("4. TC4 - Checksum Comparison (upload 2 PDFs)")
    print("5. TC5 - Validate JSON Output (upload JSON)")
    print("0. Exit")
    return input("Enter choice (0–5): ").strip()

if __name__ == "__main__":
    while True:
        choice = menu()
        if choice == "1":
            TC1_crawl_input()
        elif choice == "2":
            TC2_metadata_input()
        elif choice == "3":
            TC3_ocr_input()
        elif choice == "4":
            TC4_checksum_input()
        elif choice == "5":
            TC5_json_validation()
        elif choice == "0":
            print("👋 Exiting interactive test runner.")
            break
        else:
            print("❌ Invalid choice. Try again.")
