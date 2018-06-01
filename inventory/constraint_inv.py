import sys
sys.path.append("../..")
import MySQLdb as sql
from Configuration.model.domain import Domain
from Configuration.model.variable import Variable
from Configuration.model.constraint import Constraint

db = sql.connect(host="localhost", user="root", passwd="xu71849236", db="config")
cursor = db.cursor()

def add_constraint(product_id, expression):
    cursor.execute("""INSERT INTO c_constraint
                    (product_id, expression)
                    VALUES
                    (%s, %s)""",
                    (product_id, expression))
    db.commit()
    cursor.execute("SELECT LAST_INSERT_ID()")
    row = cursor.fetchone()
    return row[0]

def delete_constraint(id):
    cursor.execute("""DELETE FROM c_constraint WHERE id = %s""",
                    (id, ))
    db.commit()

def delete_all_constraints(product_id):
    cursor.execute("""DELETE FROM c_constraint WHERE product_id = %s""",
                    (product_id, ))
    db.commit()

def update_constraint(constraint_id, expression):
    cursor.execute("""UPDATE c_constraint
                    SET expression = %s
                    WHERE id = %s """,
                    (expression, constraint_id))
    db.commit()

def find_constraints_id(product_id):
    con_ids = []
    cursor.execute("""SELECT id FROM c_constraint
                    WHERE product_id = %s""",
                    (product_id, ))
    for row in cursor.fetchall():
        con_ids.append(row[0])
    return con_ids

# dom = Domain([10, 50, 100])
# var = Variable(dom.vals_list[0], dom)
# vars = [var]
# con = Constraint(0, '? == 100', vars)
# con.id = add_constraint(2, con)
# print(con)

# delete_constraint(2)

# update_constraint(3,'? >= 20')

# cons = find_all_constraints(2)
# for con in cons:
#     print(con)