from flask import *
from app.utility.db_con import db_con
import requests
from app.models.queries import search_query, search_query2
from app.models.hash import get_hash

@app.route('/login', methods = ['POST'])
def login_db():
    con = db_con()
    cur = con.cursor()


    if request.method == 'POST':
        try:    
            email = request.form.get('email')
            password = request.form.get('password')
            hash_pass = get_hash(password)
            cur.execute(search_query.format(ead = email))
            exists = cur.fetchone()[0]

            if exists > 0:
                cur.execute(search_query2.format(eid = email))
                db_pass = cur.fetchone()
                db_pass = str(db_pass[0])
        
                if db_pass == hash_pass:
                    return {"sttus" : "true", "code" : 200, "message" : "Login Soccessful"}
                else:
                    return {"status" : "false", "code" : 404, "message" : "Incorrect password, please enter it again"} 
            else:
                return {"status" : "false", "code" : 404, "message" : "Sorry user not found"} 

        except:
            return {"status" : "false", "code" : 404, "message" : "Please enter valid credentials"}  

    con.commit()
    con.close()
