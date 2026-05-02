# Contact Management System

This is a simple command-line contact manager built in Python as part of my internship task.

The idea was to practice working with data (JSON/CSV), handling user input, and building a small but useful CLI application.



## Features

- Add new contacts
- View all contacts in table format
- Search contacts (name, phone, email)
- Filter by city, company, or favorites
- Update existing contact details
- Delete contacts with confirmation
- Mark/unmark favorite contacts
- Import and export contacts (CSV)
- Data is automatically saved in a JSON file



## Requirements

- Python 3.7 or above
- No external libraries needed



## How to run

Open terminal in the project folder and run:

python contacts.py



## Files

- contacts.py → main program  
- contacts.json → stores contacts data  
- contacts_export.csv → created when exporting  


## Notes

- You can search using name or first few characters of ID  
- Press Enter during update to keep existing value  
- Basic validation is applied for phone and email  
- Duplicate contacts are skipped during CSV import  



## About

This project was built as part of a Python internship task to practice file handling, data management, and CLI-based application development.