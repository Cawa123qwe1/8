from peewee import *
import argparse

db_connection = SqliteDatabase('products.db')


class ProductModel(Model):
    id = IntegerField(primary_key=True)
    name = CharField()
    price = IntegerField()

    class Meta:
        database = db_connection
        db_table = 'product'

    def __str__(self):
        return f"ProductModel(id={self.id}, name={self.name}, price={self.price})"

    def to_dict(self):
        return {"id": self.id, "name": self.name, "price": self.price}


class ProductOperations:
    @staticmethod
    def create_product(name, price):
        return ProductModel.create(name=name, price=price)

    @staticmethod
    def get_product_by_id(product_id):
        try:
            return ProductModel.get(ProductModel.id == product_id)
        except DoesNotExist:
            return None

    @staticmethod
    def update_product(product_id, name=None, price=None):
        product = ProductOperations.get_product_by_id(product_id)
        if product:
            if name:
                product.name = name
            if price:
                product.price = price
            product.save()
            return product
        else:
            return None

    @staticmethod
    def delete_product(product_id):
        product = ProductOperations.get_product_by_id(product_id)
        if product:
            product.delete_instance()
            return True
        else:
            return False


def add_default_products():
    products_data = [
        {"name": "Sugar", "price": 32},
        {"name": "Sult", "price": 19},
        {"name": "Bread", "price": 20},
        {"name": "Butter", "price": 62},
        {"name": "Milk", "price": 32},
    ]
    for data in products_data:
        ProductOperations.create_product(name=data["name"], price=data["price"])


def print_all_products():
    for product in ProductModel.select():
        print(product)


def manage_product_database(delete_all_data=False, add_default_data=False):
    db_connection.connect()
    db_connection.create_tables([ProductModel])

    if delete_all_data:
        ProductModel.delete().execute()
    if add_default_data:
        add_default_products()

    db_connection.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--delete_all_data', help='deletes all data', action='store_true')
    parser.add_argument('-a', '--add_default_data', help='add default data', action='store_true')
    parser.add_argument('-p', '--print_all_data', help='print all rows', action='store_true')
    args = parser.parse_args()

    manage_product_database(delete_all_data=args.delete_all_data, add_default_data=args.add_default_data)

    if args.print_all_data:
        print_all_products()
