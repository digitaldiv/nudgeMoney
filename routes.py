from resources import FinanceDataListResource, StockListResource, StockResource, PortfolioListResource, PortfolioResource, UserResource, LoginResource

def create_routes(api):
    api.add_resource (LoginResource, '/login' )
    api.add_resource (UserResource, '/user' )
    api.add_resource (PortfolioListResource, '/portfolios' )
    api.add_resource (PortfolioResource, '/portfolio/<int:portfolio_id>' )
    api.add_resource (StockListResource, '/stocks' )
    api.add_resource (StockResource, '/stock/<int:stock_id>' )
    api.add_resource(FinanceDataListResource, '/snpstockslist')