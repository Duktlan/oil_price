#引入函示庫
import requests
from bs4 import BeautifulSoup
import pymysql
import time
import re

#利用get取得資料
url="https://new.cpc.com.tw/division/mb/oil-more1-1.aspx"
reqs = requests.get(url)
soup = BeautifulSoup(reqs.text, 'html.parser')
p=soup.find_all("td",width="9%")
now_price=float(p[9].text)

url2="http://www.taiwanoil.org/"
req2 = requests.get(url2)
soup2 = BeautifulSoup(req2.text, 'html.parser')
err_price=soup2.find_all("tr",style="text-shadow:none;background-color:#eeeeee;font-size:12px;font-family:arial;")[3].find_all("font",color="red")[1]



'''date_list=[]
date=soup.find_all("div","date")
for date in date:
    date_list=(date.find_all("span"))
new_date=str(date_list[0].text)+"年"+str(date_list[1].text)+"月"+str(date_list[2].text)+"日"'''

# 打开数据库连接
db = pymysql.connect("localhost","root","","oil_price" )

# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()
# 使用 execute() 方法执行 SQL，如果表存在则删除
cursor.execute("DROP TABLE IF EXISTS oil_price_table")

# 创建表
sql= """CREATE TABLE oil_price_table (
        柴油油價 float NOT NULL,
        預測起伏 varchar(30) NOT NULL)"""

cursor.execute(sql)

# SQL 插入语句
sql = """INSERT INTO oil_price_table(柴油油價,預測起伏)
        VALUES (("%f"),("%s"))""" %\
        (now_price,err_price.text)
try:
    # 执行sql语句
    cursor.execute(sql)
    # 提交到数据库执行
    db.commit()
    print("更新成功")
except:
    # 如果发生错误则回滚
    db.rollback()
    print("更新失敗")

# 关闭数据库连接
db.close()

#tdList = soup.find(id = 'formTable').find('tbody').find_all('tr')[5].find_all('td')