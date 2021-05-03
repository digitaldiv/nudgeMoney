from flask import Flask, render_template
from models.portfolio import db
from initapp import db_seed, get_historical_data_db, get_historical_data_files
import logging


# ---------------------------
# App initialization 
# ---------------------------
# This 
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
    '''
    This creates a database 
    '''
    db.create_all()
    app.logger.info('Database created')

@app.cli.command('db_seed')
def db_seed_cli():
    dataFile = r'/Users/divpithadia/Downloads/s-and-p-500-companies-financials_zip-2/data/constituents-financials_csv.csv'
    db_seed(dataFile)
    app.logger.info('Database seeded')

@app.cli.command('db_history_db')
def db_history_db():
    app.logger.info('Stock history import into database started.')
    get_historical_data_db ()
    app.logger.info('Stock history imported into database.')

@app.cli.command('db_history_files')
def db_history_files ():
    app.logger.info('Stock history import into CSV files started.')
    get_historical_data_files ()
    app.logger.info('Stock history imported into CSV files.')
        
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
