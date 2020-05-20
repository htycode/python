from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from time import sleep
from selenium.webdriver.common.action_chains import ActionChains
'''
在浏览器文件位置打开cmd
输入:
chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\selenum\AutomationProfile"
'''



# 主函数>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
def 签到(driver,account,password):
    driver.get("https://www.52pojie.cn/");sleep(3)  # 打开主页
    源码 = driver.page_source
    if "dep.x" in 源码:
        print("已登录")
    else:
        login_by_QQ(driver,account,password)

    driver.get("https://www.52pojie.cn/")
    sleep(2)
    driver.find_element_by_xpath('//*[@id="um"]/p[2]/a[1]/img').click()
    print("吾爱破解_签到成功")




def login_by_QQ(driver,account,password):
    # QQ登录
    driver.get("https://www.52pojie.cn/")
    driver.find_element_by_xpath('//*[@id="lsform"]/div/div[2]/p[1]/a/img').click()
    # 进入qq登录
    driver.switch_to.frame(driver.find_element_by_id("ptlogin_iframe"))
    driver.find_element_by_id("switcher_plogin").click()  # 点击账号密码登录
    # 输入帐号
    driver.find_element_by_id("u").clear()
    driver.find_element_by_id("u").send_keys(account)
    # 输入密码
    driver.find_element_by_id("p").clear()
    driver.find_element_by_id("p").send_keys(password)
    # 点击登录
    sleep(1);
    driver.find_element_by_id("login_button").click()
    sleep(1);
    driver.switch_to.default_content()
    print("吾爱破解_登陆成功")



