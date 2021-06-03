from flask import jsonify, request
from flask_restful import Resource
from models import db, FinanceData, Stock, User, Portfolio
from schemas import ma, financeDataSchema, stockschema, userschema, portfolioschema
import logging
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import datetime


# ---------------------------
#  Define API Resources  
# ---------------------------

class FinanceDataListResource(Resource):
    # Make sure the user is authenticated
    @jwt_required()
    def get(self):
        #stocks = db.session.query(FinanceData).all()
        snpList = FinanceData.query.all()

        return financeDataSchema.dump(snpList)




class PortfolioListResource (Resource):
    def get (self):
        portfoliolist = Portfolio.query.all ()
        return jsonify(portfolioschema.dump(portfoliolist)) 

    # Make sure the user is authenticated
    @jwt_required()
    # Create new portfolio
    def post(self):
        print('Adding new Portfolio')
        #app.logger.info(f'Received : {request.json}')
        #app.logger.info(f'Received : {request.get_json()}')

        # find the user id from JWT token
        logged_user_id = get_jwt_identity()
        new_portfolio = Portfolio ( id=request.json["id"],
                    portfolio_title = request.json["portfolio_title"],
                    portfolio_desc  = request.json["portfolio_desc"],
                    date_created = request.json["date_created"],
                    date_updated = request.json["date_updated"],
                    user_id = logged_user_id #request.json["user_id"]
                )
        
        db.session.add(new_portfolio)
        db.session.commit()
        
        return stockschema.dump([new_portfolio])



class PortfolioResource (Resource):
    def get (self, portfolio_id):
        portfolio = Portfolio.query.get_or_404 (portfolio_id)
        #app.logger.info (portfolio)
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




class StockListResource (Resource):
    def get (self):
        stockslist = Stock.query.all ()
        return jsonify(stockschema.dump(stockslist)) 

    # Create new stock
    def post(self):
        print('Adding new Stock')
        #app.logger.info(f'Received : {request.json}')
        #app.logger.info(f'Received : {request.get_json()}')

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




class StockResource (Resource):
    def get (self, stock_id):
        stock = Stock.query.get_or_404 (stock_id)
        #app.logger.info (stock)
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


class UserResource (Resource):
    def post(self):
        print('Adding new User')
        #app.logger.info(f'New User Add : Received : {request.json}')
        #app.logger.info(f'Received JSON: {body}')
        #new_user = User (**body)

        new_user = User(#id= request.json["id"],
                        user_name= request.json["user_name"],
                        user_pwd = request.json["user_pwd "],
                        date_signed= request.json["date_signed"],
                        status= request.json["status"],
                        user_email= request.json["user_email"],
                        user_phone= request.json["user_phone"]
                    )
        #portfolios= request.json["portfolios"]
        
        db.session.add(new_user)
        db.session.commit()
        
        return userschema.dump([new_user])

class LoginResource(Resource):
    def post(self):

        user = User.query.filter_by(user_name=request.json["user_name"]).first()

        authorized = user.check_password(request.json["user_pwd"])

        if not authorized:
            return {'error': 'User name or password invalid'}, 401
 
        expires = datetime.timedelta(days=7)
        access_token = create_access_token(identity=str(user.id), expires_delta=expires)
        return {'token': access_token}, 200

