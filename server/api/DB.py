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


    def add_product(self, img_src: str, price: int, weight: int, name: str):
        try:
            print(img_src, price, weight, name)
            sql = "INSERT INTO foodCard (img_src, price, weight, name) VALUES (%s, %s, %s, %s)"
            values = (img_src, price, weight, name)
            self.cur.execute(sql, values)
            self.conn.commit()
            return {"status": "ok"}
        except Exception as e:
            print(f"Error: {e}")
            return {"status": "error 500", "message": str(e)}


    def get_products(self):
        Product = namedtuple('Product', ['id', 'img_src', 'price', 'weight', 'name'])
        self.cur.execute("SELECT * FROM foodCard")
        response = self.cur.fetchall()
        products = [Product(*item)._asdict() for item in response]
        return products
    
    def get_product_by_id(self, id):
        Product = namedtuple('Product', ['id', 'img_src', 'price', 'weight', 'name'])
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
    
    
        