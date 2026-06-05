import os
from pathlib import Path

import requests
import pdfplumber
import pytesseract
from dotenv import load_dotenv

from PIL import Image
from bs4 import BeautifulSoup

# Load root .env if present, so TESSERACT_CMD can be defined there.
ROOT_DIR = Path(__file__).resolve().parents[1]
load_dotenv(ROOT_DIR / ".env")

# Allow overriding tesseract cmd via env var (pytesseract uses this).
if os.getenv("TESSERACT_CMD"):
    tesseract_cmd = Path(os.getenv("TESSERACT_CMD"))
    if not tesseract_cmd.is_absolute():
        tesseract_cmd = ROOT_DIR / tesseract_cmd
    if tesseract_cmd.exists():
        pytesseract.pytesseract.tesseract_cmd = str(tesseract_cmd)
else:
    local_tesseract = ROOT_DIR / "tesseract_bin" / "tesseract.exe"
    if local_tesseract.exists():
        pytesseract.pytesseract.tesseract_cmd = str(local_tesseract)

# Ensure Tesseract can find its traineddata files.
if os.getenv("TESSDATA_PREFIX"):
    tessdata_prefix = Path(os.getenv("TESSDATA_PREFIX"))
    if not tessdata_prefix.is_absolute():
        tessdata_prefix = ROOT_DIR / tessdata_prefix
    os.environ["TESSDATA_PREFIX"] = str(tessdata_prefix)
else:
    os.environ["TESSDATA_PREFIX"] = str(ROOT_DIR / "tessdata")

# Defer checking for the tesseract binary until OCR is actually requested.
# This prevents the FastAPI app from crashing on import if the binary
# is missing; an informative error will be raised when `extract_image`
# is called instead.
TESSERACT_AVAILABLE = True
try:
    # calling get_tesseract_version will raise if tesseract binary is not found
    pytesseract.get_tesseract_version()
except Exception:
    TESSERACT_AVAILABLE = False


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

        if not TESSERACT_AVAILABLE:
            raise RuntimeError(
                "Tesseract OCR is not installed or not found in PATH. "
                "Install Tesseract and ensure it's available on your PATH, or set the TESSERACT_CMD environment variable to the tesseract executable."
            )

        img = Image.open(path)

        return pytesseract.image_to_string(img)
