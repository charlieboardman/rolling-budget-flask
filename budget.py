from flask import Flask, render_template, request, url_for, flash, redirect
import csv
from collections import deque
from datetime import date
from decimal import Decimal

def tail_csv(filename, n=5): #Format is: date,amount,vendor,description,new total
    with open(filename, 'r', newline='') as file:
        csv_reader = csv.reader(file)
        return list(deque(csv_reader, n))
    
def append_csv(filename, new_row): #new_row is a list: [date,amount,vendor,description,new total]
    with open(filename, 'a', newline='') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow(new_row)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'

@app.route("/", methods=('GET','POST')) #main page
def main_page():
    
    if request.method == 'POST':
        
        last_n_txns = tail_csv('txns.csv',5)
        print('last_n_txns')
        print(last_n_txns)
        current_total = last_n_txns[-1][-1]
        print('current_total')
        print(current_total)
        
        amount_spent = request.form['amount_spent']
        print(f'Amount spent {amount_spent}')
        vendor = request.form['vendor']
        desc = request.form['description']

        if not amount_spent:
            flash('Amount spent is required!')
        elif not desc:
            flash('Description is required!')
        else:
            try:
                float(amount_spent)
            
                if not vendor:
                    vendor = ''
                today = date.today().isoformat()
                new_total = Decimal(current_total) - Decimal(amount_spent)
                append_csv('txns.csv', [today, f'{float(amount_spent):.2f}', vendor, desc, f'{new_total:.2f}'])
            except:
                flash('Amount spent must be numeric')
        
        return redirect(url_for('main_page'))

    elif request.method == 'GET': #Normal loading the page

        last_n_txns = tail_csv('txns.csv',5)
        current_total = last_n_txns[-1][-1]
            
        #Format the numbers
        for row in last_n_txns:
            row[1] = f'${float(row[1]):,.2f}'
            row[4] = f'${float(row[4]):,.2f}'
        
        return render_template('index.html', last_n_txns=last_n_txns)

    else:
        
        return 'GET and POST requests only'

