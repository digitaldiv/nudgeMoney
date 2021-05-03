from flask import Flask, render_template
from models.portfolio import db, Stock, FinanceData
from initapp import db_seed, get_historical_data, get_history2
import logging
import pandas as pd
import numpy as np

# ---------------------------
# App initialization 
# ---------------------------
app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# ---------------------------
# Logging initialization 
# ---------------------------
logging.basicConfig(filename='app.log', level=logging.DEBUG)

# ---------------------------
# Database initialization 
# ---------------------------
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///myDB.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root2:password@localhost/nudgeM'
db.init_app(app)

# ---------------------------
# Command Line initialization 
# ---------------------------
# call flask db_create on terminal
@app.cli.command('db_create')
def db_create():
    db.create_all()
    app.logger.info('Database created')

@app.cli.command('db_seed')
def db_seed_cli():
    dataFile = r'/Users/divpithadia/Downloads/s-and-p-500-companies-financials_zip-2/data/constituents-financials_csv.csv'
    db_seed(dataFile)
    app.logger.info('Database seeded')

@app.cli.command('db_history')
def db_history_all():
    #dataFile = r'/Users/divpithadia/Downloads/s-and-p-500-companies-financials_zip-2/data/constituents-financials_csv.csv'
    get_historical_data ()
    app.logger.info('Stock history files retreievd')

@app.cli.command('db_history_test_a')
def db_history_test_a():
    #dataFile = r'/Users/divpithadia/Downloads/s-and-p-500-companies-financials_zip-2/data/constituents-financials_csv.csv'
    get_history2 ('a')
    app.logger.info('History Test for A Completed')
        
# ---------------------------
#     Routes  
# ---------------------------
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/portfolio')
def portfolio():
    return render_template('portfolio.html')

# ---------------------------
# Run app   
# ---------------------------
if __name__ == '__main__':
    app.run(debug=True, port=8080)
