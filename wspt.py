import requests
import pyperclip
import socket
import base64
import http.client
import json
import os
import sys
import logging
import time
import urllib.parse
import re
import datetime
##借用了Zy143L大佬代码用以适配v4，仅供龙宫传阅，切勿外传
requests.packages.urllib3.disable_warnings()
os.environ['no_proxy'] = '*'

def cloud_info():
    url = str(base64.b64decode(url_t).decode()) + 'check_api'
    for i in range(3):
        try:
            headers = {"authorization": "Bearer Shizuku"}
            res = requests.get(url=url, verify=False, headers=headers, timeout=20).text
        except requests.exceptions.ConnectTimeout:
            #logger.info("\n获取云端参数超时, 正在重试!" + str(i))
            time.sleep(1)
            continue
        except requests.exceptions.ReadTimeout:
            #logger.info("\n获取云端参数超时, 正在重试!" + str(i))
            time.sleep(1)
            continue
        except Exception as err:
            #logger.info("\n未知错误云端, 退出脚本!")
            #logger.debug(str(err))
            sys.exit(1)
        else:
            try:
                c_info = json.loads(res)
            except Exception as err:
                #logger.info("云端参数解析失败")
                #logger.debug(str(err))
                sys.exit(1)
            else:
                return c_info

def check_cloud():
    url_list = ['aHR0cDovLzQzLjEzNS45MC4yMy8=', 'aHR0cHM6Ly9zaGl6dWt1Lm1sLw==', 'aHR0cHM6Ly9jZi5zaGl6dWt1Lm1sLw==']
    for i in url_list:
        url = str(base64.b64decode(i).decode())
        try:
            requests.get(url=url, verify=False, timeout=10)
        except Exception as err:
            #logger.debug(str(err))
            continue
        else:
            info = ['Default', 'HTTPS', 'CloudFlare']
            #logger.info(str(info[url_list.index(i)]) + " Server Check OK\n--------------------\n")
            return i


def getToken(ws):
	url = str(base64.b64decode(url_t).decode()) + 'genToken'
	header = {"User-Agent": ua}
	params = requests.get(url=url, headers=header, verify=False, timeout=20).json()
	headers = {
        'cookie': ws,
        'user-agent': ua,
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'charset': 'UTF-8',
        'accept-encoding': 'br,gzip,deflate'
    }
    
    # url = 'https://api.m.jd.com/client.action?functionId=genToken&clientVersion=10.1.2&client=android&lang=zh_CN&uuid=09d53a5653402b1f&st=1630392618706&sign=53904736db53eebc01ca70036e7187d6&sv=120'
	url = 'https://api.m.jd.com/client.action'
	data = 'body=%7B%22to%22%3A%22https%253a%252f%252fplogin.m.jd.com%252fjd-mlogin%252fstatic%252fhtml%252fappjmp_blank.html%22%7D&'
	#data = 'body=%7B%22action%22%3A%22to%22%2C%22to%22%3A%22https%253A%252F%252Fh5.m.jd.com%252Frn%252F2E9A2bEeqQqBP9juVgPJvQQq6fJ%252Findex.html%253Fhas_native%253D0%2526source%253Dwojing2%2526tttparams%253DkDyAzeeyJnTGF0IjoiMzEuMjM4MjM4IiwiZ0xuZyI6IjEyMS40NDI3NDUifQ6%25253D%25253D%22%7D&'
	res = requests.post(url=url, params=params, headers=headers, data=data, verify=False)
	# print(res.text)
	res_json = json.loads(res.text)
	totokenKey = res_json['tokenKey']
	# print("Token:", totokenKey)
	appjmp(totokenKey)


def appjmp(token):
    headers = {
        'User-Agent': 'jdapp;android;10.1.2;10;7323234356637333-1603230323260366;network/wifi;model/EBG-AN10;addressid/838684921;aid/7224e673a0202b0f;oaid/00000000-0000-0000-0000-000000000000;osVer/29;appBuild/89760;partner/huaweiharmony;eufv/1;jdSupportDarkMode/0;Mozilla/5.0 (Linux; Android 10; EBG-AN10 Build/HUAWEIEBG-AN10; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/77.0.3865.120 MQQBrowser/6.2 TBS/045713 Mobile Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'x-requested-with': 'com.jingdong.app.mall'
    }
    params = {
        'tokenKey': token,
        'to': 'https://plogin.m.jd.com/jd-mlogin/static/html/appjmp_blank.html',
    }
    # url = 'https://un.m.jd.com/cgi-bin/app/appjmp?tokenKey={0}&to=https%3A%2F%2Fplogin.m.jd.com%2Fcgi-bin%2Fm%2Fthirdapp_auth_page%3Ftoken%3DAAEAIEijIw6wxF2s3bNKF0bmGsI8xfw6hkQT6Ui2QVP7z1Xg%26client_type%3Dandroid%26appid%3D879%26appup_type%3D1'.format(token)
    url = 'https://un.m.jd.com/cgi-bin/app/appjmp'
    # print(url)
    # res = requests.get(url=url, headers=headers, verify=False, allow_redirects=False)
    res = requests.get(url=url, headers=headers, params=params, verify=False, allow_redirects=False)
    # print(res.headers)
    # print(res.status_code)
    res_set = res.cookies.get_dict()
    pt_key = 'pt_key=' + res_set['pt_key']
    pt_pin = 'pt_pin=' + res_set['pt_pin']
    ck = str(pt_key) + ';' + str(pt_pin) + ';'
    print(ck)
    pyperclip.copy(ck)
    print("已复制到剪切板")
    # print(res.text)


if __name__ == '__main__':
    os.system('chcp 65001')
    print("Ver: 0.1")
    print("limoe")
    url_t = check_cloud()
    cloud_arg = cloud_info()
    ua = cloud_arg['User-Agent']
    print("请输入格式为pin=xxx;wskey=xxx;")
    ws = input()
    getToken(ws)
    os.system('pause')
    
