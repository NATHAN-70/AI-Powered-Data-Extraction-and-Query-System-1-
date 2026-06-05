import os
import requests
import pdfplumber
import pytesseract

from PIL import Image
from bs4 import BeautifulSoup

# Allow overriding tesseract cmd via env var (pytesseract uses this)
if os.getenv("TESSERACT_CMD"):
    pytesseract.pytesseract.tesseract_cmd = os.getenv("TESSERACT_CMD")

# Quick runtime check for tesseract binary to fail fast with a helpful message
try:
    # calling get_languages will raise if tesseract binary is not found
    pytesseract.get_tesseract_version()
except Exception:
    raise RuntimeError(
        "Tesseract OCR is not installed or not found in PATH. "
        "Install Tesseract and ensure it's available on your PATH, or set the TESSERACT_CMD environment variable to the tesseract executable. "
        "See INSTALL_TESSERACT.md for platform-specific installation instructions."
    )


class Extractor:

    @staticmethod
    def extract_url(url):

        response = requests.get(url, timeout=10)

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        return soup.get_text(separator=" ")

    @staticmethod
    def extract_pdf(path):

        text = ""

        with pdfplumber.open(path) as pdf:

            for page in pdf.pages:

                page_text = page.extract_text()

                if page_text:
                    text += page_text + "\n"

        return text

    @staticmethod
    def extract_image(path):

        img = Image.open(path)

        return pytesseract.image_to_string(img)
