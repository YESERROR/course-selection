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

直接运行
```bash
python3 main.py
```

***注意***：需要先通过登录获取cookie

先登录，打开f12到网络经行抓包，获取cookie
![img.png](img.png)