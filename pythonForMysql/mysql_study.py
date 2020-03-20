import pymysql


class Database():
    def __init__(self):
        self.db = pymysql.connect("localhost", "root", "mysql2020")
        self.cursor = self.db.cursor()

    def create_database(self):
        try:
            self.cursor.execute("create database new_database;")
        except pymysql.err.ProgrammingError:
            self.cursor.execute("drop database if exists new_database;")
            self.cursor.execute("create database new_database;")

    def create_table(self):
        self.cursor.execute("use new_database;")
        sql = '''
        create table class (
        id int primary key AUTO_INCREMENT,
        cname varchar(30) NOT NULL,
        description varchar(100) default NULL) 
        charset utf8;
        '''
        self.cursor.execute(sql)

    def insert_data(self):
        sql = "INSERT INTO class (cname,description) VALUES(%s,%s);"
        self.cursor.execute(sql,('PHP','史上最强'))
        self.db.commit()
        self.cursor.executemany(sql,[('Python','人生苦短'),('Java','面向对象')])
        self.db.commit()
    def close(self):
        self.db.close()


if __name__ == '__main__':
    new_database = Database()
    new_database.create_database()
    new_database.create_table()
    new_database.insert_data()
    new_database.close()
