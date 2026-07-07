#login and sigup system 

from flask import Flask,request,sessions,redirect,url_for
from werkzeug.security import generate_password_hash,check_password_hash
import sqlite3

app =Flask(__name__)
DB = "user.data"

def base_connection():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    conn.commit()
    return conn 

def init_db():
    with base_connection() as db:
        db.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER , buisness_name TEXT, buisness_type TEXT, Founder_names TEXT ,email_id TEXT, password TEXT)")
        db.commit()

@app.route("/signin" ,methods = ['POST'])
def info():
    data = request.get_json()
    id = data.get('id')
    buisness_name = data.get('buisness_name')
    buisness_type = data.get('buisness_type')
    Founder_names = data.get('Founder_names')
    email_id = data.get('email_id')
    password = data.get('password')

    if not buisness_name or not buisness_type or not Founder_names or not email_id or not password:
        return {
            'error':"Please provide the given information correctly"
        }
    
    hashed_password = generate_password_hash(password)

    with base_connection() as db:
        db.execute("INSERT INTO  user (id,buisness_name, buisness_type,Founder_names,email_id, password) VALUES(?,?,?,?,?,?)", (id,buisness_name,buisness_type,Founder_names,email_id,hashed_password))
        db.commit()

        return{
            'Login':"Buisness account created succesfully"
        }

#login route
@app.route("/login", methods = ['POST'])
def login():
    data = request.get_json()
    id = data.get('id')
    buisness_name = data.get('buisness_name')
    buisness_type = data.get('buisness_type')
    Founder_names = data.get('Founder_names')
    email_id = data.get('email_id')
    password = data.get('password')

    with base_connection() as db:
        cursor = db.execute(
            "SELECT * FROM users WHERE buisness_name = ?",
            (buisness_name,)
        )
        result = cursor.fetchone()

        if result:
            #  MUST use check_password_hash to verify
            if check_password_hash(result['password'], password):
                sessions['user']= ['name']
                return redirect(url_for('home')) 
            else:
                return ({"message": "Wrong password!"}), 401
        else:
            return ({"message": " User not found!"}), 404
        
@app.route("/home" , methods =['POST','GET'])
def home_page():