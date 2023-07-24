
from flask import *
from app.models.mail import mail_api
from app.utility.db_con import db_con
from app.models.queries import search_query

@app.route('/forgot_password', methods = ['POST'])
def forgot_password():
    con = db_con()
    cur = con.cursor()

    try:
        email = request.form.get('email')
        cur.execute(search_query.format(ead = email))
        exists = cur.fetchone()[0]

        if exists > 0:
            mail_api(email)
            return {"status": "true", "code" : 200,"message" : "Please check your email to reset your password."}
        else:
            return {"status" : "false", "code" : 404, "message":"Sorry the user does not exist"} 
        
    except:
        return {"status" : "false", "code" : 404, "message":"Please enter a valid email address"} 
    
