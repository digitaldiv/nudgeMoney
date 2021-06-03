from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Float, Date
from sqlalchemy import BigInteger
import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_name = Column(String(40), nullable = False)
    user_pwd = Column(String(40), nullable = False)
    date_signed = Column(Date, nullable = False, default=datetime.datetime.utcnow())
    status = Column (String(40), nullable=False)
    user_email = Column(String(40), nullable = False)
    user_phone = Column(String(40), nullable = False)
    portfolios = db.relationship('Portfolio', backref='user', lazy=True)

    def check_password(self, pwd):
        if self.user_pwd == pwd:
            return True
        else:
            return False


class Portfolio (db.Model):
    __tablename__ = 'portfolio'
    id = Column(Integer, primary_key=True, autoincrement=True)
    portfolio_title = Column(String(60), nullable = False)
    portfolio_desc = Column(String(120), nullable = False)
    date_created = Column(Date, nullable = False, default=datetime.datetime.utcnow())
    date_updated = Column(Date, nullable = True)
    date_created = Column(Date, nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    stocks = db.relationship('Stock', backref='portfolio', lazy=True)

class Stock(db.Model):
    __tablename__ = 'stock'
    id = Column(Integer, primary_key=True, autoincrement=True)
    stock_symbol = Column(String(40))
    stock_company_URL = Column(String(40))
    purchase_date = Column(Date, nullable = False)
    purchase_price = Column (Float, nullable=False)
    volume = Column (Float, nullable=False)
    latest_price = Column (Float, nullable=False)
    cost_basis = Column (Float, nullable=False)
    gain_loss = Column (Float, nullable=False)
    portfolio_id = db.Column(db.Integer, db.ForeignKey('portfolio.id'), nullable=False)

# Step 3: Create a model
class FinanceData (db.Model):
    __tablename__ = 'snpcompanies'

    id = Column ( Integer, primary_key=True)
    Symbol = Column (String(10), nullable=True)
    Name = Column ( String(100), nullable=True)
    Sector= Column ( String(100), nullable=True)
    Price = Column ( Float, nullable=True )
    PricePerEarnings= Column ( Float, nullable=True )
    Dividend_Yield= Column ( Float, nullable=True )
    EarningsPerShare= Column ( Float, nullable=True )
    P52_Week_Low= Column ( Float, nullable=True)
    P52_Week_High= Column ( Float, nullable=True)
    Market_Cap= Column ( BigInteger, nullable=True )
    EBITDA= Column ( Float, nullable=True )
    PricePerSales= Column ( Float, nullable=True )
    PricePerBook= Column ( Float, default=0, nullable=True )
    SEC_Filings= Column ( String(500), nullable=True )

# Step 3: Create a model
class HistoricalData (db.Model):
    __tablename__ = 'historicaldata'

    id = Column ( Integer, primary_key=True)
    Symbol = Column (String(10), nullable=True)
    TradeDate = Column (Date, nullable=True)
    OpenPrice = Column (Float, nullable=True)
    HiPrice = Column (Float, nullable=True)
    LoPrice = Column (Float, nullable=True)
    ClosePrice = Column (Float, nullable=True)
    AdjClosePrice = Column (Float, nullable=True)
    Volume  = Column (BigInteger,nullable=True)