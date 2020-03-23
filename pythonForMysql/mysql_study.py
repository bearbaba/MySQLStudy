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
        self.cursor.execute(sql, ('PHP', '史上最强'))
        self.db.commit()
        try:
            self.cursor.executemany(sql, [('Python', '人生苦短'), ('Java', '面向对象')])
            self.db.commit()
            print("插入数据成功")
        except:
            print("插入数据失败")
            self.db.rollback()

    def drop_column(self):
        sql = "alter table class drop column cname;"
        self.cursor.execute(sql)
        self.db.commit()

    def look_table(self):
        sql = "select cname,description from class where id % 2 = 1;"
        self.cursor.execute(sql)
        aa = self.cursor.fetchall()
        print(aa)
        for a, b in aa:
            print("语言：{}，描述：{}".format(a, b))

    def look_table_by_panda(self):
        import pandas as pd
        df = pd.read_sql("select * from class", self.db)
        print(df)

    def close(self):
        self.db.close()


if __name__ == '__main__':
    new_database = Database()
    new_database.create_database()
    new_database.create_table()
    new_database.insert_data()
    # new_database.drop_column()
    new_database.look_table()
    new_database.look_table_by_panda()
    new_database.close()
