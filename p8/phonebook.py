from connect import connect

#1
def create_table():
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
        DROP TABLE IF EXISTS phonebook;

        CREATE TABLE phonebook (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            surname VARCHAR(100),
            phone VARCHAR(20) NOT NULL
        );
    """)

    conn.commit()
    cur.close()
    conn.close()
    print("Table created.")

#2,3
def execute_sql_file(filename):
    conn = connect()
    cur = conn.cursor()

    with open(filename, "r", encoding="utf-8") as file:
        sql = file.read()
        cur.execute(sql)

    conn.commit()
    cur.close()
    conn.close()
    print(filename, "executed.")

#4
def show_all_contacts():
    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT * FROM phonebook ORDER BY id;")
    rows = cur.fetchall()

    for row in rows:
        print(row)

    cur.close()
    conn.close()

#5
def search_contacts():
    pattern = input("Enter pattern: ")

    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT * FROM search_contacts(%s);", (pattern,))
    rows = cur.fetchall()

    for row in rows:
        print(row)

    cur.close()
    conn.close()

#6
def show_paginated_contacts():
    limit = int(input("Enter limit: "))
    offset = int(input("Enter offset: "))

    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT * FROM get_contacts_paginated(%s, %s);", (limit, offset))
    rows = cur.fetchall()

    for row in rows:
        print(row)

    cur.close()
    conn.close()

#7_
def upsert_contact():
    name = input("Enter name: ")
    surname = input("Enter surname: ")
    phone = input("Enter phone: ")

    conn = connect()
    cur = conn.cursor()

    cur.execute("CALL upsert_contact(%s, %s, %s);", (name, surname, phone))

    conn.commit()
    cur.close()
    conn.close()
    print("Contact inserted or updated.")

#8_
def insert_many_contacts():
    n = int(input("How many contacts: "))

    names = []
    surnames = []
    phones = []

    for i in range(n):
        print("Contact", i + 1)
        name = input("Enter name: ")
        surname = input("Enter surname: ")
        phone = input("Enter phone: ")

        names.append(name)
        surnames.append(surname)
        phones.append(phone)

    conn = connect()
    cur = conn.cursor()

    cur.execute("CALL insert_many_contacts(%s, %s, %s);", (names, surnames, phones))

    conn.commit()
    cur.close()
    conn.close()
    print("Many contacts inserted.")

#9
def delete_contact():
    value = input("Enter name or phone: ")

    conn = connect()
    cur = conn.cursor()

    cur.execute("CALL delete_contact(%s);", (value,))

    conn.commit()
    cur.close()
    conn.close()
    print("Contact deleted.")


def menu():
    while True:
        print("\n--- PHONEBOOK MENU ---")
        print("1. Create table")
        print("2. Execute functions.sql")
        print("3. Execute procedures.sql")
        print("4. Show all contacts")
        print("5. Search contacts by pattern")
        print("6. Show contacts with pagination")
        print("7. Insert or update contact")
        print("8. Insert many contacts")
        print("9. Delete contact by name or phone")
        print("0. Exit")

        choice = input("Choose: ")

        if choice == "1":
            create_table()
        elif choice == "2":
            execute_sql_file("functions.sql")
        elif choice == "3":
            execute_sql_file("procedures.sql")
        elif choice == "4":
            show_all_contacts()
        elif choice == "5":
            search_contacts()
        elif choice == "6":
            show_paginated_contacts()
        elif choice == "7":
            upsert_contact()
        elif choice == "8":
            insert_many_contacts()
        elif choice == "9":
            delete_contact()
        elif choice == "0":
            print("Goodbye")
            break
        else:
            print("Invalid choice")


menu()