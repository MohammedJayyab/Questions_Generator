import fitz  # PyMuPDF

def clean_text_dynamically(text):
    # Initialize cleaned text
    cleaned_text = ""
    prev_char = ""
    
    # Iterate over each character in text
    for i, char in enumerate(text):
        # Handle lowercase to uppercase transitions by adding a space
        if prev_char.islower() and char.isupper():
            cleaned_text += " " + char
        # Handle uppercase to lowercase transition where uppercase is followed by lowercase
        elif prev_char.isupper() and char.isupper() and (i < len(text) - 1 and text[i+1].islower()):
            cleaned_text += " " + char
        else:
            # Otherwise, add the character directly
            cleaned_text += char
        prev_char = char

    return cleaned_text

def get_pdf_title(pdf_path):
    # Open the PDF file and read the first page
    with fitz.open(pdf_path) as doc:
        if len(doc) > 0:
            page = doc.load_page(0)
            text = page.get_text("text")
            
            # Split text into lines and process initial lines for title
            lines = text.splitlines()
            title_lines = []
            for i, line in enumerate(lines[:5]):  # Limiting to first few lines
                stripped_line = line.strip()
                if stripped_line:
                    # Clean line dynamically to manage spaces effectively
                    cleaned_line = clean_text_dynamically(stripped_line)
                    title_lines.append(cleaned_line)
                    
                    # Stop if we identify a non-title line
                    if i > 0 and not stripped_line[0].isupper():
                        break

            # Join all lines for a cohesive title output
            title = ' '.join(title_lines)
            return title.strip()

    return "Title not found"

# Example usage
pdf_path = 'data/software_developement.pdf'
title = get_pdf_title(pdf_path)
print("Title:", title)
