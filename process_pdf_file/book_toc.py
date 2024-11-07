import fitz  # PyMuPDF

def read_pdf_toc(pdf_path):
    # Open the PDF file
    with fitz.open(pdf_path) as doc:
        # Extract the Table of Contents (TOC)
        toc = doc.get_toc()
        
        if not toc:
            return "No TOC found in this document."
        
        # Display the TOC entries
        toc_entries = []
        for level, title, page in toc:
            # Format each TOC entry with its level, title, and page number
            toc_entry = f"Level {level}: {title} (Page {page})"
            toc_entries.append(toc_entry)
        
        return "\n".join(toc_entries)

# Example usage
pdf_path = 'data/software_developement.pdf'
toc_content = read_pdf_toc(pdf_path)
print("Table of Contents:\n", toc_content)
