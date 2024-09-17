import sqlite3


class ProductDatabase:
    def __init__(self) -> None:
        self.conn = sqlite3.connect('product')
        self.cursor = self.conn.cursor()

    def create_table(self):
        self.cursor.execute(
            """
          CREATE TABLE IF NOT EXISTS products(
              id INTEGER PRIMARY KEY AUTOINCREMENT
              
            
          )                                 """
        )
        self.conn.commit()
        print('table created successfully')

    def add_product(self, product):
        self.cursor.execute(
            """
            INSERT INTO products (name)
            VALUES (?)
            """,
            (product.name),
        )
        
    def execute_custom_query(self, query, params=()):
        self.cursor.execute(query,params)
        self.conn.commit()
        return self.cursor.fetchall()
    


class Product:
    def __init__(self, name):
        self.name = name



if __name__ == "__main__":
    db =ProductDatabase()
    db.create_table()
