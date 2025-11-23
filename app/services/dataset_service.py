import pandas as pd
from pathlib import Path

def load_csv_to_table(conn, csv_path, table_name):
    """
    Load a CSV file into a database table using pandas.

    Args:
        conn: Database connection
        csv_path: Path to CSV file
        table_name: Name of the target table

    Returns:
        int: Number of rows loaded
    """
    csv_path = Path(csv_path)

    # 1. Check if CSV file exists
    if not csv_path.exists():
        print(f"CSV file not found: {csv_path}")
        return 0

    # 2. Read the CSV into a DataFrame
    try:
        df = pd.read_csv(csv_path)
    except Exception as e:
        print(f"Error reading {csv_path.name}: {e}")
        return 0

    # 3. Insert data into table
    try:
        df.to_sql(
            name=table_name,
            con=conn,
            if_exists='append',
            index=False
        )
    except Exception as e:
        print(f"Error loading data into {table_name}: {e}")
        return 0

    # 4. Print success and return row count
    row_count = len(df)
    print(f"Loaded {row_count} rows into '{table_name}' from {csv_path.name}")
    return row_count

def load_all_csv_data(conn):
    """
    Load all CSVs into the database.
    Calls load_csv_to_table() for each file.
    Returns total rows loaded.
    """
    total_rows = 0
    total_rows += load_csv_to_table(conn, "DATA/cyber_incidents.csv", "cyber_incidents")
    total_rows += load_csv_to_table(conn, "DATA/datasets_metadata.csv", "datasets_metadata")
    total_rows += load_csv_to_table(conn, "DATA/it_tickets.csv", "it_tickets")
    return total_rows
