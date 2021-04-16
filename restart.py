from flaskr import db
from os import path, remove
db_name = "myDB.db"

if path.exists(db_name):
    remove(db_name)
    print(db_name + " removed")

db.create_all()

query = input("Want to add an admin? (Y/N): ")


if query.lower() == "y":
    pass


