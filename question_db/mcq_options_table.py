from .db_connection import get_db_connection

def insert_mcq_option(mcq_id, option_text, is_correct):
    """Inserts an answer option for an MCQ into the mcq_options table."""
    connection = get_db_connection()
    if not connection:
        return None
    
    cursor = connection.cursor()
    query = """
        INSERT INTO mcq_options (mcq_id, option_text, is_correct)
        VALUES (%s, %s, %s)
    """
    cursor.execute(query, (mcq_id, option_text, is_correct))
    connection.commit()
    option_id = cursor.lastrowid
    cursor.close()
    connection.close()
    return option_id
