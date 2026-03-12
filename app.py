from flask_sqlalchemy import SQLAlchemy
from flask import render_template, request, session, flash, Flask, redirect, url_for
from datetime import timedelta
from datetime import datetime, date
from flask_migrate import Migrate


# setting up flask app
app = Flask(__name__)
app.secret_key = 'cake'
app.permanent_session_lifetime = timedelta(minutes=5)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# setting up database
db = SQLAlchemy(app)
class task(db.Model):
    id = db.Column("id", db.Integer, primary_key = True)
    task = db.Column("task", db.String(1200), nullable = False)
    date = db.Column("date", db.Date, nullable = False)
    expired = db.Column("expired",db.Boolean, nullable = False)


migrate = Migrate(app, db)

@app.route("/")
def home():
    return render_template("welcome.html")

@app.route("/welcome")
def welcome():
    return render_template("welcome.html")

@app.route('/main', methods=['GET'])
def main():
    return render_template('main.html')

@app.route("/show", methods = ["GET"])
def show():
    t = task.query.all()
    tasks = task.query.all()
    for tuple in tasks:
        if tuple.date < date.today():
            tuple.expired = True
            db.session.commit()
        else:
            tuple.expired = False
            db.session.commit()
    return render_template("show.html", t = t)

@app.route('/delete/<int:id>')
def delete(id):
    t = task.query.get_or_404(id)
    
    db.session.delete(t)
    db.session.commit()
    return redirect(url_for('show'))

@app.route("/add", methods = ["GET" ,"POST"])
def add():
    if request.method == "POST":
        tsk = request.form.get("task")
        d  = request.form.get("date")
        exp = False
        if d:
            d = datetime.strptime(d, '%Y-%m-%d').date()
            if d < date.today():
               exp = True

        if tsk and d:
            t = task(task = tsk , date = d, expired = exp)
            db.session.add(t)
            db.session.commit()
            return redirect("./main")   
        else:
            print("couldnt add task")
            return redirect("/main")
    else:
        return redirect("/main")
    
@app.route('/changeDate/<int:id>', methods= ['POST','GET'])
def changeDate(id):
    if request.method == 'POST':
        date = request.form.get("ndate")
        date = datetime.strptime(date, '%Y-%m-%d').date()
        t = task.query.get_or_404(id)
        if date:
            t.date = date
            db.session.commit()
        else:
            return redirect('welcome')
    else:
        return redirect('welcome')
    return redirect(url_for('show', t = t))            
    
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        for t in task.query.all():
            print(t.id, t.task, t.date)
    app.run(debug=True)