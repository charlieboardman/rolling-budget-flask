from flask import Flask, render_template, request, url_for, flash, redirect
import csv
from collections import deque

def tail_csv(filename, n=5): #Format is: date,amount,vendor,description,new total
    with open(filename, 'r', newline='') as file:
        csv_reader = csv.reader(file)
        return list(deque(csv_reader, n))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'

last_5_txns = tail_csv('txns.csv',5)

@app.route("/", methods=('GET','POST')) #main page
def main_page():
    
    if request.method == 'POST':
        amount = request.form['amount']
        vendor = request.form['vendor']
        desc = request.form['desc']

        if not amount:
            flash('Amount spent is required!')
        elif not desc:
            flash('Description is required!')
        else:
            #add_txn(date,amount,vendor='',desc)
            #return redirect(url_for('index'))
        
            print(amount)
            print(desc)
            
    return render_template('index.html', last_5_txns=last_5_txns)


