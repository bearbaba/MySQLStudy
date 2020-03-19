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



###  在`Python`中连接数据库  

```python
import pymysql
db=pymysql.connect(host="localhost",user="root",password="123456")#在MySQL5.7版本内使用该方式连接数据库
db=pymysql.connect(host="localhost",user="root",password="123456",port=3306,charset="utf8")#在MySQL8.0版本中多添加了几个参数用于连接  
```

