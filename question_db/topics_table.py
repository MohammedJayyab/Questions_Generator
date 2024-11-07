from .db_connection import get_db_connection

def insert_topic(chapter_id, topic_title, content, page_start, page_end):
    """Inserts a topic record into the topics table."""
    connection = get_db_connection()
    if not connection:
        return None
    
    cursor = connection.cursor()
    query = """
        INSERT INTO topics (chapter_id, topic_title, content, page_start, page_end)
        VALUES (%s, %s, %s, %s, %s)
    """
    cursor.execute(query, (chapter_id, topic_title, content, page_start, page_end))
    connection.commit()
    topic_id = cursor.lastrowid
    cursor.close()
    connection.close()
    return topic_id
