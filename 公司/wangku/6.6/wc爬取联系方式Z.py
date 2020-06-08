import requests
import re
from lxml import etree
from time import sleep
import json
import pymysql

header = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Cookie': 'shop_login_count=0; Hm_lvt_f160a8c6f9e75fcc0c45d38950c1b318=1591147328; _ga=GA1.2.1182363449.1591147328; _gid=GA1.2.655999740.1591147328; JSESSIONID=B3F8BD2209D4EE4C9DCA30776BFBFFD5; _pk_ref.1.0269=%5B%22%22%2C%22%22%2C1591147347%2C%22http%3A%2F%2Fshop.99114.com%2Flist%2Farea%2F101109_1%22%5D; _pk_ses.1.0269=*; _pk_ref.100000.0269=%5B%22%22%2C%22%22%2C1591147350%2C%22http%3A%2F%2Fshop.99114.com%2Flist%2Farea%2F101109_1%22%5D; _pk_ses.100000.0269=*; _pk_id.1.0269=2a1bea60d27176bd.1591147347.1.1591149052.1591147347.; _pk_ref.40118.0269=%5B%22%22%2C%22%22%2C1591149116%2C%22http%3A%2F%2Fshop.99114.com%2Flist%2Farea%2F101109_100%22%5D; _pk_id.40118.0269=3c91230bc1384b87.1591149116.1.1591149116.1591149116.; _pk_ses.40118.0269=*; Hm_lpvt_f160a8c6f9e75fcc0c45d38950c1b318=1591149116; _pk_id.100000.0269=5adc2534646ea406.1591147350.1.1591149121.1591147350.',
    'Host': 'shop.99114.com',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
}

# 插入公司名/公司链接/会员类型
def insert_shop(shop_name,shop_url,type):
    conn = pymysql.connect(host="rm-bp1278x3bc1a6ujve1o.mysql.rds.aliyuncs.com", user="test_0527",password="test_0527",database="test_0527",charset="utf8")
    # 得到一个可以执行SQL语句的光标对象
    cursor = conn.cursor()
    # 定义要执行的SQL语句
    sql = """insert into wangku (`shop_name`,`shop_url`,`type`) values('%s','%s','%s')"""%(shop_name,shop_url,type)
    # sql = "select * from wangku"
    # 执行SQL语句
    print(cursor.execute(sql))
    cursor.connection.commit()  # 执行commit操作，插入语句才能生效
    # 关闭光标对象
    cursor.close()
    # 关闭数据库连接
    conn.close()

#  上传到数据库
def post_shop_info(shop_name,手机,all_name,QQ,电话,邮箱):
    url = "http://112.124.127.143:8049/api/AliShop/PostAliShopUserOne"

    payload = 'shop_name={}&mobile={}&ori_type={}&contact_name={}&contact_qq={}&contact_tel={}&contact_email={}'.format(shop_name,手机,2,all_name,QQ,电话,邮箱)
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    res = requests.request("POST", url, headers=headers, data=payload.encode())
    # 操作失败->延时
    print(res.text) if json.loads(res.text)["msg"] == "操作成功" else sleep(10**10)

#  获取公司信息
def get_shop_info(shop_url):
    header = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        #'Cookie': 'shop_login_count=0; Hm_lvt_f160a8c6f9e75fcc0c45d38950c1b318=1591147328; _ga=GA1.2.1182363449.1591147328; _gid=GA1.2.655999740.1591147328; JSESSIONID=B3F8BD2209D4EE4C9DCA30776BFBFFD5; _pk_ref.1.0269=%5B%22%22%2C%22%22%2C1591147347%2C%22http%3A%2F%2Fshop.99114.com%2Flist%2Farea%2F101109_1%22%5D; _pk_id.1.0269=2a1bea60d27176bd.1591147347.1.1591149052.1591147347.; _pk_ref.40118.0269=%5B%22%22%2C%22%22%2C1591149116%2C%22http%3A%2F%2Fshop.99114.com%2Flist%2Farea%2F101109_100%22%5D; _pk_id.40118.0269=3c91230bc1384b87.1591149116.1.1591149116.1591149116.; _pk_ses.40115.0269=*; ydb_stat_c50,478,605=2fbb8c0e-86a4-47c6-abc2-76b85181c548; ydb_stat_sin50,478,605=; ydb_stat_vw50,478,605=%3A19974231%3A; ydb_stat_c50478605=df9cecb4-6629-4894-953a-547ae2ec62a7; ydb_stat_sin50478605=; ydb_stat_vw50478605=%3A19974231%3A; _pk_ref.100000.0269=%5B%22%22%2C%22%22%2C1591151676%2C%22http%3A%2F%2Fshop.99114.com%2Flist%2Farea%2F101109_1%22%5D; _pk_ses.100000.0269=*; _pk_id.40115.0269=99bbbb80590b45ef.1591151674.1.1591151693.1591151674.; Hm_lpvt_f160a8c6f9e75fcc0c45d38950c1b318=1591151693; ydb_ltime_50,478,605=1591151693907; ydb_ltime_50478605=1591151693968; _pk_id.100000.0269=5adc2534646ea406.1591147350.2.1591151695.1591151676.',
        'Host': 'shop.99114.com',
        'Upgrade-Insecure-Requests': '1',
        #'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
    }
    # 获取源码
    req = requests.get(shop_url,headers=header)
    all_name=""
    QQ=""
    电话=""
    邮箱=""
    传真=""
    type = ""
    手机 = ""

    try:
        selector = etree.HTML(req.text)
        type = "1"
        name = selector.xpath('//span[@class="name"]/text()')[0] if len(selector.xpath('//span[@class="name"]/text()')) != 0 else ""
        chenghu = "_" + re.sub("\s+", "", selector.xpath('//div[@class="contxt"]/p[1]/text()')[0]) if len(selector.xpath('//div[@class="contxt"]/p[1]/text()')) !=0 else ""
        all_name = name+chenghu


        手机 = selector.xpath('//span[@class="phoneNumber"]/text()')[0] if len(selector.xpath('//span[@class="phoneNumber"]/text()')) != 0 else ""

        QQ = re.search("\d+",re.sub("\s+","",selector.xpath('//a[@class="qq_img ml5 mt3"]/@title')[0]))[0] if selector.xpath('//a[@class="qq_img ml5 mt3"]/@title')[0] != '联系 ' else ""

        电话 = re.sub("\s+","",selector.xpath('//span[@class="addR telephoneShow"]/text()')[0]) if len(selector.xpath('//span[@class="addR telephoneShow"]/text()')) !=0 else ""
        if 电话 == "暂未填写": 电话 = ""

        邮箱 = re.sub("\s+","",selector.xpath('//div[@class="addIntroL"]/ul[1]/li[2]/span[2]/text()')[0]) if len(selector.xpath('//div[@class="addIntroL"]/ul[1]/li[2]/span[2]/text()')) != 0 else ""
        if 邮箱 == "暂未填写":邮箱 = ""

        传真 = re.sub("\s+","",selector.xpath('//div[@class="addIntroL"]/ul[1]/li[3]/span[2]/text()')[0]) if len(selector.xpath('//div[@class="addIntroL"]/ul[1]/li[3]/span[2]/text()')) != 0 else ""
        if 传真 == "暂未填写":传真 = ""
    except:
        res = re.findall('手  机：</span><span class="r">(\d{11})</span></p>', req.text)
        if len(res) != 0:
            all_name=""
            QQ=""
            电话=""
            邮箱=""
            传真=""
            type = "0"
            手机 = res[0]

    return {"all_name": all_name, "手机": 手机, "QQ": QQ, "电话": 电话, "邮箱": 邮箱, "传真": 传真,"type":type}




# 主函数>>>>>>>>>>>>>>>>>>>>>>>>>>
for lis_index in range(1,101):
    list_url = "http://shop.99114.com/list/pinyin/Z_{}".format(lis_index)
    req = requests.get(list_url,headers=header)
    html = req.text
    shops = re.findall(r'<a href="(http\:\/\/shop\.99114\.com/.+?)" target="_blank"><b>(.+?)</b></a>',html)
    #总长度
    print(len(shops))
    # for index,value in enumerate(shops[]):
    for index,value in enumerate(shops):
        #  获取->公司名/公司链接
        shop_url = value[0]+"/ch2";shop_name = value[1]
        # print(index,shop_url,shop_name)

        #  爬取公司信息
        shop_info = get_shop_info(shop_url)
        print(lis_index,index,shop_name, shop_url+list_url+">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>.")

        for i, s in shop_info.items():print(i + ":" + s)

        #  上传到数据库
        insert_shop(shop_name,shop_url, shop_info["type"])  #上传到我的数据库(店铺地址)
        post_shop_info(shop_name, shop_info["手机"], shop_info["all_name"], shop_info["QQ"], shop_info["电话"], shop_info["邮箱"])
    






# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>.

# # req = requests.get("http://shop.99114.com/list/pinyin/B_3",headers=header)
# # print(req.text)
# 911
# with open('911.txt', 'r', encoding='utf8') as f:
#     html =f.read()
#     print(html)
#     shops = re.findall(r'<a href="(http\:\/\/shop\.99114\.com/.+?)" target="_blank"><b>(.+?)</b></a>',html)
#     #总长度
#     print(len(shops))
#     for shop in shops:
#         #  获取->公司名/公司链接
#         shop_url = shop[0]
#         shop_name = shop[1]


# # 公司网页
# with open('公司网页.txt', 'r', encoding='utf8') as f:
#     html =f.read()
#     # print(html)
#     selector = etree.HTML(html)
#     name = selector.xpath('//h4[@class="y_b_qiye_ming"]/text()')[0];name = re.sub("\s","",name)
#     chenghu = selector.xpath('//h4[@class="y_b_qiye_ming"]/span/text()')[0];
#     chenghu = re.sub("\s+", "", chenghu)
#     all_name = name+"_"+chenghu
#     print(all_name)
#
#     手机 = selector.xpath('//a[@class="ypa_ipone"]/div/p[2]/text()')[0]
#     if re.search("\d+",手机):
#         手机 = re.search("\d+",手机)[0]
#     else:
#         手机 = ""
#
#     # return {"all_name": all_name, "手机": 手机, "QQ": QQ, "电话": 电话, "邮箱": 邮箱, "传真": 传真}
#
#
#
#
#     print(手机)