from flask import *
from app.utility.db_con import db_con
from app.models.hash import get_hash
from app.models.queries import insert_query

@app.route('/signup', methods = ['POST'])
def signup():

    con = db_con()
    cur = con.cursor()

    try:
        email = request.form.get('email')
        name = request.form.get('name')
        password = request.form.get('password')
        h_pass = get_hash(password)
        cur.execute(insert_query, (name, email, h_pass))    
    except:
        return {"status" : "false", "code" : 404, "message" : "Please enter valid details."}  

    con.commit()
    con.close()
    return {"status" : "true", "code" : 200, "message" : "Signup successful"}