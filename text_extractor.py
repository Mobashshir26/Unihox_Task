import os
import pytesseract
from PIL import Image
import fitz  # PyMuPDF
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed

# ✅ Set installed Tesseract path
pytesseract.pytesseract.tesseract_cmd = r"E:\Machine Learning Projects\UniHox\tesseract_main\tesseract.exe"

# ✅ Confirm Tesseract is accessible
try:
    version_output = subprocess.check_output([pytesseract.pytesseract.tesseract_cmd, "--version"])
    print("✅ Using Tesseract:", version_output.decode().splitlines()[0])
except Exception as e:
    print("❌ Tesseract not found or not executable:", e)

# ✅ OCR function for a single page
def ocr_page(page, page_num):
    try:
        pix = page.get_pixmap(dpi=300)
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        ocr_text = pytesseract.image_to_string(img, lang='eng+san')  # or 'eng+san+hin'
        return f"\n--- Page {page_num + 1} (OCR) ---\n{ocr_text}"
    except Exception as e:
        return f"\n--- Page {page_num + 1} (OCR ERROR) ---\nError: {e}"

# ✅ Extract text with parallel OCR
def extract_text(file_path):
    try:
        if file_path.endswith(".pdf"):
            with fitz.open(file_path) as doc:
                full_text = []
                ocr_tasks = []

                print(f"📖 Total pages: {len(doc)}")
                with ThreadPoolExecutor(max_workers=4) as executor:
                    for page_num, page in enumerate(doc):
                        text = page.get_text()
                        if text.strip():
                            full_text.append(f"\n--- Page {page_num + 1} (Text) ---\n{text}")
                        else:
                            future = executor.submit(ocr_page, page, page_num)
                            ocr_tasks.append(future)

                    for future in as_completed(ocr_tasks):
                        full_text.append(future.result())

                return "\n".join(full_text).strip()
        else:
            return ""
    except Exception as e:
        print(f"❌ Error processing {file_path}: {e}")
        return ""
