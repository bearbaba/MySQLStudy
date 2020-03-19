import pymysql
db=pymysql.connect("localhost", "root", "mysql2020")
cursors=db.cursors()
cursors.execute("create databases new_databases")