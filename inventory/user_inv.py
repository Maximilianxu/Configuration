import sys
sys.path.append("../..")
import datetime
from Configuration.inventory import db
from Configuration.model.user import User

cursor = db.cursor()

def insert_user(user):
    cursor.execute("""INSERT INTO c_user
                    (email, name, password, role, company, profession) 
                    VALUES 
                    (%s, %s, %s, %s, %s, %s)""",
                    (user.email, user.name, user.password, user.role, user.company, user.profession))
    db.commit()

def find_user_by_email(email):
    cursor.execute("SELECT * FROM c_user WHERE email=%s", (email, ))
    row = cursor.fetchone()
    if row is not None:
        return User(row[0], row[1], row[2], row[3], row[4], row[5])
    else:
        return User("","","","","","")

# user = User('895255299@qq.com', 'chen', 'jlsjamtf',1 , 'jlu', 'student')
# insert_user(user)

# user = find_user_by_email('chenjn_amtf@qq.com')
# print(user.name)