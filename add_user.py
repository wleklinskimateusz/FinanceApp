from getpass import getpass

from app import db
from flaskr.models import User

username = input("Username: ")
password = getpass("Password: ")
repeat_password = getpass("Repeat password: ")
if password != repeat_password:
    while password != repeat_password:
        print("Passwords are not the same")
        password = getpass("Password: ")
        repeat_password = getpass("Repeat password: ")

user = User(username=username)
user.set_password(password)
user.admin = True
user.photo = input("Name of a photo file: ")
db.session.add(user)
try:
    db.session.commit()
    print("Admin added successfully!")
except:
    db.session.rollback()
    print("Adding failed :(")
