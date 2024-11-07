from .db_connection import get_db_connection

def insert_mcq(topic_id, question, difficulty):
    """Inserts an MCQ record into the mcqs table."""
    connection = get_db_connection()
    if not connection:
        return None
    
    cursor = connection.cursor()
    query = """
        INSERT INTO mcqs (topic_id, question, difficulty)
        VALUES (%s, %s, %s)
    """
    cursor.execute(query, (topic_id, question, difficulty))
    connection.commit()
    mcq_id = cursor.lastrowid
    cursor.close()
    connection.close()
    return mcq_id
