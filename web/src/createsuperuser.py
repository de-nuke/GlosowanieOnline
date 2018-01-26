from app import db
from admin_login import Admin
import getpass
from werkzeug.security import generate_password_hash
import html
import random
import string

username = input('Username: ')
password = getpass.getpass('Password: ')
token = input('Token: ')

login = html.escape(username)

salt = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(30))

hashed_password = generate_password_hash(password.encode() + salt.encode())
hashed_token = generate_password_hash(token.encode() + salt.encode())

# hashed_password = generate_password_hash(hashed_password)
# hashed_token = generate_password_hash(hashed_token)

db.session.add(Admin(
    login=login,
    password=hashed_password,
    token=hashed_token,
    salt=salt
))
print('User {} created!'.format(login))
db.session.commit()
