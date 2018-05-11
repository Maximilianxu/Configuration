import sys
sys.path.append("../..")
import mysql.connector as sql
from Configuration.model.component import Component

db = sql.connect(host="localhost", user="root", passwd="jlsjamtf", db="config")
cursor = db.cursor()

def add_component(product_id, component):
    cursor.execute("""INSERT INTO component
                    (product_id, father_component_id, name, introduction)
                    VALUES
                    (%s, %s, %s, %s)""",
                    (product_id, component.father_component_id, component.name, component.introduction))
    db.commit()
    cursor.execute("SELECT LAST_INSERT_ID()")
    row = cursor.fetchone()
    return row[0]

def delete_component(id):
    cursor.execute("""DELETE FROM component WHERE id = %s""",
                    (id, ))
    db.commit()

def update_component(id, name, introducton):
    cursor.execute("""UPDATE component
                    SET name = %s, introduction = %s
                    WHERE id = %s """,
                    (name, introducton, id))
    db.commit()

def updata_father_id(id, father_component_id):
    cursor.execute("""UPDATE component
                    SET father_component_id = %s 
                    WHERE id = %s """,
                    (father_component_id, id))
    db.commit()

def find_all_components(product_id):
    coms = []
    cursor.execute("""SELECT * FROM component
                    WHERE product_id = %s""",
                    (product_id, ))
    for row in cursor.fetchall():
        com = Component(row[0], row[2], row[3], row[4])
        coms.append(com)
    return coms

# def find_all_models(user_email):
#     mods = []
#     cursor.execute("""SELECT * FROM component
#                     WHERE user_email = %s AND is_release = 0""",
#                     (user_email, ))
#     for row in cursor.fetchall():
#         mod = component(row[0], row[2], row[3], row[4], row[5], row[6])
#         mods.append(mod)
#     return mods

# com = Component(0, 3,'莲花', '往生极乐世界的众生均从莲花中化生。')
# com.id = add_component(2, com)
# com.prn_obj()

# delete_component(2)

# update_component(5,'八功德水', '具足澄净、清冷、甘美、轻软、润泽、安和、除饥渴和长养诸根这八种功德的水。')

# updata_father_id(5, 4)

# coms = find_all_components(2)
# for com in coms:
#     com.prn_obj()
