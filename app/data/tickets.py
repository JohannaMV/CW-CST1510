import pandas as pd

def insert_ticket(conn, ticket_id, priority, description, status, assigned_to, created_at, resolution_time_hours):
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO it_tickets
        (ticket_id, priority, description, status, assigned_to, created_at, resolution_time_hours)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (ticket_id, priority, description, status, assigned_to, created_at, resolution_time_hours))
    conn.commit()
    return cursor.lastrowid

def get_ticket_by_id(conn, ticket_id):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM it_tickets WHERE ticket_id = ?", (ticket_id,))
    return cursor.fetchone()

def update_ticket_status(conn, ticket_id, new_status):
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE it_tickets
        SET status = ?
        WHERE ticket_id = ?
    """, (new_status, ticket_id))
    conn.commit()
    return cursor.rowcount

def delete_ticket(conn, ticket_id):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM it_tickets WHERE ticket_id = ?", (ticket_id,))
    conn.commit()
    return cursor.rowcount

def get_tickets_by_status_count(conn):
    """
    Count tickets by status.
    Uses: SELECT, FROM, GROUP BY, ORDER BY
    """
    query = """
    SELECT status, COUNT(*) as count
    FROM it_tickets
    GROUP BY status
    ORDER BY count DESC
    """
    df = pd.read_sql_query(query, conn)
    return df

def get_high_severity_by_priority(conn):
    """
    Count high severity  by status.
    Uses: SELECT, FROM, WHERE, GROUP BY, ORDER BY
    """
    query = """
    SELECT priority, COUNT(*) as count
    FROM it_tickets
    WHERE priority = 'High'
    GROUP BY priority
    ORDER BY count DESC
    """
    df = pd.read_sql_query(query, conn)
    return df

def get_assigned_to_with_many_cases(conn, min_count=5):
    """
    Find assigned with more than min_count cases.
    Uses: SELECT, FROM, GROUP BY, HAVING, ORDER BY
    """
    query = """
    SELECT assigned_to, COUNT(*) as count
    FROM it_tickets
    GROUP BY assigned_to
    HAVING COUNT(*) > ?
    ORDER BY count DESC
    """
    df = pd.read_sql_query(query, conn, params=(min_count,))
    return df



