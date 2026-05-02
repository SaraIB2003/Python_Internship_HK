# Multi User Authentication System

This is a simple command-line authentication system built in Python as part of my internship task.

The project focuses on handling multiple users, login systems, and basic security concepts like password hashing and account locking.


## What it does

- Register new users (username, email, password)
- Login using username or email
- Passwords are stored as hashes (not plain text)
- Accounts get locked after multiple wrong login attempts
- Reset password with basic verification
- Delete your own account
- Admin can manage users (view, delete, unlock, change roles)



## Requirements

- Python 3.7 or above
- No external libraries used



## How to run

Open terminal in the project folder and run:

python auth.py


## Files

- auth.py → main program  
- users.json → stores all user data  


## Notes

- First registered user becomes Admin automatically  
- Username and email must be unique  
- Password must follow basic rules (length, uppercase, number, etc.)  
- Accounts are locked after 3 failed login attempts  



## About

This project was created as part of a Python internship task to practice authentication systems, file handling, and CLI-based applications.