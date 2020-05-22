from selenium import webdriver
import 吾爱破解
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from time import sleep
from selenium.webdriver.common.action_chains import ActionChains
'''
在浏览器文件位置打开cmd
输入:
chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\selenum\AutomationProfile"
'''


chrome_options = webdriver.ChromeOptions()
mobile = {"deviceName":"Galaxy S5"}


# "mobileEmulation", mobile
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
chrome_options.add_argument('user-agent="MQQBrowser/26 Mozilla/5.0 (Linux; U; Android 2.3.7; zh-cn; MB200 Build/GRJ22; CyanogenMod-7) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1"')
chrome_driver = "C:\Python37\chromedriver.exe"
driver = webdriver.Chrome(chrome_driver, options=chrome_options)
driver.implicitly_wait(5) #  隐式等待


吾爱破解.签到(driver,"1126875067","341223.hty")

