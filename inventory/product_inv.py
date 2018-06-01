import sys
sys.path.append("../..")
import datetime
from Configuration.inventory import db
from Configuration.model.product import Product
from Configuration.model.variable import Variable
from Configuration.model.property import Property
from Configuration.model.constraint import Constraint
from Configuration.model.domain import Domain

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

def update_realease(state, id):
    cursor.execute("""UPDATE product
                    SET is_release = %s 
                    WHERE id = %s """,
                    (state, id))
    db.commit()

def update_deadline(id, deadline):
    cursor.execute("""UPDATE product
                    SET deadline = %s 
                    WHERE id = %s """,
                    (deadline, id))
    db.commit()

def update_root_component_id(id, root_component_id):
    cursor.execute("""UPDATE product
                    SET root_component_id = %s 
                    WHERE id = %s """,
                    (root_component_id, id))
    db.commit()

def find_models_id_name(user_email):
    mods = []
    cursor.execute("""SELECT id, name FROM product
                    WHERE user_email = %s AND is_release = 0""",
                    (user_email, ))
    for row in cursor.fetchall():
        mod = {'id': row[0], 'name': row[1]}
        mods.append(mod)
    return mods

def find_products_id_name_for_expert(user_email):
    products = []
    cursor.execute("""SELECT id, name FROM product
                    WHERE user_email = %s AND is_release = 1""",
                    (user_email, ))
    for row in cursor.fetchall():
        product = {'id': row[0], 'name': row[1]}
        products.append(product)
    return products

def find_products_id_name_for_customer():
    products = []
    cursor.execute("""SELECT id, name FROM product
                    WHERE is_release = 1""")
    for row in cursor.fetchall():
        product = {'id': row[0], 'name': row[1]}
        products.append(product)
    return products

def find_a_model(id):
    cursor.execute("""SELECT name, introduction, root_component_id FROM product
                    WHERE id = %s""",
                    (id, ))
    row = cursor.fetchone()
    mod = {'name': row[0], 'introduction': row[1], 'root_component_id': row[2]}
    return mod

def find_all_properties_by_product_id(product_id):
    properties = []
    cursor.execute("""SELECT id FROM component
                    WHERE product_id = %s""",
                    (product_id, ))
    components_id = []
    for row in cursor.fetchall():
        components_id.append(row[0])
    for component_id in components_id:        
        cursor.execute("""SELECT * FROM property
                    WHERE component_id = %s""",
                    (component_id, ))
        for row in cursor.fetchall():
            vals_str_list = row[6].split(',')
            domin = Domain([int(i) for i in vals_str_list])
            domin_display = row[7].split(',')
            property = Property(domin.vals_list[0], domin, row[0], row[2], row[3], row[4], row[5], domin_display)
            properties.append(property)
    return properties

def find_all_constraints_by_product_id(product_id, properties):
    constraints = []
    expressions_display = []
    cursor.execute("""SELECT id, expression, expression_display FROM c_constraint
                    WHERE product_id = %s""",
                    (product_id, ))
    for row in cursor.fetchall():
        constraint = Constraint(row[0], row[1], [])
        constraints.append(constraint)
        expressions_display.append(row[2])
    for constraint in constraints:
        cursor.execute("""SELECT property_id FROM con_include_p
                        WHERE constraint_id = %s""",
                        (constraint.id, ))
        rows = cursor.fetchall()
        variables = []
        for row in rows:
            property_id = row[0]
            for property in properties:
                if property.id == property_id:
                    variables.append(property)
                    break
        constraint.vars = variables
    return (constraints, expressions_display)
        

# user_email = 'chenjn_amtf@qq.com'

# product = Product('jlsj', 'This is the best world.', 0, datetime.datetime.now(), 666)
# id = add_product(user_email, product)
# print(id)

# delete_product(1)

# update_product(2,'极乐世界', '这是十方世界中最殊胜的世界。')

# update_is_realease(2)
# update_is_realease(3)

# updete_deadline(2, datetime.datetime.now())

# constraints = find_all_constraints_by_product_id(2)
# for con in constraints:
#     print(con)