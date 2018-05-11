import sys
sys.path.append("../..")
import mysql.connector as sql
import datetime
from Configuration.model.product import Product

db = sql.connect(host="localhost", user="root", passwd="jlsjamtf", db="config")
cursor = db.cursor()

def add_product(user_email, product):
    cursor.execute("""INSERT INTO product
                    (user_email, name, introduction, is_release, deadline, root_component_id)
                    VALUES
                    (%s, %s, %s, %s, %s, %s)""",
                    (user_email, product.name, product.introduction, product.is_release, product.deadline, product.root_component_id))
    db.commit()
    cursor.execute("SELECT LAST_INSERT_ID()")
    row = cursor.fetchone()
    return row[0]

def delete_product(id):
    cursor.execute("""DELETE FROM product WHERE id = %s""",
                    (id, ))
    db.commit()

def update_product(id, name, introducton):
    cursor.execute("""UPDATE product
                    SET name = %s, introduction = %s
                    WHERE id = %s """,
                    (name, introducton, id))
    db.commit()

def update_is_realease(id):
    cursor.execute("""UPDATE product
                    SET is_release = 1 
                    WHERE id = %s """,
                    (id, ))
    db.commit()

def updete_deadline(id, deadline):
    cursor.execute("""UPDATE product
                    SET deadline = %s 
                    WHERE id = %s """,
                    (deadline, id))
    db.commit()

def find_all_products(user_email):
    pros = []
    cursor.execute("""SELECT * FROM product
                    WHERE user_email = %s AND is_release = 1""",
                    (user_email, ))
    for row in cursor.fetchall():
        pro = Product(row[0], row[2], row[3], row[4], row[5], row[6])
        pros.append(pro)
    return pros

def find_all_models(user_email):
    mods = []
    cursor.execute("""SELECT * FROM product
                    WHERE user_email = %s AND is_release = 0""",
                    (user_email, ))
    for row in cursor.fetchall():
        mod = Product(row[0], row[2], row[3], row[4], row[5], row[6])
        mods.append(mod)
    return mods

user_email = 'chenjn_amtf@qq.com'

# product = Product('jlsj', 'This is the best world.', 0, datetime.datetime.now(), 666)
# id = add_product(user_email, product)
# print(id)

# delete_product(1)

# update_product(2,'极乐世界', '这是十方世界中最殊胜的世界。')

# update_is_realease(2)
# update_is_realease(3)

# updete_deadline(2, datetime.datetime.now())

pros = find_all_products(user_email)
for pro in pros:
    pro.prn_obj()