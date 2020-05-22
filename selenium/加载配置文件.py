# coding=utf-8
'''
加载所有Chrome配置
-用Chrome地址栏输入chrome://version/
-查看自己的“个人资料路径”
-然后在浏览器启动时，调用这个配置文件，代码如下：
'''

from selenium import webdriver

option = webdriver.ChromeOptions()
option.add_argument(r'--user-data-dir=C:\Users\Administrator\AppData\Local\Google\Chrome\User Data')  # 设置成用户自己的数据目录
# 修改浏览器的User-Agent来伪装你的浏览器访问手机m站
option.add_argument('user-agent="MQQBrowser/26 Mozilla/5.0 (Linux; U; Android 2.3.7; zh-cn; MB200 Build/GRJ22; CyanogenMod-7) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1"')

# 浏览器启动时安装crx扩展
option.add_extension('d:\crx\AdBlock_v2.17.crx') #自己下载的crx路径

driver = webdriver.Chrome(chrome_options=option)






















