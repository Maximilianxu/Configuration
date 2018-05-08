import sys
sys.path.append("../")
import MySQLdb as sql
import datetime
from Configuration.model.user import User

db = sql.connect(host="localhost", user="root", passwd="xu71849236", db="config")
cursor = db.cursor()

def insert_user(user):
    cursor.execute("""INSERT INTO c_user (email, name, password) 
    VALUES (%s, %s, %s)""", (user.email, user.name, user.password))
    db.commit()

def find_user_by_email(email):
    cursor.execute("SELECT * FROM c_user WHERE email=%s", (email, ))
    row = cursor.fetchone()
    return User(row[0], row[1], row[2])

# user = User('15754310533', 'Max', '123456')
# insert_user(user)

# user = find_user_by_phone_number('15754310533')
# print(user.name)