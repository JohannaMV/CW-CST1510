def insert_dataset(conn, dataset_id, name, row, columns, uploaded_by, upload_date):
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO datasets_metadata
        (dataset_id, name, row, columns, uploaded_by, upload_date)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (dataset_id, name, row, columns, uploaded_by, upload_date))
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

def get_dataset_by_uploader(conn, min_rows=1000):
    """counts datasets by uploader if they have more than min rows"""
    query = """
    SELECT uploaded_by, COUNT(*) as count
    FROM datasets_metadata
    WHERE rows > ?
    GROUP BY uploaded_by
    ORDER BY count DESC
    """
    df= pd.read_sql_query(query, conn, params=(min_rows,))
    return df
