#  `MySQL`的学习

为了能更好查看执行的结果，采用`Python`与`MySQL`进行交互。

需要安装`pymysql`库,执行以下命令以安装。

```powershell
pip install pymysql
```

##  连接操作

###  在命令行内连接数据库 

```powershell
mysql -uroot -p -P3306 -h 127.0.0.1
```

连接本地默认数据库可以用

```powershell
mysql -uroot -p
```

参数说明：

| 选项        | 说明          | 默认             |
| ----------- | ------------- | ---------------- |
| -u          | 账号          | 当前系统同名账号 |
| -p（小写p） | 密码          |                  |
| -P（大写P） | 连接端口      | 3306             |
| -h          | 主机地址      | 127.0.0.1        |
| -e          | 执行`sql`指令 |                  |

使用`-e`执行SQL语句：

```powershell
mysql -uroot -p -e"show databases;"
```

使用`exit`可退出连接



##  数据库的创建、使用、删除  

###  在`Python`中连接数据库  

```python
import pymysql
db=pymysql.connect(host="localhost",user="root",password="123456")#在MySQL5.7版本内使用该方式连接数据库
db=pymysql.connect(host="localhost",user="root",password="123456",port=3306,charset="utf8")#在MySQL8.0版本中多添加了几个参数用于连接  
```

在使用完后使用`db.close()`关闭数据库。  



###  命令行创建数据库   

在命令行中使用`create database 数据库名字 charset utf8; ` ，数据库名字自定义，`charset utf8`表明该数据库使用的编码方式是utf-8。MySQL使用`;`表示语句的结束。

创建完数据库后即可使用`show databases;`命令查看所有的数据库，

###  python创建数据库  

在python内在连接数据库之后，可以通过`cursor=db.cursor()`开启MySQL的游标功能，创建一个游标对象，再通过执行`cursor.execute(sql)#sql表示要执行的SQL语句` 

例如创建数据库

```python
import pymysql 
db=pymysql.connect(host='localhost',user='root', password='123456',
                   port=3306, db='huangwei', charset='utf8')              
cursor = db.cursor()
cursor.execute("create database new_databases charset utf8;")
```



###  使用数据库  

在命令行中用`use 数据库名;`即可使用数据库，python中同样在`execute()`中可以直接执行这句命令。  



###  删除数据库  

使用`drop database 数据库名`的方式进行删除操作，为防止删除不存在的数据库可以增加条件`drop database if exists houdunren;`



##  命令行导入外部SQL文件  

首先创建`test.sql`文件 

```powershell
create database test charset utf8;
show databases;
```

外部导入

```powershell
mysql -uroot -p < test.sql
```

连接后导入 

```powershell
mysql -uroot -p
>source test.sql
```



##  数据表管理  

数据库实际上就是多个表组成的，表中存储着数据。
数据表也是数据库最重要的组成部分之一，我们绝大多数情况下都是在跟表打交道。
例如从表里查找一些数据，删除表中的某些数据，更新表中的某些数据等等。

数据表由**行（row）**和**列(column)**组成，是一个二维的网格结构，每个列都是一个字段。
字段由字段名称和字段的**数据类型**以及一些**约束条件**组成
表中至少要有一列，可以有多行或0行，**表名要唯一**



###  创建数据表  

```mysql
create table class(
id int primary key AUTO_INCREMENT,
cname varchar(30) NOT NULL,
description varchar(100) default NULL)
charset utf8
```

以上操作创建一个表`class`，说明如下：

* 字段id为主键自增
* 字段cname为字符串类型varchar并不允许为null值
* 字段description可为null字符串
* 字符集为utf8，如果不设置将继承数据库字符集  

创建完表后就可以插入数据  

```mysql
INSERT INTO class (cname,description) VALUES('PHP','史上最强');
INSERT INTO class (cname) VALUES('Mysql');
```



pymysql模块是默认开启mysql的事务功能的，因此，进行 "增"、 "删"、"改"表内数据的时候，一定要使用`db.commit()`提交事务，否则就看不见所插入的数据。

因此使用`cursor.execute(sql)`执行SQL的插入语句后，一定要使用`db.commit()`提交事务。



上述的sql插入语句在python中可以改为:  

```python
sql="INSERT INTO class (cname,description) VALUES(%s,%s)"
cursor.execute(sql,('PHP','史上最强'))
db.commit()
```

如果要同时插入多条的语句可以使用`cursor.executemany()`，

```python
sql="INSERT INTO class (cname,description) VALUES(%s,%s)"
cursor,executemany(sql,[('PHP','史上最强'),('python','人生苦短')])
db.commit()
```



对于插入或者删除表中数据的操作时，务必要使用`try... except..`结构，如果对这些数据进行的操作失败后，就进行回滚操作，避免操作失败影响之后的数据的插入删除。  

```mysql
try:
	sql="INSERT INTO class (cname,description) VALUES(%s,%s)"
	cursor.execute(sql,('PHP','史上最强'))
	db.commit()
	print("插入成功")
except:
	print("插入失败")
	db.rollback()
```





###  表的操作

查看数据库内的所有表

```mysql
show tables;
```



根据已经存在的表结构创建新表

```mysql
create table test like class;
```

修改表名

```mysql
ALTER TABLE stu RENAME stus;
```

另一种方式修改表名

```mysql
RENAME TABLE stus to stu;
```



更改表的字符集

```mysql
ALTER TABLE class charset gbk;
```



删除表的所有数据

```mysql
TRUNCATE stu;
```

删除表

```mysql
DROP TABLE IF EXISTS stu;
```



查看表的内容

```mysql
desc tablename;
```



在`python`中查看表内容  

1. `fetchall`一次获取所有记录

```mysql
import  pymysql

db = pymysql.connect(host='localhost',user='root',db='huangwei',
                     password='123456',port=3306,charset='utf8')

cursor = db.cursor()

cursor.execute('select name,age from person')
aa = cursor.fetchall()
# print(aa)
for a,b in aa:
    c = "我的名字叫{}，今年{}岁".format(a,b)
    display(c)
db.close()
```



2. 使用`pandas`查看内容

使用pandas中的read_sql()方法，将提取到的数据直接转化为DataFrame，进行操作

```mysql
import pymysql 
import pandas as pd

db = pymysql.connect(host='localhost',user='root',db='huangwei',
                     password='123456',port=3306,charset='utf8')
cursor = db.cursor()

df1 = pd.read_sql("select * from student where ssex='男'",db)
display(df1)
df2 = pd.read_sql("select * from student where ssex='女'",db)
display(df2)
```



修改表类型  

例如，修改表emp的ename字段定义，将`varchar(10)`改为`varchar(20)`：   

```mysql
alter table emp modify ename varchar(20);
```



增加表字段  

例如，表emp上新增加字段age，类型为int(3)：

```mysql
alter table emp add column age int(3);
```



删除表字段

例如，删除表emp上的age列：

```mysql
alter table emp drop column age;
```



更改列的名称  

例如，将表emp上的age列改名为age1列,同时将字段更改为int(4)：

```mysql
alter table emp change age age1 int(4);
```

`change`能更改列的名称，在使用时必须要指明列的字段类型，不然会报错。



修改字段的排列顺序  

在字段增加和修改语法（ADD/CHANGE/MODIFY）中都有一个可选项`first|after column_name`，这个选项可修改字段在表中的位置，默认`add`增加的新字段是加在表的最后的位置，而`change/modify`默认不会更改字段的位置。  

例如，将新增的字段birth date（data是字段类型）加在ename之后，需要指明字段类型。  

```mysql
alter table emp add birth date after ename;
```

例如，修改字段age，将它放在最前面：

```mysql
alter table emp modify age int(3) first;
```



##  DML语句  

DML操作是指对数据库中表记录的操作，主要包括表记录的插入（insert）、更新（update）、删除（delete）和查询（select）。

###  插入记录  

插入记录的基本语法为：
`INSERT INTO tablename (field1,field2,.....,fieldn) VALUES (value1, value2,......valuesn);` 

例如：向表emp中插入一下记录：ename为zzx1，hiredate为2000-01-01，sal为2000，deptno为1，命令执行为：

```mysql
insert into emp (ename, hiredate,sal,deptno) values('zzx1','2000-01-01','2000',1);
```

也可以不用指定字段名称，但是`values`后面的顺序和字段的排列顺序一致：

```mysql
insert into emp values ('zzx1','2000-01-01','2000',1)
```

可以一次插入大量数据：

```mysql
INSERT INTO tablename (field1, field2,……fieldn)
VALUES
(record1_value1, record1_value2,……record1_valuesn),
(record2_value1, record2_value2,……record2_valuesn),
……
(recordn_value1, recordn_value2,……recordn_valuesn)
;
```



###  更新记录  

对于表里的记录值，可以通过`update`命令进行更改，语法如下：

```mysql
UPDATE tablename SET field = vluae1,field=value2, ....fieldn=valuen[WHERE CONDITION]
```

例如，将表emp中ename为“lisa”的薪水（sal）从3000更改为4000： 

```mysql
update emp set sal=4000 where ename="lisa";
```

在MySQL中，update可以同时更新多个表中数据，语法为：

```mysql
update t1,t2...tn set t1.field1=expr1,tn.fieldn=exprn [WHERE CONDITION]
```

在下例中，同时更新表emp中的字段sal和表dept中的字段deptname：

```mysql
update emp a,dept b set a.sal=a.sal*b.deptname=a.ename where a.deptno = b.deptno;
```

上例中a是emp的别名，b是dept的别名，可见设置别名只需在表名后附上别名即可。



###  删除记录  

可以使用`delete`命令进行删除，语法为：  

```mysql
DELETE FROM tablename [WHERE CONDITION]
```

例如，在emp中将ename为‘dony’的记录全部删除：

```mysql
delete from emp where ename='dony';
```



在MySQL中可以一次删除多个表的数据，语法为：

```mysql
DELETE t1,t2...tn FROM t1,t2...tn [WHERE CONDITION]
```



例，将表 emp 和 dept 中 deptno 为 3 的记录同时都删除：

```mysql
delete a,b from emp a,dept b where a.deptno=b.deptno and a.deptno=3;
```

如果 from 后面的表名用别名，则 delete 后面的也要用相应的别名，否则会提示语法错误。



