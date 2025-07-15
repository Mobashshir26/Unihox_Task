import os
from crawler import crawl_site
from downloader import download_documents
from metadata_extractor import extract_metadata
from text_extractor import extract_text
from delta_checker import get_delta_documents
from utils import save_json

# List of all 7 target URLs
START_URLS = [
    "https://sanskritdocuments.org/scannedbooks/asisanskritpdfs.html",
    "https://sanskritdocuments.org/scannedbooks/asiallpdfs.html",
    "https://indianculture.gov.in/ebooks",
    "https://ignca.gov.in/divisionss/asi-books/",
    "https://archive.org/details/TFIC_ASI_Books/ACatalogueOfTheSamskritManuscriptsInTheAdyarLibraryPt.1/",
    "https://indianmanuscripts.com/",
    "https://niimh.nic.in/ebooks/ayuhandbook/index.php"
 
]

# Ensure required folders exist
os.makedirs("downloads", exist_ok=True)
os.makedirs("output", exist_ok=True)

if __name__ == "__main__":
    for url in START_URLS:
        print(f"\n🕷️ Crawling: {url}")
        all_links = crawl_site(url)

        # Get only new or updated files
        changed_links = get_delta_documents(all_links)
        print(f"🔗 New/updated files found: {len(changed_links)}")

        for link in changed_links:
            print(f"\n⬇️ Downloading: {link}")
            file_path = download_documents(link)

            if file_path:
                print(f"📄 Extracting metadata and text from: {os.path.basename(file_path)}")
                
                # Extract metadata
                metadata = extract_metadata(file_path, link)

                # Extract content (embedded or OCR)
                content = extract_text(file_path)
                metadata["content"] = content

                # Save to JSON
                save_json(metadata, "output")

        print(f"✅ Completed processing for: {url}")
