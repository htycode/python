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
driver = webdriver.Chrome()
driver.implicitly_wait(5) #  隐式等待


吾爱破解.签到(driver,"1126875067","341223.hty")

