from flask_script import Manager, prompt_bool
from app import app, db

manager = Manager(app)


@manager.command
def init_db():
    db.create_all()
    print("Database initialized")


@manager.command
def drop_db():
    if prompt_bool("Are you sure you want to delete the database?"):
        db.drop_all()
        print("Database dropped!")


if __name__ == "__main__":
    manager.run()
