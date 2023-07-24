
insert_query = """insert into users (name,email,password) values (%s,%s,%s);"""
search_query = """select count(*) from users where email = '{ead}';"""
search_query2 = """select password from users where email = '{eid}'"""
update_query = """update users set password = '{pss}' where email = '{em}'"""
