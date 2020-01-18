from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from db import db
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList

from datetime import datetime, timedelta

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True      #
app.secret_key = 'ehab'
api = Api(app)
db.init_app(app)


@app.before_first_request
def create_tables():
    db.create_all()


# optional ... if removed, URL will be /auth
app.config['JWT_AUTH_URL_RULE'] = '/login'

# config JWT to expire within 15 min
app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=900)

jwt = JWT(app, authenticate, identity)  # /auth ... end point created for us

api.add_resource(Item, '/item/<string:name>')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(StoreList, '/stores')
api.add_resource(UserRegister, '/register')

# api.add_resource(UserRegister, '/getuser/<int:id>')

if __name__ == '__main__':
    app.run(port=5000, host='0.0.0.0', debug=True)
