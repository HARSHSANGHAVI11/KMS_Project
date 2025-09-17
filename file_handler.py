import os
from typing import List
import fitz  # PyMuPDF
import docx
import pytesseract
from PIL import Image
import io

# Optional: Set Tesseract path if needed (Windows)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def read_txt(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

def ocr_image(image_bytes: bytes) -> str:
    """Run OCR on image bytes and return extracted text."""
    img = Image.open(io.BytesIO(image_bytes))
    return pytesseract.image_to_string(img)

def read_pdf(file_path: str) -> str:
    """Extract text + OCR from images in PDF."""
    text = ""
    doc = fitz.open(file_path)

    for page_num, page in enumerate(doc):
        # 1️⃣ Extract text from the page
        text += page.get_text() + "\n"

        # 2️⃣ Extract images and run OCR
        for img_index, img in enumerate(page.get_images(full=True)):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            ocr_text = ocr_image(image_bytes)
            if ocr_text.strip():
                text += f"\n[Image_Text_Page_{page_num+1}_{img_index+1}]\n{ocr_text}\n"

    return text

def read_docx(file_path: str) -> str:
    """Extract text + OCR from images in DOCX."""
    doc = docx.Document(file_path)
    full_text = "\n".join([para.text for para in doc.paragraphs])

    # Extract and OCR images
    for rel in doc.part.rels.values():
        if "image" in rel.target_ref:
            image_data = rel.target_part.blob
            ocr_text = ocr_image(image_data)
            if ocr_text.strip():
                full_text += f"\n[Image_Text]\n{ocr_text}\n"

    return full_text

def read_file(file_path: str) -> str:
    ext = os.path.splitext(file_path)[1].lower()
    if ext == ".pdf":
        return read_pdf(file_path)
    elif ext == ".docx":
        return read_docx(file_path)
    elif ext == ".txt":
        return read_txt(file_path)
    else:
        raise ValueError("Unsupported file type")
