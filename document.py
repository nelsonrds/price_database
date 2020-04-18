from datetime import datetime
from mongoengine.fields import *
from mongoengine.document import *
import json


class ProductPrices(DynamicDocument):
    price = StringField()
    price_was = StringField()
    price_number = DecimalField(precision=2)
    price_number_was = DecimalField(precision=2)
    date_created = DateTimeField(default=datetime.utcnow)

    def get_json(self):
        prd_prices = {
            "price": self.price,
            "price_was": self.price_was,
            "price_number": self.price_number,
            "price_number_was": self.price_number_was,
            "date_inserted": self.date_created,
        }
        return json.dumps(prd_prices)

    meta = {
        "indexes": ['date_inserted', 'price'],
        "ordering": ['-date_inserted']
    }


class Product(DynamicDocument):
    name = StringField()
    sub_title = StringField()
    sub_sub_title = StringField()
    url_img = StringField()
    url_product = StringField()
    color = StringField()
    company = StringField()
    prices = ListField(ReferenceField(ProductPrices))
    category_list = ListField(StringField())
    date_created = DateTimeField(default=datetime.utcnow)
    is_deleted = BooleanField(default=False)

    def get_json(self):
        prd = {
            "name": self.name,
            "sub_title": self.sub_title,
            "sub_sub_title": self.sub_sub_title,
            "url_img": self.url_img,
            "url_product": self.url_product
        }
        return json.dumps(prd)

    meta = {
        "indexes": ['username', 'email'],
        "ordering": ['-date_created']
    }


class User(DynamicDocument):
    username = StringField(required=True)
    first_name = StringField()
    last_name = StringField()
    password = StringField(required=True)
    email = EmailField(required=True)
    date_created = DateTimeField(default=datetime.utcnow)
    image = ImageField(size=(60, 60, True))
    admin = BooleanField()
    product = ListField(ReferenceField(Product))

    def get_json(self):
        prd = {
            "username": self.username,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email
        }
        return json.dumps(prd)

    def test_name(self, name):
        self.save()

    meta = {
        "indexes": ['username', 'email'],
        "ordering": ['-date_created']
    }
