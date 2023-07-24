from flask import *
import hashlib
import psycopg2
import requests


app = Flask(__name__)


def db_con():
    con = psycopg2.connect(host='127.0.0.1',
                        port=5432,
                        dbname = 'tvtracking',
                        password = 'prismpassword',
                        user = 'prismuser')

    return con;

insert_query = """insert into users (name,email,password) values (%s,%s,%s);"""
search_query = """select count(*) from users where email = '{ead}';"""
search_query2 = """select password from users where email = '{eid}'"""
update_query = """update users set password = '{pss}' where email = '{em}'"""

def get_hash(string):
    tmp = hashlib.md5()
    tmp.update(string.encode('utf-8'))    
    return tmp.hexdigest()


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


def mail_api(email):
    url = "https://emailapi.silverpush.co/mail/"

    payload = {'To': '',
    'Subject': 'Reset Password ',
    'From': 'reports@chocolateplatform.com',
    'Body': 'Please use the link below to reset your password: ',
    'Name': 'Gen AI '}
    payload['To'] = email
    files = []
    headers = {}

    response = requests.request("POST", url, headers=headers, data=payload, files=files)

    print(response.text)


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
    
    

if __name__ == '__main__':
    app.run(debug = True)
