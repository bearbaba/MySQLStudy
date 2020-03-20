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

