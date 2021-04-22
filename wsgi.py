from os import remove, path

from flaskr import create_app, db

app = create_app()
db_name = "flaskr/myDB.db"


@app.cli.command()
def createdb():
    if path.exists(db_name):
        remove(db_name)
        print(db_name + " removed")
    db.create_all()

    query = input("Want to add an admin? (Y/N): ")

    if query.lower() == "y":
        import add_user


if __name__ == "__main__":
    app.run()
