import csv
from connect import connect


def create_table():
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS phonebook (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            phone VARCHAR(20) NOT NULL,
            email VARCHAR(100)
        );
    """)

    conn.commit()
    cur.close()
    conn.close()
    print("Table created.")


#2

def insert_from_csv():
    conn = connect()
    cur = conn.cursor()

    with open("contacts.csv", "r", encoding="utf-8") as file:
        reader = csv.reader(file)
        for row in reader:
            name, phone, email = row
            cur.execute(
                "INSERT INTO phonebook (name, phone, email) VALUES (%s, %s, %s)",
                (name, phone, email)
            )

    conn.commit()
    cur.close()
    conn.close()
    print("Data inserted from CSV.")


#3

def insert_from_console():
    name = input("Enter name: ")
    phone = input("Enter phone: ")
    email = input("Enter email: ")

    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO phonebook (name, phone, email) VALUES (%s, %s, %s)",
        (name, phone, email)
    )

    conn.commit()
    cur.close()
    conn.close()
    print("Contact added.")


#4

def update_contact():
    old_name = input("Enter contact name to update: ")
    new_name = input("Enter new name: ")
    new_phone = input("Enter new phone: ")

    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "UPDATE phonebook SET name = %s, phone = %s WHERE name = %s",
        (new_name, new_phone, old_name)
    )

    conn.commit()
    cur.close()
    conn.close()
    print("Contact updated.")



#5

def query_all():
    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT * FROM phonebook")
    rows = cur.fetchall()

    for row in rows:
        print(row)

    cur.close()
    conn.close()



#6

def query_by_name():
    name = input("Enter name: ")

    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT * FROM phonebook WHERE name = %s", (name,))
    rows = cur.fetchall()

    for row in rows:
        print(row)

    cur.close()
    conn.close()

#7

def query_by_phone_prefix():
    prefix = input("Enter phone prefix: ")

    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT * FROM phonebook WHERE phone LIKE %s", (prefix + "%",))
    rows = cur.fetchall()

    for row in rows:
        print(row)

    cur.close()
    conn.close()

#8

def delete_by_name():
    name = input("Enter name to delete: ")

    conn = connect()
    cur = conn.cursor()

    cur.execute("DELETE FROM phonebook WHERE name = %s", (name,))

    conn.commit()
    cur.close()
    conn.close()
    print("Deleted by name.")

#9

def delete_by_phone():
    phone = input("Enter phone to delete: ")

    conn = connect()
    cur = conn.cursor()

    cur.execute("DELETE FROM phonebook WHERE phone = %s", (phone,))

    conn.commit()
    cur.close()
    conn.close()
    print("Deleted by phone.")

#10
def menu():
    while True:
        print("\n1. Create table")
        print("2. Insert from CSV")
        print("3. Insert from console")
        print("4. Update contact")
        print("5. Show all contacts")
        print("6. Search by name")
        print("7. Search by phone prefix")
        print("8. Delete by name")
        print("9. Delete by phone")
        print("0. Exit")

        choice = input("Choose: ")

        if choice == "1":
            create_table()
        elif choice == "2":
            insert_from_csv()
        elif choice == "3":
            insert_from_console()
        elif choice == "4":
            update_contact()
        elif choice == "5":
            query_all()
        elif choice == "6":
            query_by_name()
        elif choice == "7":
            query_by_phone_prefix()
        elif choice == "8":
            delete_by_name()
        elif choice == "9":
            delete_by_phone()
        elif choice == "0":
            print("Goodbye")
            break
        else:
            print("Invalid choice")


menu()