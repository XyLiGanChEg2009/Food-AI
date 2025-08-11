import psycopg2
from collections import namedtuple

class DB():
    def __init__(self):
        self.conn = psycopg2.connect(
        dbname="foodAi",
        user="postgres",
        password="12345678",
        host="localhost",
        port="5432"
        )
        self.cur = self.conn.cursor()

    def add_restaurants(self, name: str):
        try:
            sql = "INSERT INTO restaurants (name) VALUES (%s)"
            self.cur.execute(sql, (name,))
            self.conn.commit()
            return {"status": "ok"}
        except Exception as e:
            print(f"Error: {e}")
            return {"status": "error 500", "message": str(e)}
        
    def get_restaurants(self, id: int = -13):
        print(id)
        if isinstance(id, int) and id >= 0:
            sql = '''SELECT
                r.name AS restaurant_name,
                json_agg(f.*) AS food_items
            FROM
                Restaurants r
            LEFT JOIN
                foodcard f ON r.id = f.restaurant_id
            WHERE r.id = %s
            GROUP BY
                r.name;'''
            self.cur.execute(sql, (id,))
        else:
            sql = """
            SELECT
                r.name AS restaurant_name,
                json_agg(f.*) AS food_items
            FROM
                Restaurants r
            LEFT JOIN
                foodcard f ON r.id = f.restaurant_id
            GROUP BY
                r.name;
        """
            self.cur.execute(sql)
        response = self.cur.fetchall()
        restaurant_food_dict = {}
        for row in response:
            restaurant_name = row[0]
            food_items = row[1] if row[1] else []  # Обрабатываем случай, когда нет блюд

            restaurant_food_dict[restaurant_name] = food_items

        return restaurant_food_dict
        
            

    def add_product(self, img_src: str, price: int, weight: int, name: str, restaurant_id: int, keys: list = []):
        try:
            sql = "INSERT INTO foodCard (img_src, price, weight, name, keys, restaurant_id) VALUES (%s, %s, %s, %s, %s, %s)"
            values = (img_src, price, weight, name, keys, restaurant_id)
            self.cur.execute(sql, values)
            self.conn.commit()
            return {"status": "ok"}
        except Exception as e:
            print(f"Error: {e}")
            return {"status": "error 500", "message": str(e)}


    def get_products(self):
        Product = namedtuple('Product', ['id', 'img_src', 'price', 'weight', 'name', 'keys', 'restaurant_id'])
        self.cur.execute("SELECT * FROM foodCard")
        response = self.cur.fetchall()
        products = [Product(*item)._asdict() for item in response]
        return products
    
    def get_products_by_keys(self, keys: list):
        Product = namedtuple('Product', ['id', 'img_src', 'price', 'weight', 'name', 'keys', 'restaurant_id'])
        self.cur.execute("SELECT * FROM foodCard WHERE keys && %s", (keys,))
        response = self.cur.fetchall()
        products = [Product(*item)._asdict() for item in response]
        return products
    
    def get_product_by_id(self, id):
        Product = namedtuple('Product', ['id', 'img_src', 'price', 'weight', 'name', 'keys', 'restaurant_id'])
        sql = "SELECT * FROM foodCard WHERE id = %s"
        self.cur.execute(sql, id)
        response = self.cur.fetchall()
        products = [Product(*item)._asdict() for item in response]
        return products
    
    # def update_product_by_id(self, id: int, img_src: str, price: int, weight: int):
    #     databaseProduct = self.get_product_by_id(id)
    #     sql = "UPDATE foodCard SET img_src = %s, price = %s, weight = %s WHERE id = %s"
    #     values = (img_src, price, weight, id)
    #     self.cur.execute(sql, values)
    #     self.conn.commit()
    
    
        