from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Float, Date
from sqlalchemy import BigInteger

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'Users'
    id = Column(Integer, primary_key=True)
    user_name = Column(String(40), nullable = False)
    user_pwd = Column(String(40), nullable = False)
    date_signed = Column(Date, nullable = False)
    status = Column (String(40), nullable=False)
    user_email = Column(String(40), nullable = False)
    user_phone = Column(String(40), nullable = False)
    

class Stock(db.Model):
    __tablename__ = 'Stocks'
    id = Column(Integer, primary_key=True)
    stock_symbol = Column(String(40))
    stock_company_URL = Column(String(40))
    purchase_date = Column(Date, nullable = False)
    purchase_price = Column (Float, nullable=False)
    volume = Column (Float, nullable=False)
    latest_price = Column (Float, nullable=False)
    cost_basis = Column (Float, nullable=False)
    gain_loss = Column (Float, nullable=False)


# Step 3: Create a model
class FinanceData (db.Model):
    __tablename__ = 'FinanceData'

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
    __tablename__ = 'HistoricalData'

    id = Column ( Integer, primary_key=True)
    Symbol = Column (String(10), nullable=True)
    TradeDate = Column (Date, nullable=True)
    OpenPrice = Column (Float, nullable=True)
    HiPrice = Column (Float, nullable=True)
    LoPrice = Column (Float, nullable=True)
    ClosePrice = Column (Float, nullable=True)
    AdjClosePrice = Column (Float, nullable=True)
    Volume  = Column (BigInteger,nullable=True)