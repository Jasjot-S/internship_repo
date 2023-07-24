from flask import *
from app.models.queries import search_query2, update_query
from app.utility.db_con import db_con
from app.models.hash import get_hash

@app.route('/reset_password/')
def reset_password():

    con = db_con()
    cur = con.cursor()

    try:
        email = request.form.get('email')
        new_pass = request.form.get('New password')
        hash_pass = get_hash(new_pass)
        cur.execute(search_query2.format(eid = email))
        db_pass = cur.fetchone()
        db_pass = str(db_pass[0])

        if db_pass == hash_pass:
            return {"status" : "false", "code" : 404, "message" : "New password cannot be the same as the old password."}
        else:
            cur.execute(update_query.format(pss = hash_pass, em = email))
            con.commit()
            con.close()
            return {"status" : "true", "code" : 201, "message" : "Password changed successfully"}

    except:
        return {"status" : "false", "code" : 404, "message":"Please enter valid password"}
    
 