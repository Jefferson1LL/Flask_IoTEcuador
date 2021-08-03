from dns import ipv4
from flask import Flask, render_template, request, url_for, redirect, session
from functools import wraps
from bson.objectid import ObjectId
import pymongo
from functools import wraps
from flask_pymongo import PyMongo

app = Flask(__name__)
app.secret_key = b'\xcc^\x91\xea\x17-\xd0W\x03\xa7\xf8J0\xac8\xc5'

# Database
url_client = pymongo.MongoClient("mongodb+srv://jeff:Barcelona1925@cluster0.j8qp4.mongodb.net/mydb?retryWrites=true&w=majority")
db = url_client.mydb

def get_db():
    #Connection MongoDB
    client = 'jeff'
    passdb = 'Barcelona1925'
    dbname = 'mydb'
    app.config['MONGO_URI'] = "mongodb+srv://jeff:Barcelona1925@cluster0.j8qp4.mongodb.net/mydb?retryWrites=true&w=majority"
    mongo = PyMongo(app)

    return mongo

# Decorators
def login_required(f):
  @wraps(f)
  def wrap(*args, **kwargs):
    if 'logged_in' in session:
      return f(*args, **kwargs)
    else:
      return redirect('/')
  
  return wrap

# Routes
from user import routes

#@app.route('/login')
#def login():
  #return render_template('login.html')

@app.route('/registro')
def home():
  return render_template('home.html')



@app.route('/')
def index():
    mydb = get_db()
    saved_todos = mydb.db.todos.find().limit(10)
    cantidad = saved_todos .count()
    return render_template('index.html', filters=saved_todos, cantidades = cantidad)


@app.route('/dashboard/')
@login_required
def dashboard():
  return render_template('dashboard.html')


@app.route('/busqueda/<id>', methods=['GET'])
def get_info(id):
    mydb = get_db()
    todo_item = mydb.db.todos.find({'_id': ObjectId(id)})
    return render_template('busqueda.html', items = todo_item)




@app.route('/', methods=['POST'])
def filter_info():
    filter = request.form.get('filter')
    parameter = request.form.get('parameter')

    if(str(parameter) == "Dirección"):
        mydb = get_db()
        todo_filter = mydb.db.todos.find({'Direccion': filter})
        cantidad = todo_filter.count()
        print("catidad", cantidad)
        return render_template('index.html', filters=todo_filter, cantidades=cantidad)

    if(str(parameter) == "Puerto"):
        mydb = get_db()
        todo_filter = mydb.db.todos.find({'puerto.Puerto': filter})
        cantidad = todo_filter.count()
        print("catidad", cantidad)
        return render_template('index.html', filters=todo_filter, cantidades=cantidad)

    if(str(parameter) == "Cuidad"):
        mydb = get_db()
        capitalize = filter.capitalize()
        todo_filter = mydb.db.todos.find({'Locatizacion.city': capitalize})
        cantidad = todo_filter.count()
        print("catidad", cantidad)
        return render_template('index.html', filters=todo_filter, cantidades=cantidad)

    if(str(parameter) == "GeoLocalización"):
        mydb = get_db()
        capitalize = filter.capitalize()
        todo_filter = mydb.db.todos.find({'Locatizacion.city': capitalize})
        cantidad = todo_filter.count()
        print("catidad", cantidad)
        return render_template('index.html', filters=todo_filter, cantidades=cantidad)

    else:
        msg = "Ups! algo salio mal :("
        return redirect(url_for('index'))

    
    

  