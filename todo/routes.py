from extension import db
from .models import task
from datetime import datetime, date
from flask import url_for, request
from flask import render_template, request, session, flash, Flask, redirect, url_for, Blueprint

todo = Blueprint("todo", __name__, template_folder='templates')

@todo.route("/")
def home():
    return render_template("welcome.html")

@todo.route("/welcome")
def welcome():
    return render_template("welcome.html")

@todo.route('/main', methods=['GET'])
def main():
    return render_template('todo/main.html')

@todo.route("/show", methods = ["GET"])
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
    return render_template("todo/show.html", t = t)

@todo.route('/delete/<int:id>')
def delete(id):
    t = task.query.get_or_404(id)
    
    db.session.delete(t)
    db.session.commit()
    return redirect(url_for('todo.show'))

@todo.route("/add", methods = ["GET" ,"POST"])
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
            return redirect(url_for("todo.main"))   
        else:
            print("couldnt add task")
            return redirect("/main")
    else:
        return redirect("/main")
    
@todo.route('/changeDate/<int:id>', methods= ['POST','GET'])
def changeDate(id):
    if request.method == 'POST':
        date = request.form.get("ndate")
        date = datetime.strptime(date, '%Y-%m-%d').date()
        t = task.query.get_or_404(id)
        if date:
            t.date = date
            db.session.commit()
        else:
            return redirect(url_for("welcome"))
    else:
        return redirect(url_for("welcome"))
    return redirect(url_for('todo.show', t = t))            
    
