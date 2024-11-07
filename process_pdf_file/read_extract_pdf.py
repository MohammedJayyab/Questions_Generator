import os
import re
import fitz  # PyMuPDF
from dotenv import load_dotenv
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords

from process_pdf_file.book_title import  get_pdf_title

from question_db.books_table import insert_book
from question_db.chapters_table import insert_chapter
from question_db.topics_table import insert_topic

# Set NLTK data path to the existing directory
os.environ["NLTK_DATA"] = "C:/Users/mjayy/AppData/Roaming/nltk_data"

# Load environment variables
load_dotenv()

PDF_PATH = os.getenv("PDF_PATH")
CHAPTER_HEADER_PATTERN = os.getenv("CHAPTER_HEADER_PATTERN", r"(Chapter\s+\d+:\s+[^\n]+)")
SUBTOPIC_HEADER_PATTERN = os.getenv("SUBTOPIC_HEADER_PATTERN", r"(Subtopic\s+\d+:\s+[^\n]+)")

#CHAPTER_HEADER_PATTERN = r"Chapter\s+\d+:\s+([^\.\n]+)"
def clean_text(raw_text):
    cleaned_text = re.sub(r'[^\x20-\x7E]+', ' ', raw_text)  # Remove non-printable characters
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text)        # Normalize whitespace
    cleaned_text = re.sub(r'\s*\.*\s*\d+\s*$', '', cleaned_text).strip()  # Remove trailing dots and numbers
    return cleaned_text

def list_chapters(pdf_path):
    chapters = []
    try:
        with fitz.open(pdf_path) as pdf:
            for page_num in range(pdf.page_count):
                page = pdf[page_num]
                text = page.get_text()
                matches = re.findall(CHAPTER_HEADER_PATTERN, text)
                for match in matches:
                    chapter_title = clean_text(match)
                    chapters.append((chapter_title, page_num + 1))
        return chapters
    except Exception as e:
        print(f"Error listing chapters: {e}")
        return []

def extract_text_from_pdf(pdf_path=PDF_PATH):
    """Extracts the entire text from the PDF once."""
    try:
        text = ""
        with fitz.open(pdf_path) as pdf:
            for page in pdf:
                text += page.get_text()
        return text
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return None

def extract_book_details( ):
    title=get_pdf_title(pdf_path=PDF_PATH)
    author = "Unknown"
    year = "Unknown"
    isbn = "Unknown"
    return title, author, year, isbn
     


def extract_chapter(text, chapter_number):
    """Extracts a specific chapter's content based on its number."""
    try:
        # Replace the placeholder \d+ in the chapter pattern with the actual chapter number
        chapter_pattern = re.sub(r"\\d+", str(chapter_number), CHAPTER_HEADER_PATTERN)
        # Define a pattern to match the chapter content up to the next chapter header or the end
        pattern = f"{chapter_pattern}.*?(?={CHAPTER_HEADER_PATTERN}|$)"
        
        # Search for the chapter content
        match = re.search(pattern, text, re.DOTALL)
        return match.group(0).strip() if match else None
    except Exception as e:
        print(f"Error extracting chapter {chapter_number}: {e}")
        return None
# def split_chapter_into_subtopics(chapter_text):
#     """Splits chapter text into subtopics based on subtopic patterns."""
#     try:
#         subtopics = re.split(SUBTOPIC_HEADER_PATTERN, chapter_text)
#         headers = re.findall(SUBTOPIC_HEADER_PATTERN, chapter_text)
#         return dict(zip(headers, subtopics[1:]))
#     except Exception as e:
#         print(f"Error splitting chapter into subtopics: {e}")
#         return {}


def split_chapter_into_subtopics(chapter_text):
    try:
        sections = re.split(f'({SUBTOPIC_HEADER_PATTERN})', chapter_text)
        unified_subtopics = [clean_text(section) for section in sections if section.strip()]
        return unified_subtopics
    except Exception as e:
        print(f"Error splitting chapter into subtopics: {e}")
        return []






def extract_key_phrases(subtopic_text):
    """Extracts key phrases from subtopic text by removing stopwords."""
    try:
        sentences = sent_tokenize(subtopic_text)
        stop_words = set(stopwords.words("english"))
        key_phrases = []

        for sentence in sentences:
            words = word_tokenize(sentence)
            filtered_words = [word for word in words if word.isalpha() and word.lower() not in stop_words]
            if filtered_words:
                key_phrases.append(filtered_words[0])
        return key_phrases
    except Exception as e:
        print(f"Error extracting key phrases: {e}")
        return []

def main():
    # Extract the full text of the PDF once
    full_text = extract_text_from_pdf(PDF_PATH)
    if not full_text:
        print("Failed to extract text from PDF.")
        return

    # Extract book details from the full text
    title, author, year, isbn = extract_book_details()
    book_id = insert_book(title, author, year, isbn, 0)
    if not book_id:
        print("Failed to insert book.")
        return

    # List and process chapters
    chapters = list_chapters(PDF_PATH)
    if not chapters:
        print("No chapters found.")
        return

    print("Chapters detected:")
    for chapter_index, (chapter_title, start_page) in enumerate(chapters, start=1):
        print(f"{chapter_title} - Starts on Page {start_page}")

        # Extract and insert each chapter
        chapter_text = extract_chapter(full_text, chapter_index)
        if not chapter_text:
            print(f"Failed to extract text for {chapter_title}")
            continue
          
        chapter_id = insert_chapter(book_id, chapter_index, chapter_title, start_page, start_page + 10)
        if not chapter_id:
            print(f"Failed to insert chapter: {chapter_title}")
            continue

        print(f"\nProcessing {chapter_title}...")

        # Split chapter into subtopics and insert each subtopic
        subtopics = split_chapter_into_subtopics(chapter_text)
        if not subtopics:
            print(f"No subtopics found in {chapter_title}")
            continue

        for subtopic in subtopics:
            topic_id = insert_topic(chapter_id, clean_text(subtopic), "", start_page, start_page)
            if not topic_id:
                print(f"Failed to insert topic: {subtopic}")
                continue


            #print(f"\nSubtopic: {subtopic_title}")
            key_phrases = extract_key_phrases("")
            #print(f"Key Phrases: {', '.join(key_phrases)}")

if __name__ == "__main__":
    main()
