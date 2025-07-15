# 📚 Data Harvesting & Structuring Assignment

This project is built to crawl, download, extract, and structure scanned literature (PDFs, eBooks) from Indian heritage archives. It uses both embedded text and OCR (via Tesseract) to extract content and generates clean JSON metadata records.

---

## 🧠 Key Features

- 🌐 Web crawler using `requests` and `Selenium`
- 📥 Auto-download of `.pdf`, `.html`, `.epub` documents
- 🔍 Text extraction (embedded + OCR via Tesseract)
- 🧾 Metadata extraction (title, language, authors, etc.)
- 💾 JSON output with schema validation
- 🔁 Delta processing via file checksum
- 🧪 Interactive test runner (5 assignment test cases)

---

## 🛠️ Requirements

- Python 3.8+
- VS Code (recommended)
- Google Chrome (for Selenium)
- [Tesseract OCR (Windows installer)](https://github.com/UB-Mannheim/tesseract/wiki)

Install all Python dependencies:

```bash
pip install -r requirements.txt
