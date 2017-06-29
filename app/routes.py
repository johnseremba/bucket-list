from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy


def create_app():
    return Flask(__name__)

app = create_app()
db = SQLAlchemy(app)


@app.route('/')
def index():
    # admin = User('admin', 'admin@example.com')
    # db.session.add(admin)
    # db.session.commit()
    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)
