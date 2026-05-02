# Contact Management System (CLI)
# Internship Task - Python Developer

import json
import csv
import os
import re
import uuid
from datetime import datetime

DATA_FILE = "contacts.json"
CSV_FILE = "contacts_export.csv"


def load_contacts():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []


def save_contacts(contacts):
    with open(DATA_FILE, "w") as f:
        json.dump(contacts, f, indent=4)


def is_valid_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w{2,}$'
    return re.match(pattern, email) is not None


def is_valid_phone(phone):
    pattern = r'^\+?\d{10,15}$'
    return re.match(pattern, phone) is not None


def input_required(prompt):
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("This field cannot be empty.")


def print_header(title):
    print("\n" + "-" * 50)
    print(title)
    print("-" * 50)


def print_contacts_table(contacts):
    if not contacts:
        print("\nNo contacts found.")
        return

    col = {"id": 6, "name": 20, "phone": 15, "email": 25, "city": 12, "company": 15}

    header = (
        f"{'ID':<{col['id']}} "
        f"{'Name':<{col['name']}} "
        f"{'Phone':<{col['phone']}} "
        f"{'Email':<{col['email']}} "
        f"{'City':<{col['city']}} "
        f"{'Company':<{col['company']}}"
    )

    print("\n" + "-" * len(header))
    print(header)
    print("-" * len(header))

    for c in contacts:
        print(
            f"{c['id'][:6]:<{col['id']}} "
            f"{c['name'][:col['name']]:<{col['name']}} "
            f"{c['phone'][:col['phone']]:<{col['phone']}} "
            f"{c['email'][:col['email']]:<{col['email']}} "
            f"{c['city'][:col['city']]:<{col['city']}} "
            f"{c['company'][:col['company']]:<{col['company']}}"
        )

    print("-" * len(header))
    print(f"Total: {len(contacts)}\n")


# Add contact
def add_contact(contacts):
    print_header("Add Contact")

    name = input_required("Name: ")

    while True:
        phone = input_required("Phone: ")
        if is_valid_phone(phone):
            break
        print("Invalid phone number.")

    while True:
        email = input_required("Email: ")
        if is_valid_email(email):
            break
        print("Invalid email.")

    city = input_required("City: ")
    company = input_required("Company: ")

    contact = {
        "id": str(uuid.uuid4()),
        "name": name,
        "phone": phone,
        "email": email,
        "city": city,
        "company": company,
        "favorite": False,
        "added_on": datetime.now().strftime("%Y-%m-%d %H:%M")
    }

    contacts.append(contact)
    save_contacts(contacts)

    print(f"\nContact added: {name}")


# View contacts
def view_contacts(contacts):
    print_header("All Contacts")

    if not contacts:
        print("No contacts available.")
        return

    print("Sort by: 1) Name  2) Recent  3) None")
    choice = input("Choice: ").strip()

    data = contacts[:]

    if choice == "1":
        data.sort(key=lambda x: x["name"].lower())
    elif choice == "2":
        data.sort(key=lambda x: x.get("added_on", ""), reverse=True)

    page_size = 10
    page = 0
    total = len(data)
    pages = (total + page_size - 1) // page_size

    while True:
        start = page * page_size
        end = start + page_size

        print_contacts_table(data[start:end])
        print(f"Page {page+1}/{pages}")

        if pages <= 1:
            break

        nav = input("n-next, p-prev, q-quit: ").lower()
        if nav == "n" and page < pages - 1:
            page += 1
        elif nav == "p" and page > 0:
            page -= 1
        elif nav == "q":
            break


# Search
def search_contacts(contacts):
    print_header("Search")

    print("1) Name  2) Phone  3) Email")
    choice = input("Choice: ").strip()

    if choice not in ("1", "2", "3"):
        print("Invalid choice.")
        return

    query = input_required("Search: ").lower()
    field = {"1": "name", "2": "phone", "3": "email"}[choice]

    results = [c for c in contacts if query in c[field].lower()]

    print_contacts_table(results)


# Filter
def filter_contacts(contacts):
    print_header("Filter")

    print("1) City  2) Company  3) Favorites")
    choice = input("Choice: ").strip()

    if choice == "1":
        value = input_required("City: ").lower()
        results = [c for c in contacts if value in c["city"].lower()]
    elif choice == "2":
        value = input_required("Company: ").lower()
        results = [c for c in contacts if value in c["company"].lower()]
    elif choice == "3":
        results = [c for c in contacts if c.get("favorite")]
    else:
        print("Invalid choice.")
        return

    print_contacts_table(results)


# Update
def update_contact(contacts):
    print_header("Update Contact")

    query = input_required("Enter name or ID: ").lower()

    matches = [c for c in contacts if query in c["name"].lower() or c["id"].startswith(query)]

    if not matches:
        print("No match found.")
        return

    contact = matches[0]

    for field in ["name", "phone", "email", "city", "company"]:
        new_val = input(f"{field} ({contact[field]}): ").strip()
        if new_val:
            if field == "phone" and not is_valid_phone(new_val):
                print("Invalid phone.")
                continue
            if field == "email" and not is_valid_email(new_val):
                print("Invalid email.")
                continue
            contact[field] = new_val

    save_contacts(contacts)
    print("Updated successfully.")


# Delete
def delete_contact(contacts):
    print_header("Delete Contact")

    query = input_required("Enter name or ID: ").lower()

    matches = [c for c in contacts if query in c["name"].lower() or c["id"].startswith(query)]

    if not matches:
        print("No match found.")
        return

    print_contacts_table(matches)

    confirm = input("Type 'yes' to delete: ").lower()
    if confirm != "yes":
        print("Cancelled.")
        return

    ids = {c["id"] for c in matches}
    contacts[:] = [c for c in contacts if c["id"] not in ids]

    save_contacts(contacts)
    print("Deleted.")


# Export
def export_to_csv(contacts):
    print_header("Export CSV")

    if not contacts:
        print("No data.")
        return

    fields = ["id", "name", "phone", "email", "city", "company", "favorite", "added_on"]

    with open(CSV_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(contacts)

    print("Exported.")


# Import
def import_from_csv(contacts):
    print_header("Import CSV")

    filename = input_required("File name: ")

    if not os.path.exists(filename):
        print("File not found.")
        return

    existing = {c["phone"] for c in contacts}
    added = 0

    with open(filename, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get("phone") in existing:
                continue

            row["id"] = row.get("id") or str(uuid.uuid4())
            row["favorite"] = row.get("favorite") == "True"
            row["added_on"] = row.get("added_on") or datetime.now().strftime("%Y-%m-%d %H:%M")

            contacts.append(row)
            existing.add(row["phone"])
            added += 1

    save_contacts(contacts)
    print(f"Imported {added} contacts.")


# Favorite toggle
def toggle_favorite(contacts):
    print_header("Toggle Favorite")

    query = input_required("Enter name or ID: ").lower()

    matches = [c for c in contacts if query in c["name"].lower() or c["id"].startswith(query)]

    if not matches:
        print("No match found.")
        return

    contact = matches[0]
    contact["favorite"] = not contact.get("favorite", False)

    save_contacts(contacts)
    print("Updated.")


def print_menu():
    print("""
Contact Management System

1. Add Contact
2. View Contacts
3. Search
4. Filter
5. Update
6. Delete
7. Export CSV
8. Import CSV
9. Toggle Favorite
0. Exit
""")


def main():
    contacts = load_contacts()
    print(f"Loaded {len(contacts)} contacts.")

    while True:
        print_menu()
        choice = input("Select option: ").strip()

        try:
            if choice == "1": add_contact(contacts)
            elif choice == "2": view_contacts(contacts)
            elif choice == "3": search_contacts(contacts)
            elif choice == "4": filter_contacts(contacts)
            elif choice == "5": update_contact(contacts)
            elif choice == "6": delete_contact(contacts)
            elif choice == "7": export_to_csv(contacts)
            elif choice == "8": import_from_csv(contacts)
            elif choice == "9": toggle_favorite(contacts)
            elif choice == "0":
                print("Goodbye.")
                break
            else:
                print("Invalid option.")

        except KeyboardInterrupt:
            print("\nInterrupted.")
        except Exception as e:
            print(f"Error: {e}")

        input("\nPress Enter to continue...")


if __name__ == "__main__":
    main()