from getpass import getpass

from database import SessionLocal
from models import Client
from security import hash_password

with SessionLocal() as db:
    db.add(Client(
        email=input("Email : "),
        hashed_password=hash_password(getpass("Password : ")),
        first_name=input("First name : "),
        last_name=input("Last name : "),
        role="admin",
    ))
    db.commit()
    print("Admin created.")