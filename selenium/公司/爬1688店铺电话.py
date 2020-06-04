from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from time import sleep
from selenium.webdriver.common.action_chains import ActionChains
import re
import requests
'''
在浏览器文件位置打开cmd
输入:
chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\selenum\AutomationProfile"

'''
chrome_options = webdriver.ChromeOptions()
mobile = {"deviceself.name":"Galaxy S5"}
# "mobileEmulation", mobile
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
chrome_options.add_argument('user-agent="MQQBrowser/26 Mozilla/5.0 (Linux; U; Android 2.3.7; zh-cn; MB200 Build/GRJ22; CyanogenMod-7) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1"')
driver = webdriver.Chrome(options=chrome_options)
print(driver.title)

# 封装函数#############################################
class 爬取1688_phone:
    def __init__(self):
        self.headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'max-age=0',
            # 'cookie': 'cna=uPJUFxmPhCwCAbR3GHoSl1xl; UM_distinctid=17254c2cdc81d5-0e42093353349e-d373666-100200-17254c2cdc940b; taklid=91ccfc8d98144596adf6b4fed9ab4395; ali_beacon_id=180.119.24.122.1590559955185.481463.2; h_keys="%u6709%u9650%u516c%u53f8"; ali_ab=180.119.24.122.1590560013181.5; lid=t_1493565210967_0515; ali_apache_track=c_mid=b2b-299020775014ef0|c_lid=t_1493565210967_0515|c_ms=1; last_mid=b2b-299020775014ef0; cookie2=1a5b2e09824e6643f23733a2bcb2a65d; t=d5f0504094442d001644cd613e43ba46; _tb_token_=535bbaede368e; alicnweb=touch_tb_at%3D1590626846640%7Clastlogonid%3Dt_1493565210967_0515; cookie1=BxZjKG0ztSSTZ7cIWSgbK%2FusNfEeiKB%2B7KZTAv14WOY%3D; cookie17=UUGrdlWh%2BFygrQ%3D%3D; sg=502; csg=3f166824; unb=2990207750; uc4=id4=0%40U2OcRhFnSO1ANdrxQInbrllz0mXy&nk4=0%40FbMocp0REDyJnA%2B62ByJu1noZqIwO3kU%2BWodvtYc7w%3D%3D; __cn_logon__=true; __cn_logon_id__=t_1493565210967_0515; ali_apache_tracktmp=c_w_signed=Y; _nk_=t_1493565210967_0515; _csrf_token=1590626868661; _is_show_loginId_change_block_=b2b-299020775014ef0_false; _show_force_unbind_div_=b2b-299020775014ef0_false; _show_sys_unbind_div_=b2b-299020775014ef0_false; _show_user_unbind_div_=b2b-299020775014ef0_false; __rn_alert__=false; ad_prefer="2020/05/28 08:48:17"; isg=BHBwvN9R2rwqN4a5HgnsfgKqQT7CuVQDXBEbgWrASUufJRTPEMqsktBXeSxF8wzb; l=eBgf9BXuQD29Fw3EBO5Zdurza77tXIOfGVNzaNbMiInca1yhLFpAvNQDtI0kbdtjitfvCexuEdARfRUk7rU38xZ7hHCuattzG296-',
            'referer': 'https://nbc520.1688.com/?tracelog=p4p&clickid=cfa6a9385812430b9d8dad0e185a039a&sessionid=c6d1a503dafce9892d4669d7cdcc7e21',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
            }



    def 爬取(self):
        # 获取搜索的商店列表的跳转链接
        titles = driver.find_elements_by_xpath('//*[@class="company-list-item"]/div[1]/div[2]/div[1]/a[1]')

        for html in titles:
            # link: https://pengchengdajiaju.1688.com/
            link = html.get_attribute('href')

            # 获取联系方式网页的链接
            contactinfo_link = self.get_联系方式html_link(link)

            # 获取_店铺名:
            self.name = html.get_attribute('title')

            # 获取电话号码->上传到数据库
            self.get_联系方式html_phone_post(contactinfo_link)


            

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>封装函数>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    def get_联系方式html_link(self,link):
        # 如果链接比较长
        if re.search(r"^https://dj.1688.com", link):
            link = re.search(r"2F(\w+?\.1688\.com)%3", link)[1]
            contactinfo_link = "https://" + link + r"/page/contactinfo.html"
        else:
            contactinfo_link = link + r"page/contactinfo.html"
        # print(contactinfo_link)
        return contactinfo_link


    # 获取电话号码
    def get_联系方式html_phone_post(self,contactinfo_link):
        # 获取联系方式网址源码
        req = requests.get(contactinfo_link, headers=self.headers)

        if(re.findall(r"移动电话", req.text)):
        	if re.findall(r"登录后可见", req.text):
        		print("需要登录"+contactinfo_link+"****************************************************")
        		return ""

        	phone = re.findall(r"移动电话.+?(1\d{10})[^0-9]", req.text, re.DOTALL)
        	if phone:
        		phone = phone[0]
        	else:
        		phone = ""
        		print(self.name+"##############################################################################################")

        	# 上传到数据库
        	self.post_shop_phone(self.name,phone)

        elif(re.findall(r"滑动一下马上回来", req.text)):
        	print("ip被限制, 要等一会儿")
        	sleep(11111111)

        else:
        	# print(req.text)
        	print("没有移动电话")
        	self.post_shop_phone(self.name,"")
        	# sleep(1212121)



    # 数据库: 上传shop电话号码
    def post_shop_phone(self,name,phone):
    	payload = 'shop_name={}&mobile={}&ori_type=1'.format(name,phone)
    	headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    	response = requests.post("http://112.124.127.143:8049/api/AliShop/PostAliShopUserOne",headers=headers, data = payload.encode('utf-8'))

    	print(phone + name + response.text)


# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>主函数>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
phone_1688 = 爬取1688_phone()
for index in range(2,102):
	phone_1688.爬取()
	driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
	sleep(2)
	driver.find_element_by_xpath("//a[text()='{}']".format(index)).click()
	sleep(2) 









