import re
import os
from dotenv import load_dotenv

load_dotenv()

SUBTOPIC_HEADER_PATTERN = os.getenv("SUBTOPIC_HEADER_PATTERN")

def split_chapter_into_subtopics(chapter_text):
    try:
        subtopics = re.split(SUBTOPIC_HEADER_PATTERN, chapter_text)
        headers = re.findall(SUBTOPIC_HEADER_PATTERN, chapter_text)
        return dict(zip(headers, subtopics[1:]))
    except Exception as e:
        print(f"Error splitting chapter into subtopics: {e}")
        return {}
