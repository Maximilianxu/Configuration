import sys
sys.path.append("../..")
<<<<<<< HEAD
import MySQLdb as sql
=======
from Configuration.inventory import db
>>>>>>> df4cef6cec979710aee074118eeb67ff3ab11140
from Configuration.model.domain import Domain
from Configuration.model.variable import Variable
from Configuration.model.constraint import Constraint

<<<<<<< HEAD
db = sql.connect(host="localhost", user="root", passwd="xu71849236", db="config")
=======
>>>>>>> df4cef6cec979710aee074118eeb67ff3ab11140
cursor = db.cursor()

def add_constraint(product_id, expression, expression_display):
    cursor.execute("""INSERT INTO c_constraint
                    (product_id, expression, expression_display)
                    VALUES
                    (%s, %s, %s)""",
                    (product_id, expression, expression_display))
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

def find_a_constraint(constraint_id):
    cursor.execute("""SELECT id, expression_display FROM c_constraint
                    WHERE id = %s""",
                    (constraint_id, ))
    row = cursor.fetchone()
    constraint = {'id': row[0], 'expression_display': row[1]}
    return constraint

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