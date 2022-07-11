from bs4 import BeautifulSoup
from selenium import webdriver
from apscheduler.schedulers.blocking import BlockingScheduler
import xml.dom.minidom as minidom
from datetime import datetime
import numpy
import requests
import bs4
import json
import sqlite3
import sched
import time
import os

#base_url = 'https://interface.sina.cn/news/wap/fymap2020_data.d.json?_={}&callback=Zepto{}'
base_url = 'https://markets.businessinsider.com/Ajax/Chart_GetChartData?instrumentType=ExchangeRate&tkData=300011,675,,&from=20130526&to={}'

start_page = 1
start_id = 0
limit_num = 350

sqlite_file = 'E:/pyproject/bitcoin/bitcoin.db'    # name of the sqlite database file
table_name1 = 'heimaotousu'	# name of the table to be created
conn=None
c=None
total_time = 0
xml_path=''

xml_path = os.getcwd()
sqlite_file = xml_path + '\\bitcoin.db'
xml_path = xml_path + '\system.xml'

print(sqlite_file+'\n')
print(xml_path+'\n')


#
# get html content
#
def get_html_ex(url):
    driver.get(url)
    time.sleep(1)
    bFind = False
    source = ''
    try:
        if '<html><head></head><body><pre style=\"word-wrap: break-word; white-space: pre-wrap;\">' in str(driver.page_source):
            bFind = True    
    except requests.exceptions.RequestException:
        return None 
    
    if bFind == True:
        source = driver.page_source

    return source
#
# get html content
#
def get_html(url):
    try:
        response = requests.get(url)
        response.encoding = 'utf-8'
        if response.status_code == 200:
            return response.text
        print(url,response.status_code)
        return None
    except requests.exceptions.RequestException:
        return None 

def createdb(table_name):
    # Connecting to the database file
    
    conn = sqlite3.connect(sqlite_file)
    c = conn.cursor()  
    exec_sql = 'CREATE TABLE IF NOT EXISTS {} (Close VARCHAR(32),         \
                                 Open VARCHAR(32),       \
                                 High VARCHAR(32), \
                                 Low VARCHAR(32),      \
                                 Volume VARCHAR(32),\
                                 Date VARCHAR(128))'.format(table_name)

    try:
        c.execute(exec_sql)
    except sqlite3.IntegrityError as err:
        print(str(err))
    conn.commit()
    conn.close()

def writedb(table_name,Close, Open, High, Low, Volume, Date):
        # Connecting to the database file
    conn = sqlite3.connect(sqlite_file)
    c = conn.cursor()
    #isExist = isexist(sn)
    isExist = False
    if isExist == False:
        sql_cmd = 'insert into {} (Close, Open, High, Low, Volume, Date) values (\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\')'.format(table_name,Close, Open, High, Low, Volume, Date)
        try:
            c.execute(sql_cmd)
        except sqlite3.IntegrityError as err:
            print(str(err))
        conn.commit() 
        conn.close() 
        return True
    else:
        return False

def isexist(sn):   
    conn = sqlite3.connect(sqlite_file)
    c = conn.cursor()
    sql_cmd = 'select * from {} where sn=\'{}\''.format(table_name1,sn)
    try:
        data = c.execute(sql_cmd)
        row = data.fetchone()
        if row != None:
            conn.close() 
            return True
    except sqlite3.IntegrityError as err:
        print(str(err))
    conn.close() 
    return False    

def emptyTable(table_name):   
    conn = sqlite3.connect(sqlite_file)
    c = conn.cursor()
    sql_cmd = 'delete from {}'.format(table_name)
    try:
        c.execute(sql_cmd)
    except sqlite3.IntegrityError as err:
        print(str(err))
    conn.commit() 
    conn.close() 
    return False         

def parse_Bitcoin_info(table,html):
    infos = json.loads(html)
    for info in infos:
        isSuccess = False
        isSuccess = writedb(table,info['Close'],info['Open'],info['High'],info['Low'],info['Volume'],info['Date']) 
        if isSuccess == True:
            data = {
                'Close':info['Close'],
                'Open':info['Open'],
                'High':info['High'],
                'Low':info['Low'],
                'Volume':info['Volume'],
                'Date':info['Date']
            }
            print(data)

def get_Bitcoin_info(table,url):
    html = get_html(url)
    if html != None :
        parse_Bitcoin_info(table,html)   

def beginTask():
#    start_id = int(time.time()*1000)
    url = base_url.format(time.strftime('%Y%m%d',time.localtime(int(time.time()))))
    get_Bitcoin_info('bitcoinhistoryinfo',url) 



def main():
    
#    get_news() 
#    get_top_news()
#    writeEmptyXml()
    createdb('bitcoinhistoryinfo')
    emptyTable('bitcoinhistoryinfo')
    beginTask()
# BlockingScheduler
#    sched = BlockingScheduler()
#    sched.add_job(beginTask, 'interval', seconds=60)
#    sched.start()

if __name__ == "__main__":
#    driver = webdriver.Chrome(executable_path=r"D:\chromedriver_win32\chromedriver.exe")
#    driver.maximize_window()  
    main()   
#    driver.quit()
