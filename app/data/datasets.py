def insert_dataset(conn, dataset_name, category, source, last_updated, record_count, file_size_mb):
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO datasets_metadata
        (dataset_name, category, source, last_updated, record_count, file_size_mb)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (dataset_name, category, source, last_updated, record_count, file_size_mb))
    conn.commit()
    return cursor.lastrowid

def get_dataset_by_id(conn, dataset_id):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM datasets_metadata WHERE id = ?", (dataset_id,))
    return cursor.fetchone()

def update_dataset_stats(conn, dataset_id, new_record_count, new_file_size):
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE datasets_metadata
        SET record_count = ?, file_size_mb = ?
        WHERE id = ?
    """, (new_record_count, new_file_size, dataset_id))
    conn.commit()
    return cursor.rowcount

def delete_dataset(conn, dataset_id):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM datasets_metadata WHERE id = ?", (dataset_id,))
    conn.commit()
    return cursor.rowcount
