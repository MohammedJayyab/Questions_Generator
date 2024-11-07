from .db_connection import get_db_connection

def insert_chapter(book_id, chapter_number, title, page_start, page_end):
    """Inserts a chapter record into the chapters table."""
    connection = get_db_connection()
    if not connection:
        return None
    
    cursor = connection.cursor()
    query = """
        INSERT INTO chapters (book_id, chapter_number, title, page_start, page_end)
        VALUES (%s, %s, %s, %s, %s)
    """
    cursor.execute(query, (book_id, chapter_number, title, page_start, page_end))
    connection.commit()
    chapter_id = cursor.lastrowid
    cursor.close()
    connection.close()
    return chapter_id
