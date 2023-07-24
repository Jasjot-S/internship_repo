import psycopg2

def db_con():
    con = psycopg2.connect(host='127.0.0.1',
                        port=5432,
                        dbname = 'tvtracking',
                        password = 'prismpassword',
                        user = 'prismuser')

    return con
