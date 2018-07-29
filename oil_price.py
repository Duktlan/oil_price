import requests
from bs4 import BeautifulSoup
import pymysql
import time
import re

url="https://new.cpc.com.tw/division/mb/oil-more1-1.aspx"
reqs = requests.get(url)
soup = BeautifulSoup(reqs.text, 'html.parser')
p=soup.find_all("td",width="9%")
now_price=float(p[9].text)

url2="http://www.taiwanoil.org/"
req2 = requests.get(url2)
soup2 = BeautifulSoup(req2.text, 'html.parser')
err_price=soup2.find_all("tr",style="text-shadow:none;background-color:#eeeeee;font-size:12px;font-family:arial;")[3].find_all("font",color="red")[1]


db = pymysql.connect("localhost","root","","oil_price" )
cursor = db.cursor()
cursor.execute("DROP TABLE IF EXISTS oil_price_table")


sql= """CREATE TABLE oil_price_table (
        柴油油價 float NOT NULL,
        預測起伏 varchar(30) NOT NULL)"""
cursor.execute(sql)
sql = """INSERT INTO oil_price_table(柴油油價,預測起伏)
        VALUES (("%f"),("%s"))""" %\
        (now_price,err_price.text)
try:
    cursor.execute(sql)
    print("更新成功")
except:
    db.rollback()
    print("更新失敗")
db.close()
