# 南阳理工学院自动抢体育课系统
## 有效期 2025年12月23日

### 重要 url 
> https://ngjw.nyist.edu.cn/admin/xsd/xk/listV2

获取选课的类型，如体育课，选修课

> https://ngjw.nyist.edu.cn/admin/xsd/xk/listjxbDataV2

获取体育课的课程 

> https://ngjw.nyist.edu.cn/admin/xsd/xk/xsdXkV2 

提交选课结果

### 安装依赖
```bash
pip install requests
```

直接运行，会检查***储存在本地cookie的值***，请妥善保存。若过期，则需要账号密码登录。
```bash
python3 main.py
```

***注意***：
1. 需要安装谷歌游览器,运行时会弹出，***请不要关闭***
2. 在本地生成`cookie.txt`为保存的cookie