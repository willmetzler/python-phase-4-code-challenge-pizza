from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(
    naming_convention={
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    }
)

db = SQLAlchemy(metadata=metadata)


class Restaurant(db.Model, SerializerMixin):
    __tablename__ = "restaurants"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    address = db.Column(db.String)

    # add relationship
    restaurantpizza = db.relationship("RestaurantPizza", back_populates="restaurant")

    # add serialization rules
    serialize_rules = ['-restaurantpizza.restaurant', '-pizzas.restaurantpizza']

    def __repr__(self):
        return f"<Restaurant {self.name}>"


class Pizza(db.Model, SerializerMixin):
    __tablename__ = "pizzas"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    ingredients = db.Column(db.String)

    # add relationship
    restaurantpizza = db.relationship("RestaurantPizza", back_populates="pizza" )
    restaurants = association_proxy("restaurantpizza", "restaurant")

    # add serialization rules
    serialize_rules = ['-restaurantpizza.pizza', '-restaurants.restaurantpizza']

    def __repr__(self):
        return f"<Pizza {self.name}, {self.ingredients}>"


class RestaurantPizza(db.Model, SerializerMixin):
    __tablename__ = "restaurant_pizzas"

    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Integer, nullable=False)

    # add relationships
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'))
    pizza_id = db.Column(db.Integer, db.ForeignKey('pizzas.id'))

    restaurant = db.relationship("Restaurant", back_populates='restaurantpizza')
    pizza = db.relationship("Pizza", back_populates='restaurantpizza')

    # add serialization rules
    serialize_rules = ['-restaurant.restaurantpizza', '-pizza.restaurantpizza']

    # add validation
    @validates('price')
    def validate_price(self, key, price):
        if price  < 1 or price   > 30:
            raise ValueError('Price must be between 1 and 30')
        return price   
    
    def __repr__(self):
        return f"<RestaurantPizza ${self.price}>"
