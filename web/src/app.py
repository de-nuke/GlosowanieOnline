# app.py


from flask import Flask
from flask import request, render_template, redirect

from flask.ext.sqlalchemy import SQLAlchemy
from config import BaseConfig


app = Flask(__name__)
app.config.from_object(BaseConfig)
db = SQLAlchemy(app)

from models import *


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        machine = Machine(name)
        db.session.add(machine)
        db.session.commit()
    machines = Machine.query.order_by(Machine.last_checked.desc()).all()
    for machine in machines:
        machine_update(machine)
    db.session.commit()
    return render_template('index.html', machines=machines)

def machine_update(machine):
    import subprocess
    import datetime
    p = subprocess.Popen(['ping', machine.name, '-c', '1', '-W', '2'])
    p.wait()
    machine.last_status = p.poll() == 1
    machine.last_checked = datetime.datetime.now() 
        
if __name__ == '__main__':
    app.run(host='127.0.0.1',port=8877)
