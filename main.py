from app.data.db import connect_database
from app.data.schema import create_all_tables
from app.data.datasets import get_dataset_by_uploader
from app.services.user_service import register_user, login_user, migrate_users_from_file
from app.data.incidents import insert_incident, get_all_incidents
from app.services.dataset_service import load_csv_to_table
from app.data.tickets import get_tickets_by_status_count, get_high_severity_by_priority, get_assigned_to_with_many_cases
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
    load_csv_to_table(conn, "DATA/datasets_metadata.csv", "datasets_metadata")
    load_csv_to_table(conn, "DATA/cyber_incidents.csv", "cyber_incidents")
    load_csv_to_table(conn, "DATA/it_tickets.csv", "it_tickets")

    # 4. Test authentication
    success, msg = register_user("why", "SecurePass123!", "intern")
    print(msg)

    success, msg = login_user("why", "SecurePass123!")
    print(msg)

    # 5. Test CRUD
    incident_id = insert_incident(
        conn,
        "23",
        "11:00:00",
        "High",
        "Phishing",
        "open",
        "too far spread"
    )
    print(f"Created incident #{incident_id}")

    # 6. Query data
    df = get_all_incidents(conn)
    print(f"Total incidents: {len(df)}")

    print("Tickets by Status:")
    df_by_status = get_tickets_by_status_count(conn)
    print(df_by_status)

    print("\nHigh severity:")
    df_by_severity = get_high_severity_by_priority(conn)
    print(df_by_severity)

    print("\nAssigned to:")
    df_by_assigned_to = get_assigned_to_with_many_cases(conn)
    print(df_by_assigned_to)

    print("\nUploaded By:")
    df_by_uploader = get_dataset_by_uploader(conn)
    print(df_by_uploader)

    conn.close()

if __name__ == "__main__":
    main()