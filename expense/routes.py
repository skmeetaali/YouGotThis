from extension import db
from .models import expense
from datetime import datetime, date
from flask import url_for, request
from flask import render_template, request, session, flash, Flask, redirect, url_for, Blueprint

expense = Blueprint("expense", __name__, template_folder='templates')

@expense.route('/add', methods = ['POST', 'GET'])
def add():
    if request.method == 'POST':
        date = request.form.get("date")
        amount = request.form.get("amount")
        item = request.form.get("item")
        
        d  = datetime.strptime(d, '%Y-%m-%d').date()
        
        if date and amount and item:
            expense = expense(date = date, amount = amount , item = item)
            db.session.add(expense)
            db.session.commit()
        else:
            print("cannot add expense")
            return redirect(url_for('expense.dashboard'))
        
    else:
        return redirect(url_for('todo.welcome'))
    
@expense.route("/dashboard", methods = ["GET"])
def show():
    expenses = expense.query.group_by(expense.date).all()
    return render_template("expense/dashboard", expense = expense)