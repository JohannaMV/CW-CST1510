import pandas as pd
from app.data.db import connect_database

def insert_incident(conn, incident_id, timestamp, severity, category, status, description):
    """
    Insert a new cyber incident into the database.
    """
    cursor = conn.cursor()

    sql = """
    INSERT INTO cyber_incidents
    (incident_id, timestamp, severity, category, status, description)
    VALUES (?, ?, ?, ?, ?, ?)
    """

    cursor.execute(sql, (incident_id, timestamp, severity, category, status, description))
    conn.commit()

    return cursor.lastrowid

def get_all_incidents(conn):
    return pd.read_sql_query("SELECT * FROM cyber_incidents", conn)

def get_incident_by_id(conn, incident_id):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM cyber_incidents WHERE id = ?", (incident_id,))
    return cursor.fetchone()

def update_incident_status(conn, incident_id, new_status):
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE cyber_incidents
        SET status = ?
        WHERE incident_id = ?
    """, (new_status, incident_id))
    conn.commit()
    return cursor.rowcount

def delete_incident(conn, incident_id):
    cursor = conn.cursor()
    cursor.execute("""
        DELETE FROM cyber_incidents
        WHERE incident_id = ?
    """, (incident_id,))
    conn.commit()
    return cursor.rowcount

def get_incidents_by_type_count(conn):
    """
    Count incidents by type.
    Uses: SELECT, FROM, GROUP BY, ORDER BY
    """
    query = """
    SELECT category, COUNT(*) as count
    FROM cyber_incidents
    GROUP BY category
    ORDER BY count DESC
    """
    df = pd.read_sql_query(query, conn)
    return df

def get_high_severity_by_status(conn):
    """
    Count high severity incidents by status.
    Uses: SELECT, FROM, WHERE, GROUP BY, ORDER BY
    """
    query = """
    SELECT severity, COUNT(*) as count
    FROM cyber_incidents
    WHERE severity = 'High'
    GROUP BY severity
    ORDER BY count DESC
    """
    df = pd.read_sql_query(query, conn)
    return df

def get_incident_types_with_many_cases(conn, min_count=5):
    """
    Find incident types with more than min_count cases.
    Uses: SELECT, FROM, GROUP BY, HAVING, ORDER BY
    """
    query = """
    SELECT category, COUNT(*) as count
    FROM cyber_incidents
    GROUP BY category
    HAVING COUNT(*) > ?
    ORDER BY count DESC
    """
    df = pd.read_sql_query(query, conn, params=(min_count,))
    return df

def update_incident(conn, incident_id, timestamp, severity, category, status, description):
    """update incident"""
    cursor = conn.cursor()
    sql_update = """ UPDATE cyber_incidents 
        SET timestamp = ?, 
        severity = ?, 
        category = ?, 
        status = ?, 
        description = ?
    WHERE incident_id = ?"""
    cursor.execute(sql_update, (timestamp, severity, category, status, description, incident_id))
    conn.commit()
    return cursor.rowcount