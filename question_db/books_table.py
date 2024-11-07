from .db_connection import get_db_connection

def insert_book(title, author, publication_year, isbn, total_chapters):
    """Inserts a book record into the books table."""
    connection = get_db_connection()
    if not connection:
        return None
    
    cursor = connection.cursor()
    query = """
        INSERT INTO books (title, author, publication_year, isbn, total_chapters)
        VALUES (%s, %s, %s, %s, %s)
    """
    cursor.execute(query, (title, author, publication_year, isbn, total_chapters))
    connection.commit()
    book_id = cursor.lastrowid
    cursor.close()
    connection.close()
    return book_id
