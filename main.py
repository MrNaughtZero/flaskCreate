import os

## Create new directory
os.mkdir('app')

## Create new run.py file
r = open('run.py', 'x')
r.write('from app import app \n \nif __name__ == "__main__:"\n   app.run()')

## Create Routes, Static, Templates folder
os.mkdir('app/routes')
os.mkdir('app/static')
os.mkdir('app/static/images')
os.mkdir('app/static/styles')
os.mkdir('app/static/scripts')
os.mkdir('app/templates')
os.mkdir('app/templates/main')

## Create default main.css && main.js

c = open('app/static/styles/main.css', 'x')
j = open('app/static/scripts/main.js', 'x')

## Create Main template folder && index.html

m = open('app/templates/main/index.html', 'x')


print('Y or N \n')

## Check for blueprints & setup

setup_bp = input('Setup Blueprints: ')
if setup_bp == 'Y':
    ## add bp to init
    init_create =  open('app/__init__.py', 'x')
    init_create.write('''from flask import Flask, Blueprint\n\napp = Flask(__name__)\napp.debug = True\napp.secret_key ='knakjds03928knds'\n''')

    blueprint_amount = int(input('How many blueprints: '))
    blueprint_list = []
    blueprint = {}
    
    for i in range(blueprint_amount):
        blueprint[i] = input(f'Blueprint {i+1} name: ')
        blueprint_create = open(f'app/routes/{blueprint[i]}.py', 'x')
        blueprint_create.write('from flask import Flask, Blueprint\n\n' +f'{blueprint[i]}' + f'_bp = Blueprint("blueprint_{blueprint[i]}", __name__)')

        blueprint_list.append(blueprint[i])

    routes_str = '\nfrom .routes import '
    
    for item in blueprint_list:
        routes_str = routes_str + str(item) + ','
    init_create.write(routes_str[:-1] + '\n \n')

    for item in blueprint_list:
        init_create.write(f'app.register_blueprint({item}.{item}_bp) \n')

else:
    ## Create __init__

    init_create = open('app/__init__.py', 'x')
    init_create.write('''from flask import Flask\n\napp = Flask(__name__)\napp.debug = True\napp.secret_key ='knakjds03928knds'\n''')

setup_connection = input('\nSetup Database: ')
if setup_connection == 'Y':
    db_name = input('Database name: ')
    db_user = input('Database username: ')
    db_pass = input('Database Password: ')
    create_db = open('app/database.py', 'x')
    create_db.write(f'''from flask_mysqldb import MySQL\nfrom flask_sqlalchemy import SQLAlchemy\nfrom flask_login import UserMixin\n\n\ndatabase_name = '{db_name}'\ndatabase_path = 'mysql://{db_user}:{db_pass}@localhost/{db_name}'\n\ndb = SQLAlchemy()\n\ndef setup_db(app, database_path=database_path):\n    app.config["SQLALCHEMY_DATABASE_URI"] = database_path\n    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False\n    db.app = app\n    db.init_app(app)\n    db.create_all()''')

    init_create.write('\nfrom app.database import setup_db\n\nsetup_db(app)\n')

setup_login = input('Setup Flask Login: ')
if setup_login == 'Y':
    init_create.write('\nfrom flask_login import LoginManager\n\nlogin_manager = LoginManager()\nlogin_manager.init_app(app)\n\nfrom app.models import User\n\n@login_manager.user_loader\ndef load_user(id):\n    return User.query.get(id)')

    create_models = open('app/models.py', 'x')
    create_models.write('''from app.database import db\nimport hashlib\nfrom hashlib import sha256\n\nclass User(db.Model):\n    __tablename__ = 'users'\n    id = db.Column(db.Integer, primary_key=True)\n    username = db.Column(db.String(255), nullable=False)\n    email = db.Column(db.String(255), nullable=False)\n    password = db.Column(db.String(255), nullable=False)\n    \n    def get_id(self):\n        return self.id\n    \n    def is_authenticated(self):\n        return True\n\n    def get_username(self):\n        return self.username\n\n    def is_active(self):\n        return True\n\n    def is_anonymous(self):\n        return False\n\n    def create_user(self):\n        db.session.add(self)\n        db.session.commit()\n\n    def update(self):\n        db.session.commit()\n\n    @staticmethod\n    def hash_password(password):\n        return sha256(password.encode('utf-8')).hexdigest()''')

setup_venv = input('Setup virtual environment: ')
if setup_venv == 'Y':
    os.system('python3 -m venv venv')
    
create_classes = open('app/classes.py', 'x')

setup_forms = input('Create forms: ')
if setup_forms == 'Y':
    create_forms = open('app/forms.py', 'x')
    create_forms.write('''from flask_wtf import FlaskForm\nfrom wtforms import StringField, PasswordField, SubmitField, RadioField, validators, FileField, TextAreaField, HiddenField, MultipleFileField, SelectField, BooleanField, IntegerField\nfrom wtforms.validators import InputRequired, Email, Length, NumberRange, EqualTo\n\nclass UserRegister(FlaskForm):\n    profile_img = FileField(validators=[InputRequired()])\n    email = StringField(validators=[InputRequired(), Email('Invalid Email'), Length(max=300)])\n    username = StringField(validators=[InputRequired(), Length(max=300)])\n    password = PasswordField(validators=[InputRequired(), EqualTo('confirm_password')])\n    confirm_password = PasswordField(validators=[InputRequired(), EqualTo('password')])\n    submit = SubmitField('Register')\n\nclass UserLogin(FlaskForm):\n    username = StringField(validators=[InputRequired(), Length(max=300)])\n    password = PasswordField(validators=[InputRequired()])\n    submit = SubmitField('Login')\n''')
