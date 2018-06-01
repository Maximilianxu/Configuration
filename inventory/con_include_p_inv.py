import sys
sys.path.append("../..")
import MySQLdb as sql

db = sql.connect(host="localhost", user="root", passwd="xu71849236", db="config")
cursor = db.cursor()

def add_relation(constraint_id, property_ids):
    for property_id in property_ids:
        cursor.execute("""INSERT INTO con_include_p
                        (constraint_id, property_id)
                        VALUES
                        (%s, %s)""",
                        (constraint_id, property_id))
    db.commit()

def delete_relation_by_property(property_id):
    cursor.execute("""DELETE FROM con_include_p WHERE property_id = %s""",
                    (property_id, ))
    db.commit()

def delete_relation_by_constraint(constraint_id):
    cursor.execute("""DELETE FROM con_include_p WHERE constraint_id = %s""",
                    (constraint_id, ))
    db.commit()

def find_properties_id_by_constraint(constraint_id):
    prop_ids = []
    cursor.execute("""SELECT property_id FROM con_include_p
                    WHERE constraint_id = %s""",
                    (constraint_id, ))
    for row in cursor.fetchall():
        prop_ids.append(row[0])
    return prop_ids

def find_constraints_id_by_property(property_id):
    cons_ids = []
    cursor.execute("""SELECT constraint_id FROM con_include_p
                    WHERE property_id = %s""",
                    (property_id, ))
    for row in cursor.fetchall():
        cons_ids.append(row[0])
    return cons_ids

# constraint_id = 4
# property_id = 3
# property_ids = [5]

# add_relation(constraint_id, property_ids)

# delete_property(property_id)

# delete_constraint(constraint_id)

# prop_ids = find_all_property_id(constraint_id)
# print(prop_ids)

# cons_ids = find_all_constraint_id(property_id)
# print(cons_ids)