#!/usr/bin/env python3
from models import db, Restaurant, RestaurantPizza, Pizza
from flask_migrate import Migrate
from flask import Flask, request, make_response
from flask_restful import Api, Resource
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)


@app.route("/")
def index():
    return "<h1>Code challenge</h1>"

@app.get('/restaurants')
def all_restaurants():
    return [r.to_dict() for r in Restaurant.query.all() ], 200

@app.get('/restaurants/<int:id>')
def restaurants_by_id(id):
    restaurant = db.session.get(Restaurant, id)
    if restaurant:
        restaurant_dict = restaurant.to_dict()
        restaurant_dict["restaurant_pizzas"] = [rp.to_dict() for rp in restaurant.restaurantpizza]
        return restaurant_dict, 200
    else:
        return {"error": "Restaurant not found"}, 404

@app.delete('/restaurants/<int:id>')
def delete_restaurant_by_id(id):
    restaurant = Restaurant.query.where(Restaurant.id == id).first()
    
    if restaurant:
        db.session.delete(restaurant)
        db.session.commit()
        return {}, 204
    else:
        return {"error": "Restaurant not found"}, 404
    
@app.get('/pizzas')
def all_pizzas():
    return [ p.to_dict() for p in Pizza.query.all() ], 200

@app.post('/restaurant_pizzas')
def post_rp():
    try:
        
        new_rp = RestaurantPizza(
        price = request.json.get('price'),
        pizza_id = request.json.get('pizza_id'),
        restaurant_id=request.json.get('restaurant_id')
            )
        db.session.add(new_rp)
        db.session.commit()

        return new_rp.to_dict(), 201
    
    except ValueError as error:
        return { "errors": ["validation errors"] }, 400


if __name__ == "__main__":
    app.run(port=5555, debug=True)
