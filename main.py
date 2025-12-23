import requests
import ddddocr
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os
import json

BASE_URL = "https://ngjw.nyist.edu.cn"
COOKIE_FILE = "cookies.txt"

session = requests.Session()
ocr = ddddocr.DdddOcr()

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.6778.86 Safari/537.36',
    'Accept': 'application/json, text/plain, */*',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
}

AJAX_HEADERS = {
    'User-Agent': HEADERS['User-Agent'],
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'X-Requested-With': 'XMLHttpRequest',
    'Origin': BASE_URL,
    'Referer': f'{BASE_URL}/admin/xsd/xk/index',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty'
}


def get_cookie():
    """使用 selenium 登录并保存 cookie"""
    username = input("用户名：")
    password = input("密码：")

    driver = webdriver.Chrome()
    driver.get(
        "https://cas.nyist.edu.cn/cas/login"
        "?service=https%3A%2F%2Fngjw.nyist.edu.cn%2Fadmin%2Fcaslogin"
    )

    driver.find_element(By.ID, "username").send_keys(username)
    driver.find_element(By.ID, "password").send_keys(password)

    captcha_img = driver.find_element(By.ID, "captcha_img")
    captcha_img.screenshot("captcha.png")

    with open("captcha.png", "rb") as f:
        captcha = f.read()

    code = ocr.classification(captcha)
    print(f"识别验证码：{code}")

    driver.find_element(By.ID, "captcha").send_keys(code)
    driver.find_element(By.XPATH, '//input[@value="登录"]').click()

    time.sleep(2)

    if "cas/login" in driver.current_url:
        driver.quit()
        raise RuntimeError("登录失败，请重新运行")

    cookies = {c['name']: c['value'] for c in driver.get_cookies()}
    with open(COOKIE_FILE, "w", encoding="utf-8") as f:
        json.dump(cookies, f, ensure_ascii=False, indent=2)

    driver.quit()
    print("Cookie 获取成功")
    os.remove("captcha.png")


def load_cookie():
    if not os.path.exists(COOKIE_FILE):
        print("cookie 不存在，重新登录")
        get_cookie()

    with open(COOKIE_FILE, "r", encoding="utf-8") as f:
        cookies = json.load(f)

    session.cookies.clear()
    session.cookies.update(cookies)


def request_with_relogin(url, *, data=None, headers=None, retry=True):
    """
    自动处理 ret == -2（登录超时）
    只重试一次
    """
    resp = session.post(url, data=data, headers=headers)
    try:
        js = resp.json()
    except Exception:
        return resp

    if js.get("ret") == "-2" and retry:
        print("登录超时，重新登录一次...")
        get_cookie()
        load_cookie()
        return request_with_relogin(
            url, data=data, headers=headers, retry=False
        )

    return resp


def get_pcinfo():
    resp = request_with_relogin(
        f"{BASE_URL}/admin/xsd/xk/listV2",
        headers=HEADERS
    )
    data = resp.json()["data"]["pcencs"]
    return next(iter(data.items()))  # pcid, pcenc


def get_course_list(pcid, pcenc):
    resp = request_with_relogin(
        f"{BASE_URL}/admin/xsd/xk/listjxbDataV2",
        data={
            "from": "fjjx",
            "pcid": pcid,
            "pcenc": pcenc
        },
        headers=AJAX_HEADERS
    )
    return resp.json()["data"]["initData"]


def select_course(course, pcid):
    resp = request_with_relogin(
        f"{BASE_URL}/admin/xsd/xk/xsdXkV2",
        data={
            "jxbid": course["id"],
            "pcid": pcid
        },
        headers=AJAX_HEADERS
    )
    print("选课结果：", resp.json().get("msg"))


def main():
    print("=========== 选课脚本 ===========")
    print("检查本地cookie中。。。。。。。。。。")
    load_cookie()

    pcid, pcenc = get_pcinfo()
    courses = get_course_list(pcid, pcenc)

    for i, c in enumerate(courses):
        print(f"\n====== 第 {i} 个 ======")
        print("课程：", c["jxbmc"])
        print("人数：", c["yxrl"])
        print("地点：", c["sksjdd"])
        print("教师：", c["teacher"])

    index = int(input("\n请选择课程编号："))
    print("你选择了：", courses[index]["jxbmc"])

    select_course(courses[index], pcid)


if __name__ == "__main__":
    main()
