from flask_marshmallow import Marshmallow
from models import Stock, FinanceData, User, HistoricalData, Portfolio

ma = Marshmallow() 

# Define Schemas 
class FinanceDataSchema(ma.Schema):
    class Meta:
        fields = ("Symbol","Name","Sector","Price","PricePerEarnings","Dividend_Yield","EarningsPerShare","P52_Week_Low","P52_Week_High","Market_Cap","EBITDA","PricePerSales","PricePerBook","SEC_Filings")
        model = FinanceData

financeDataSchema = FinanceDataSchema()
financeDataSchema = FinanceDataSchema(many=True)

class UserSchema (ma.Schema):
    class Meta:
        fields = ("id","user_name","user_pwd","date_signed","status","user_email","user_phone")
        model = User

userschema = UserSchema ( )
userschema = UserSchema (many=True)

class PortfolioSchema (ma.Schema):
    class Meta:
        #fields = ( "id","stock_symbol","stock_company_URL","purchase_date","purchase_price","volume","latest_price","cost_basis","gain_loss")
        fields = ("id","portfolio_title","portfolio_desc","date_created","date_updated","date_created", "user_id")
        model = Portfolio
        include_fk = True

portfolioschema = PortfolioSchema ( )
portfolioschema = PortfolioSchema (many=True)

class StockSchema (ma.Schema):
    class Meta:
        fields = ( "id","stock_symbol","stock_company_URL","purchase_date","purchase_price","volume","latest_price","cost_basis","gain_loss", "portfolio_id")
        model = Stock
        include_fk = True

stockschema = StockSchema ( )
stockschema = StockSchema (many=True)