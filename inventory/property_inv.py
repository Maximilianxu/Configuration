import sys
sys.path.append("../..")
import mysql.connector as sql
from Configuration.model.domain import Domain
from Configuration.model.variable import Variable
from Configuration.model.property import Property

db = sql.connect(host="localhost", user="root", passwd="xu71849236", db="config")
cursor = db.cursor()

def add_property(component_id, name, introduction, datatype, dataunit, domin, domin_display):
    # vals_str_list = [str(i) for i in property.dom.vals_list]
    # domin = ','.join(vals_str_list)
    # domin_display = ','.join(property.domin_display)
    cursor.execute("""INSERT INTO property
                    (component_id, name, introduction, datatype, dataunit, domin, domin_display)
                    VALUES
                    (%s, %s, %s, %s, %s, %s, %s)""",
                    (component_id, name, introduction, datatype, dataunit, domin, domin_display))
    db.commit()
    cursor.execute("SELECT LAST_INSERT_ID()")
    row = cursor.fetchone()
    return row[0]

def delete_property(id):
    cursor.execute("""DELETE FROM property WHERE id = %s""",
                    (id, ))
    db.commit()

def delete_all_propertys(component_id):
    cursor.execute("""DELETE FROM property WHERE component_id = %s""",
                    (component_id, ))
    db.commit()

def update_property(property_id, name, introduction, datatype, dataunit, domin, domin_display):
    # vals_str_list = [str(i) for i in property.dom.vals_list]
    # domin = ','.join(vals_str_list)
    cursor.execute("""UPDATE property
                    SET name = %s, introduction = %s, datatype = %s, dataunit = %s, domin = %s, domin_display = %s
                    WHERE id = %s """,
                    (name, introduction, datatype, dataunit, domin, domin_display, property_id))
    db.commit()

def find_properties_id_name(component_id):
    properties = []
    cursor.execute("""SELECT id, name FROM property
                    WHERE component_id = %s""",
                    (component_id, ))
    for row in cursor.fetchall():
        property = {'id': row[0], 'name': row[1]}
        properties.append(property)
    return properties

def find_a_property(id):
    cursor.execute("""SELECT name, introduction, datatype, dataunit, domin_display FROM property
                    WHERE id = %s""",
                    (id, ))
    row = cursor.fetchone()
    pro = {'name': row[0], 'introduction': row[1], 'datatype': row[2], 'dataunit': row[3], 'domin_display': row[4]}
    return pro

# dom = Domain([10, 50, 100])
# domin_display = [str(i) for i in dom.vals_list]
# pro = Property(dom.vals_list[0], dom, 2, '面积', '莲花因为念佛人的愿力大小、精进程度等而有不同的面积。', '整型', '由旬', domin_display)
# pro.id = add_property(6,pro)
# pro.prn_obj()


# delete_property(1)

# update_property(pro)

# props = find_all_propertys(6)
# for prop in props:
#     prop.prn_obj()
