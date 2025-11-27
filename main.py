from app.data.db import connect_database
from app.data.schema import create_all_tables
from app.services.user_service import register_user, login_user, migrate_users_from_file
from app.data.incidents import insert_incident, get_all_incidents
from app.services.dataset_service import load_csv_to_table, load_all_csv_data

def main():
    print("=" * 60)
    print("Week 8: Database Demo")
    print("=" * 60)

    # 1. Setup database
    conn = connect_database()
    create_all_tables(conn)

    # 2. Migrate users
    migrate_users_from_file(conn)

    #3. loading data
    print("Moving data")
    load_csv_to_table(conn,"DATA/datasets_metadata.csv", "datasets_metadata")
    load_csv_to_table(conn, "DATA/cyber_incidents.csv", "cyber_incidents")
    load_csv_to_table(conn, "DATA/it_tickets.csv", "it_tickets")

    # 4. Test authentication
    success, msg = register_user("carl", "SecurePass123!", "intern")
    print(msg)

    success, msg = login_user("carl", "SecurePass123!")
    print(msg)

    # 5. Test CRUD
    incident_id = insert_incident(
        conn,
        "2024-12-05",
        "Phishing",
        "High",
        "Open",
        "Suspicious sms detected",
        "carl"
    )
    print(f"Created incident #{incident_id}")

    # 6. Query data
    df = get_all_incidents(conn)
    print(f"Total incidents: {len(df)}")

    conn.close()

if __name__ == "__main__":
    main()