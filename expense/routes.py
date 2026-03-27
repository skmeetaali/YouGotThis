from extension import db
from .models import expense
from datetime import datetime, date
from flask import url_for, request
from flask import render_template, request, session, flash, Flask, redirect, url_for, Blueprint
from sqlalchemy import func
from collections import defaultdict


exp = Blueprint("exp", __name__, template_folder='templates')

@exp.route("/expmain", methods=['GET'])
def expmain():
    return render_template("expense/note.html")

@exp.route('/addexp', methods = ['POST', 'GET'])
def addexp():
    if request.method == "POST":
        date = request.form.get("date")
        amount = request.form.get("amount")
        item = request.form.get("item")
        
        if date:
            date = datetime.strptime(date, '%Y-%m-%d').date()
            
        if date == None:
            date = date.today()
        
        if date  and amount and item:
            e = expense(date = date, amount = amount , item = item)
            db.session.add(e)
            db.session.commit()
            return redirect(url_for("exp.expmain"))   
        else:
            print("cannot add expense")
            return redirect(url_for('todo.welcome'))
        
    else:
        return redirect(url_for("todo.show"))
    
@exp.route("/dashboard", methods = ["GET"])
def dashboard():
    expenses = expense.query.order_by(expense.date.desc()).all()
    grouped_exp = defaultdict(list)
    for exp in expenses:
        grouped_exp[exp.date].append(exp)
    return render_template("expense/dashboard.html", grp = grouped_exp)


@exp.route('/deleteall', methods = ['GET'])
def deleteall():
    expenses = expense.query.all()
    for exp in expenses:
        db.session.delete(exp)
        db.session.commit()
    return redirect(url_for('exp.dashboard'))