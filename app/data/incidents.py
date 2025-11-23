import pandas as pd
from app.data.db import connect_database

def insert_incident(conn, date, incident_type, severity, status, description, reported_by=None):
    """
    Insert a new cyber incident into the database.
    """
    cursor = conn.cursor()

    sql = """
    INSERT INTO cyber_incidents
    (date, incident_type, severity, status, description, reported_by)
    VALUES (?, ?, ?, ?, ?, ?)
    """

    cursor.execute(sql, (date, incident_type, severity, status, description, reported_by))
    conn.commit()

    return cursor.lastrowid

def get_incident_by_id(conn, incident_id):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM cyber_incidents WHERE id = ?", (incident_id,))
    return cursor.fetchone()

def update_incident_status(conn, incident_id, new_status):
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE cyber_incidents
        SET status = ?
        WHERE id = ?
    """, (new_status, incident_id))
    conn.commit()
    return cursor.rowcount

def delete_incident(conn, incident_id):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM cyber_incidents WHERE id = ?", (incident_id,))
    conn.commit()
    return cursor.rowcount


