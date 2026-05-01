import csv
import json
from connect import connect

#1-2
def run_sql_file(filename):
    conn = connect()
    cur = conn.cursor()

    with open(filename, "r", encoding="utf-8") as file:
        sql = file.read()

    cur.execute(sql)
    conn.commit()

    cur.close()
    conn.close()

    print(f"{filename} executed successfully!")

#3
def add_contact():
    name = input("Name: ")
    email = input("Email: ")
    birthday = input("Birthday (YYYY-MM-DD): ")
    group_name = input("Group: ")

    conn = connect()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO groups(name)
        VALUES (%s)
        ON CONFLICT (name) DO NOTHING;
    """, (group_name,))

    cur.execute("""
        SELECT id FROM groups
        WHERE name = %s;
    """, (group_name,))

    group_id = cur.fetchone()[0]

    cur.execute("""
        INSERT INTO contacts(name, email, birthday, group_id)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (name) DO NOTHING;
    """, (name, email, birthday, group_id))

    conn.commit()
    cur.close()
    conn.close()

    print("Contact added!")


def show_all_contacts():
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            contacts.id,
            contacts.name,
            contacts.email,
            contacts.birthday,
            groups.name,
            contacts.created_at
        FROM contacts
        LEFT JOIN groups ON contacts.group_id = groups.id
        ORDER BY contacts.id;
    """)

    rows = cur.fetchall()

    for row in rows:
        print(row)

    cur.close()
    conn.close()


def add_phone_to_contact():
    contact_name = input("Contact name: ")
    phone = input("Phone: ")
    phone_type = input("Phone type (home/work/mobile): ")

    conn = connect()
    cur = conn.cursor()

    cur.execute("""
        CALL add_phone(%s, %s, %s);
    """, (contact_name, phone, phone_type))

    conn.commit()
    cur.close()
    conn.close()

    print("Phone added!")


def move_contact_to_group():
    contact_name = input("Contact name: ")
    group_name = input("New group: ")

    conn = connect()
    cur = conn.cursor()

    cur.execute("""
        CALL move_to_group(%s, %s);
    """, (contact_name, group_name))

    conn.commit()
    cur.close()
    conn.close()

    print("Contact moved to group!")


def search_contacts():
    query = input("Search: ")

    conn = connect()
    cur = conn.cursor()

    cur.execute("""
        SELECT * FROM search_contacts(%s);
    """, (query,))

    rows = cur.fetchall()

    for row in rows:
        print(row)

    cur.close()
    conn.close()


def filter_by_group():
    group_name = input("Group name: ")

    conn = connect()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            contacts.id,
            contacts.name,
            contacts.email,
            contacts.birthday,
            groups.name
        FROM contacts
        LEFT JOIN groups ON contacts.group_id = groups.id
        WHERE groups.name ILIKE %s;
    """, (group_name,))

    rows = cur.fetchall()

    for row in rows:
        print(row)

    cur.close()
    conn.close()


def search_by_email():
    email_part = input("Email search: ")

    conn = connect()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            id,
            name,
            email,
            birthday
        FROM contacts
        WHERE email ILIKE %s;
    """, ('%' + email_part + '%',))

    rows = cur.fetchall()

    for row in rows:
        print(row)

    cur.close()
    conn.close()


def sort_contacts():
    print("1. Sort by name")
    print("2. Sort by birthday")
    print("3. Sort by created date")

    choice = input("Choose: ")

    if choice == "1":
        order_column = "contacts.name"
    elif choice == "2":
        order_column = "contacts.birthday"
    elif choice == "3":
        order_column = "contacts.created_at"
    else:
        print("Wrong choice")
        return

    conn = connect()
    cur = conn.cursor()

    query = f"""
        SELECT
            contacts.id,
            contacts.name,
            contacts.email,
            contacts.birthday,
            groups.name,
            contacts.created_at
        FROM contacts
        LEFT JOIN groups ON contacts.group_id = groups.id
        ORDER BY {order_column};
    """

    cur.execute(query)
    rows = cur.fetchall()

    for row in rows:
        print(row)

    cur.close()
    conn.close()


def pagination():
    limit = 3
    offset = 0

    while True:
        conn = connect()
        cur = conn.cursor()

        cur.execute("""
            SELECT
                contacts.id,
                contacts.name,
                contacts.email,
                contacts.birthday,
                groups.name
            FROM contacts
            LEFT JOIN groups ON contacts.group_id = groups.id
            ORDER BY contacts.id
            LIMIT %s OFFSET %s;
        """, (limit, offset))

        rows = cur.fetchall()

        print("\n--- Page ---")
        for row in rows:
            print(row)

        cur.close()
        conn.close()

        command = input("next / prev / quit: ")

        if command == "next":
            offset += limit
        elif command == "prev":
            offset -= limit
            if offset < 0:
                offset = 0
        elif command == "quit":
            break
        else:
            print("Wrong command")


def export_to_json():
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            contacts.id,
            contacts.name,
            contacts.email,
            contacts.birthday,
            groups.name
        FROM contacts
        LEFT JOIN groups ON contacts.group_id = groups.id
        ORDER BY contacts.id;
    """)

    contacts = cur.fetchall()

    result = []

    for contact in contacts:
        contact_id = contact[0]

        cur.execute("""
            SELECT phone, phone_type
            FROM phones
            WHERE contact_id = %s;
        """, (contact_id,))

        phones = cur.fetchall()

        result.append({
            "id": contact[0],
            "name": contact[1],
            "email": contact[2],
            "birthday": str(contact[3]) if contact[3] else None,
            "group": contact[4],
            "phones": [
                {
                    "phone": phone[0],
                    "phone_type": phone[1]
                }
                for phone in phones
            ]
        })

    with open("contacts_export.json", "w", encoding="utf-8") as file:
        json.dump(result, file, indent=4, ensure_ascii=False)

    cur.close()
    conn.close()

    print("Exported to contacts_export.json")


def import_from_json():
    filename = input("JSON filename: ")

    with open(filename, "r", encoding="utf-8") as file:
        data = json.load(file)

    conn = connect()
    cur = conn.cursor()

    for item in data:
        name = item["name"]
        email = item["email"]
        birthday = item["birthday"]
        group_name = item["group"]

        cur.execute("""
            SELECT id FROM contacts
            WHERE name = %s;
        """, (name,))

        existing = cur.fetchone()

        if existing:
            answer = input(f"{name} already exists. skip/overwrite: ")

            if answer == "skip":
                continue

            elif answer == "overwrite":
                contact_id = existing[0]

                cur.execute("""
                    DELETE FROM phones
                    WHERE contact_id = %s;
                """, (contact_id,))

                cur.execute("""
                    INSERT INTO groups(name)
                    VALUES (%s)
                    ON CONFLICT (name) DO NOTHING;
                """, (group_name,))

                cur.execute("""
                    SELECT id FROM groups
                    WHERE name = %s;
                """, (group_name,))

                group_id = cur.fetchone()[0]

                cur.execute("""
                    UPDATE contacts
                    SET email = %s,
                        birthday = %s,
                        group_id = %s
                    WHERE id = %s;
                """, (email, birthday, group_id, contact_id))

            else:
                print("Wrong answer, skipped")
                continue

        else:
            cur.execute("""
                INSERT INTO groups(name)
                VALUES (%s)
                ON CONFLICT (name) DO NOTHING;
            """, (group_name,))

            cur.execute("""
                SELECT id FROM groups
                WHERE name = %s;
            """, (group_name,))

            group_id = cur.fetchone()[0]

            cur.execute("""
                INSERT INTO contacts(name, email, birthday, group_id)
                VALUES (%s, %s, %s, %s)
                RETURNING id;
            """, (name, email, birthday, group_id))

            contact_id = cur.fetchone()[0]

        for phone_item in item["phones"]:
            cur.execute("""
                INSERT INTO phones(contact_id, phone, phone_type)
                VALUES (%s, %s, %s);
            """, (
                contact_id,
                phone_item["phone"],
                phone_item["phone_type"]
            ))

    conn.commit()
    cur.close()
    conn.close()

    print("JSON imported!")


def import_from_csv():
    filename = input("CSV filename: ")

    conn = connect()
    cur = conn.cursor()

    with open(filename, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            name = row["name"]
            email = row["email"]
            birthday = row["birthday"]
            group_name = row["group"]
            phone = row["phone"]
            phone_type = row["phone_type"]

            cur.execute("""
                INSERT INTO groups(name)
                VALUES (%s)
                ON CONFLICT (name) DO NOTHING;
            """, (group_name,))

            cur.execute("""
                SELECT id FROM groups
                WHERE name = %s;
            """, (group_name,))

            group_id = cur.fetchone()[0]

            cur.execute("""
                INSERT INTO contacts(name, email, birthday, group_id)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (name) DO NOTHING;
            """, (name, email, birthday, group_id))

            cur.execute("""
                SELECT id FROM contacts
                WHERE name = %s;
            """, (name,))

            contact_id = cur.fetchone()[0]

            cur.execute("""
                INSERT INTO phones(contact_id, phone, phone_type)
                VALUES (%s, %s, %s);
            """, (contact_id, phone, phone_type))

    conn.commit()
    cur.close()
    conn.close()

    print("CSV imported!")


def menu():
    while True:
        print("\n===== PHONEBOOK MENU =====")
        print("1. Create tables")
        print("2. Create procedures/functions")
        print("3. Add contact")
        print("4. Show all contacts")
        print("5. Add phone")
        print("6. Move contact to group")
        print("7. Search contacts")
        print("8. Filter by group")
        print("9. Search by email")
        print("10. Sort contacts")
        print("11. Pagination")
        print("12. Export to JSON")
        print("13. Import from JSON")
        print("14. Import from CSV")
        print("0. Exit")

        choice = input("Choose: ")

        if choice == "1":
            run_sql_file("schema.sql")
        elif choice == "2":
            run_sql_file("procedures.sql")
        elif choice == "3":
            add_contact()
        elif choice == "4":
            show_all_contacts()
        elif choice == "5":
            add_phone_to_contact()
        elif choice == "6":
            move_contact_to_group()
        elif choice == "7":
            search_contacts()
        elif choice == "8":
            filter_by_group()
        elif choice == "9":
            search_by_email()
        elif choice == "10":
            sort_contacts()
        elif choice == "11":
            pagination()
        elif choice == "12":
            export_to_json()
        elif choice == "13":
            import_from_json()
        elif choice == "14":
            import_from_csv()
        elif choice == "0":
            break
        else:
            print("Wrong choice")


menu()