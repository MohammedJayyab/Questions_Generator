from .db_connection import get_db_connection

def insert_annotation(topic_id, note, page_number):
    """Inserts an annotation record into the annotations table."""
    connection = get_db_connection()
    if not connection:
        return None
    
    cursor = connection.cursor()
    query = """
        INSERT INTO annotations (topic_id, note, page_number)
        VALUES (%s, %s, %s)
    """
    cursor.execute(query, (topic_id, note, page_number))
    connection.commit()
    annotation_id = cursor.lastrowid
    cursor.close()
    connection.close()
    return annotation_id
