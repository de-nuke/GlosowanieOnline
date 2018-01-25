from app import db
from admin_login import Admin
import getpass
from werkzeug.security import generate_password_hash
import html

username = input('Username: ')
password = getpass.getpass('Password: ')

login = html.escape(username)

hashed_password = generate_password_hash(password.encode())

db.session.add(Admin(
    login=login,
    password=hashed_password
))
print('User {} created!'.format(login))
db.session.commit()
