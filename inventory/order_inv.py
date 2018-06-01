import sys
sys.path.append("../")
import datetime
from Configuration.inventory import db
from Configuration.model.order import Order

<<<<<<< HEAD
db = sql.connect(host="localhost", user="root", passwd="xu71849236", db="config")
=======
>>>>>>> df4cef6cec979710aee074118eeb67ff3ab11140
cursor = db.cursor()

def insert_order(order):
    cursor.execute("""INSERT INTO c_order (user_email, product_id, assignments, order_date, price, order_state) 
    VALUES (%s, %s, %s, %s, %s, %s)""", (order.user_email, order.product_id,\
    order.assignments, order.order_date, order.price, order.order_state))
    db.commit()

def find_all_orders_by_email(email):
    ords = []
    cursor.execute("SELECT * FROM c_order WHERE user_email=%s", (email, ))
    for row in cursor.fetchall():
        ord = Order(row[1], row[2], row[3], row[4], row[5], row[6])
        ords.append(ord)
    return ords

# ord = Order('maximilian.xu.2015@gmail.com', 1, 'a = 1, b = 2, c = 3', datetime.date.today(), \
#     30, 'up')

# insert_order(ord)
# ords = find_all_orders()
# for ord in ords:
#     print(ord.user_email)
