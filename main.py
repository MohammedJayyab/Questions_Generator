from dotenv import load_dotenv
from mcq_generator.pdf_processor import extract_text_from_pdf, extract_chapter, list_chapters
from mcq_generator.chapter_splitter import split_chapter_into_subtopics
from mcq_generator.mcq_creator import  generate_mcq
from mcq_generator.mcq_exporter import export_mcqs_to_json

load_dotenv()

def main_menu():
    print("Choose an option:")
    print("1. List all chapters")
    print("2. Enter chapter number to generate MCQs")
    print("0. Exit")
    return input("Enter your choice: ")

def list_all_chapters():
    chapters = list_chapters()
    if not chapters:
        print("No chapters found.")
    else:
        for chapter, page in chapters:
            print(f"{chapter} - Page {page}")

def generate_mcqs_for_chapter():
    chapter_number = input("Enter chapter number: ")
    text = extract_text_from_pdf()
    chapter_text = extract_chapter(text, chapter_number)
    
    if not chapter_text:
        print(f"Chapter {chapter_number} not found.")
        return

    subtopics = split_chapter_into_subtopics(chapter_text)
    if not subtopics:
        print("No subtopics found.")
        return

    mcqs = generate_mcq(subtopics, 3, "medium")
    if mcqs:
        export_mcqs_to_json(mcqs)
    else:
        print("No MCQs generated.")

def main():
    while True:
        choice = main_menu()
        if choice == "1":
            list_all_chapters()
        elif choice == "2":
            generate_mcqs_for_chapter()
        elif choice == "0":
            print("Exiting program.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
