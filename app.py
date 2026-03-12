from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta
from flask_migrate import Migrate
from flask import Flask
from todo import app


# setting up flask app
app = Flask(__name__)
app.secret_key = 'cake'
app.permanent_session_lifetime = timedelta(minutes=5)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# setting up database
db = SQLAlchemy(app)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

migrate = Migrate(app, db)
