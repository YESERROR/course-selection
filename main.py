import requests
session = requests.Session()
print("===========选课脚本===========")
cookie_input =input("输入cookie:")
cookies = {}
if cookie_input:
    for item in cookie_input.split(';'):
        if '=' in item:
            key, value = item.strip().split('=', 1)
            cookies[key] = value
session.cookies.update(cookies)
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
