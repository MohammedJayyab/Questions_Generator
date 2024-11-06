import fitz  # PyMuPDF
import re
import os
from dotenv import load_dotenv

load_dotenv()

PDF_PATH = os.getenv("PDF_PATH")
CHAPTER_HEADER_PATTERN = os.getenv("CHAPTER_HEADER_PATTERN", r"(Chapter\s+\d+:\s+[^\n]+)")

def extract_text_from_pdf(pdf_path=PDF_PATH):
    try:
        text = ""
        with fitz.open(pdf_path) as pdf:
            for page in pdf:
                text += page.get_text()
        return text
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return None

def list_chapters(pdf_path=PDF_PATH):
    chapters = []
    try:
        with fitz.open(pdf_path) as pdf:
            for page_num in range(pdf.page_count):
                page = pdf[page_num]
                text = page.get_text()
                matches = re.findall(CHAPTER_HEADER_PATTERN, text)
                for match in matches:
                    chapters.append((match.strip(), page_num + 1))
        return chapters
    except Exception as e:
        print(f"Error listing chapters: {e}")
        return []

def extract_chapter(text, chapter_number):
    try:
        chapter_pattern = CHAPTER_HEADER_PATTERN.replace(r"\d+", str(chapter_number))
        pattern = f"{chapter_pattern}.*?(?={CHAPTER_HEADER_PATTERN}|$)"
        match = re.search(pattern, text, re.DOTALL)
        return match.group(0) if match else None
    except Exception as e:
        print(f"Error extracting chapter {chapter_number}: {e}")
        return None
