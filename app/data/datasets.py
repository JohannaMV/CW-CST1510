import pandas as pd
def insert_dataset(conn, dataset_id, name, rows, columns, uploaded_by, upload_date):
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO datasets_metadata
        (dataset_id, name, rows, columns, uploaded_by, upload_date)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (dataset_id, name, rows, columns, uploaded_by, upload_date))
    conn.commit()
    return cursor.lastrowid

def get_all_datasets(conn):
    """gets all dataset metadata as a df"""
    df = pd.read_sql_query(
    "SELECT * FROM datasets_metadata ORDER BY dataset_id DESC",
    conn
    )
    return df

def update_dataset(conn, dataset_id, rows, columns):
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE datasets_metadata
        SET rows = ?, columns = ? 
        WHERE dataset_id = ?
    """, (rows, columns, dataset_id))
    conn.commit()
    return cursor.rowcount

def delete_dataset(conn, dataset_id):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM datasets_metadata WHERE dataset_id = ?", (dataset_id,))
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
