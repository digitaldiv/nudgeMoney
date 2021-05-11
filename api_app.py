from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource
from flask_marshmallow import Marshmallow
from models.portfolio import db, FinanceData, Stock, User, Portfolio
import logging

# ---------------------------
# App initialization 
# ---------------------------

app = Flask(__name__)

app.config.from_object('config.Config')

api = Api(app) 

# ---------------------------
# Logging initialization 
# ---------------------------
logging.basicConfig(filename='api.log', level=logging.DEBUG)

# ---------------------------
# Database initialization 
# ---------------------------
db.init_app(app)
ma = Marshmallow(app) 

# ---------------------------
# Define Schemas 
# ---------------------------
class FinanceDataSchema(ma.Schema):
    class Meta:
        fields = ("Symbol","Name","Sector","Price","PricePerEarnings","Dividend_Yield","EarningsPerShare","P52_Week_Low","P52_Week_High","Market_Cap","EBITDA","PricePerSales","PricePerBook","SEC_Filings")
        model = FinanceData

financeDataSchema = FinanceDataSchema()
financeDataSchema = FinanceDataSchema(many=True)

class UserSchema (ma.Schema):
    class Meta:
        fields = ("id","user_name","user_pwd","date_signed","status","user_email","user_phone")
        #fields = ( "id","stock_symbol","stock_company_URL","purchase_date","purchase_price","volume","latest_price","cost_basis","gain_loss")
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

# ---------------------------
#  Define API Resources  
# ---------------------------

class FinanceDataListResource(Resource):
    def get(self):
        #stocks = db.session.query(FinanceData).all()
        snpList = FinanceData.query.all()

        return jsonify(financeDataSchema.dump(snpList))

api.add_resource(FinanceDataListResource, '/snpstockslist')

class PortfolioListResource (Resource):
    def get (self):
        portfoliolist = Portfolio.query.all ()
        return jsonify(portfolioschema.dump(portfoliolist)) 

    # Create new portfolio
    def post(self):
        print('Adding new Portfolio')
        app.logger.info(f'Received : {request.json}')
        app.logger.info(f'Received : {request.get_json()}')

        new_portfolio = Portfolio ( id=request.json["id"],
                    portfolio_title = request.json["portfolio_title"],
                    portfolio_desc  = request.json["portfolio_desc"],
                    date_created = request.json["date_created"],
                    date_updated = request.json["date_updated"],
                    user_id = request.json["user_id"]
                )
        
        db.session.add(new_portfolio)
        db.session.commit()
        
        return stockschema.dump([new_portfolio])

api.add_resource (PortfolioListResource, '/portfolios' )

class PortfolioResource (Resource):
    def get (self, portfolio_id):
        portfolio = Portfolio.query.get_or_404 (portfolio_id)
        app.logger.info (portfolio)
        return portfolioschema.dump([portfolio])
        # return jsonify(stockschema.dump(stock)) 

    def patch(self, portfolio_id):
        portfolio = Portfolio.query.get_or_404(portfolio_id)
        '''
        if 'title' in request.json:
            post.title = request.json['title']
        if 'content' in request.json:
            post.content = request.json['content']
        '''
        db.session.commit()
        return portfolioschema.dump(portfolio)

    def delete(self, portfolio_id):
        portfolio = Portfolio.query.get_or_404(portfolio_id)
        db.session.delete(portfolio)
        db.session.commit()
        return '', 204

api.add_resource (PortfolioResource, '/portfolio/<int:portfolio_id>' )


class StockListResource (Resource):
    def get (self):
        stockslist = Stock.query.all ()
        return jsonify(stockschema.dump(stockslist)) 

    # Create new stock
    def post(self):
        print('Adding new Stock')
        app.logger.info(f'Received : {request.json}')
        app.logger.info(f'Received : {request.get_json()}')

        new_stock = Stock(id	=request.json["id"],
                        stock_symbol	=request.json["stock_symbol"],
                        stock_company_URL	=request.json["stock_company_URL"],
                        purchase_date	=request.json["purchase_date"],
                        purchase_price	=request.json["purchase_price"],
                        volume	=request.json["volume"],
                        latest_price	=request.json["latest_price"],
                        cost_basis	=request.json["cost_basis"],
                        gain_loss	=request.json["gain_loss"] 
        )
        db.session.add(new_stock)
        db.session.commit()
        
        return stockschema.dump([new_stock])


api.add_resource (StockListResource, '/stocks' )

class StockResource (Resource):
    def get (self, stock_id):
        stock = Stock.query.get_or_404 (stock_id)
        app.logger.info (stock)
        return stockschema.dump([stock])
        # return jsonify(stockschema.dump(stock)) 

    def patch(self, stock_id):
        stock = Stock.query.get_or_404(stock_id)
        '''
        if 'title' in request.json:
            post.title = request.json['title']
        if 'content' in request.json:
            post.content = request.json['content']
        '''
        db.session.commit()
        return stockschema.dump(stock)

    def delete(self, stock_id):
        stock = Stock.query.get_or_404(stock_id)
        db.session.delete(stock)
        db.session.commit()
        return '', 204


api.add_resource (StockResource, '/stock/<int:stock_id>' )


# ---------------------------
# Routes  for error handling and index redirect
# ---------------------------
@app.route('/')
def index():
    return 'Hello APIs'


# ---------------------------
# Run app   
# ---------------------------
if __name__ == '__main__':
    app.run(debug=True, port=8081)
