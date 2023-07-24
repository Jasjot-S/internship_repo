'''
Make an API which accepts csv file from user and inserts the data from csv file to postgres database.
The columns of the csv file are - id, first_name, last_name, email, gender.

Important - How we take csv file on API 
'''

from flask import *
import psycopg2
import pandas as pd
import os
import psycopg2.extras
from fileinput import filename

app = Flask(__name__)

def db_con():
    con = psycopg2.connect(host='127.0.0.1',
                           port=5432,
                           dbname = 'tvtracking',
                           password = 'prismpassword',
                           user = 'prismuser')
    
    return con

upload_folder = '/home/jasjot/Desktop/work/flask_tasks/uploads'
up_f = '/home/jasjot/Desktop/work/flask_tasks/uploads/{fname}'

insert_query = "INSERT INTO flask_dat ({cols}) VALUES (%s, %s, %s, %s, %s);"

app.config['upload_folder'] = upload_folder

@app.route('/post', methods = ['POST'])
def upload_dat():

    try:
        upload_file = request.files['file']
        upload_name = upload_file.filename

        if upload_name != '':
            file_path = os.path.join(app.config['upload_folder'], upload_name)
            upload_file.save(file_path)
            
        insert_dat(upload_name)
        return "Data transfer to table done"

    except:
        return "Please provide a valid file."

def insert_dat(file_name):
    data = pd.read_csv(up_f.format(fname = file_name))
    cols_tmp = data.columns
    cols_lst = ", ".join(cols_tmp)

    dat_lst = data.values.tolist()
    dat_lst = (tuple(x) for x in dat_lst)


    con = db_con()
    cur = con.cursor()
    psycopg2.extras.execute_batch(cur, insert_query.format(cols = cols_lst), dat_lst, page_size=100)
    con.commit()
    con.close()


if __name__ == '__main__':
    app.run(debug = True)