from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta
from flask_migrate import Migrate
from flask import Flask
from todo.routes import todo
from extension import db
from expense.routes import exp


# setting up flask app
app = Flask(__name__)
app.secret_key = 'cake'
app.permanent_session_lifetime = timedelta(minutes=5)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# setting up database
db.init_app(app)
migrate = Migrate(app, db)
app.register_blueprint(todo)
app.register_blueprint(exp)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

