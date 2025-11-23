from app.data.db import connect_database

def insert_user(conn, username, password_hash, role='user'):
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO users (username, password_hash, role)
        VALUES (?, ?, ?)
    """, (username, password_hash, role))
    conn.commit()
    return cursor.lastrowid

def get_user_by_username(conn, username):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    return cursor.fetchone()

def update_user_role(conn, username, new_role):
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE users
        SET role = ?
        WHERE username = ?
    """, (new_role, username))
    conn.commit()
    return cursor.rowcount

def delete_user(conn, username):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE username = ?", (username,))
    conn.commit()
    return cursor.rowcount






