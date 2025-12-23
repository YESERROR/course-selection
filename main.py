import requests
import ddddocr
from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
session = requests.Session()
ocr = ddddocr.DdddOcr()
print("===========选课脚本===========")
username=input("用户名：")
password=input("密码：")

driver = webdriver.Chrome()
driver.get("https://cas.nyist.edu.cn/cas/login?service=https%3A%2F%2Fngjw.nyist.edu.cn%2Fadmin%2Fcaslogin")


# 用户名
username_input = driver.find_element(By.ID, "username")
username_input.send_keys(username)

# 密码
password_input = driver.find_element(By.ID, "password")
password_input.send_keys(password)

captcha_img = driver.find_element(By.ID, "captcha_img")
captcha_img.screenshot("captcha.png")

with open("captcha.png", "rb") as file:
    captcha = file.read()
result = ocr.classification(captcha)

captcha_input = driver.find_element(By.ID, "captcha")
captcha_input.send_keys(result)
# 登录
login_btn = driver.find_element(By.XPATH, '//input[@value="登录"]')
login_btn.click()
print("当前URL:", driver.current_url)
cookies = driver.get_cookies()

req_cookies = {c['name']: c['value'] for c in cookies}
session.cookies.update(req_cookies)
driver.quit()
headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.6778.86 Safari/537.36',
         'Accept':'application/json, text/plain, */*',
         'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8'}
response = session.post("https://ngjw.nyist.edu.cn/admin/xsd/xk/listV2",headers=headers)
print(f"\n状态码: {response.status_code}")
sports_data = response.json()
pcid, pcenc = next(iter(sports_data.get('data').get('pcencs').items()))
getlist={
    'from':'fjjx',
    'pcid':pcid,
    'pcenc':pcenc
}
headers2={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.6778.86 Safari/537.36',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'X-Requested-With': 'XMLHttpRequest',
    'Origin': 'https://ngjw.nyist.edu.cn',
    'Referer': 'https://ngjw.nyist.edu.cn/admin/xsd/xk/index',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty'
}
sports_list=session.post(
            url="https://ngjw.nyist.edu.cn/admin/xsd/xk/listjxbDataV2",
            data=getlist,
            headers=headers2)
print(f"\n状态码: {sports_list.status_code}")
courses=sports_list.json().get('data').get('initData')
for i in range(len(courses)):
    print(f'===========第{i}个：{courses[i].get("jxbmc")}============')
    print(f'人数：{courses[i].get("yxrl")}')
    print(f'地点：{courses[i].get("sksjdd")}')
    print(f'教师：{courses[i].get("teacher")}')


print('====================================\n'*3)
index=int(input("请选择第几个课程："))
print(f'你选择：{courses[index].get("jxbmc")}')

enter=session.post(
    url="https://ngjw.nyist.edu.cn/admin/xsd/xk/xsdXkV2",
    data={'jxbid':courses[index].get("id"),
          'pcid':pcid},
    headers=headers2)

print(f"选课结果：{enter.json().get('msg')}")
