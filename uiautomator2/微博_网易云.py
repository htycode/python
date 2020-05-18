#coding:utf-8
import requests,re,random
import uiautomator2 as u2
import urllib.request
from time import sleep
import os
from tkinter import Tk
import sys
import ast

d = u2.connect("127.0.0.1:5555")
d.implicitly_wait(9)  # 隐式等待9s


# 获取剪切板内容
def gettext():
    r = Tk()
    t = r.clipboard_get()
    return (t)

# 删除文件夹下所有文件
def del_file(path):
    for i in os.listdir(path):
        path_file = os.path.join(path, i) #取文件绝对路径
        if os.path.isfile(path_file):
            os.remove(path_file)
        else:
            del_file(path_file)

# 类=========================================================================================
class 微博转发:
    def __init__(self):
        self.index = 0

        # 初始化
        d.app_stop_all()
        del_file(r"C:\Users\hty\Documents\雷电模拟器\Pictures\微博")   #删除下载的图片
        d.shell('pm clear com.cyanogenmod.filemanager')  # 清除文件管理缓存
        d.shell('pm clear com.android.gallery')          # 清除相册缓存



    #获取微博图片和文案
    def get_content_img(self):
        d.app_start("com.hengye.share","com.hengye.share.module.status.StatusFavoriteActivity");

        if bool(d(text="我收藏的微博").exists(3)) == True:
            d.swipe(444, 560, 444, 918);sleep(2)    #下拉刷新
        else: sys.exit()

        # 获得微博文案>>>>>>>>
        d.click(687, 203);sleep(2)
        self.content = d(resourceId="com.hengye.share:id/a10").get_text()
        print("文案:\n"+self.content)

        # 点击分享->复制链接
        d(description="更多").click()
        d(text="分享").click()
        d(text="复制链接").click();sleep(1)
        d.press("back")

        # 获取img_urls链接->下载图片
        url = gettext() + "?jumpfrom=weibocom" # 获取剪切板内容
        print(url)
        headers = {"user-agent": "Mozilla/5.0 (Linux; Android 4.4.2; Nexus 4 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.114 Mobile Safari/537.36"}
        r = requests.get(url, headers=headers)
        pattern = re.compile(r'\"large\":[\d\D]+?url\": \"(.+?)\"')
        res = pattern.findall(r.text)
        res.reverse()
        self.index=len(res) #网易云选择图片个数用
        print("一共{}个图片\n".format(len(res)), res)

        # 下载imgs
        i=0
        for item in res:
            urllib.request.urlretrieve(item, r"C:\Users\hty\Documents\雷电模拟器\Pictures\微博\{}.jpg".format(i))
            i=i+1

        d.app_start("com.android.gallery");
        sleep(2)
        d.app_stop("com.android.gallery");

    # 转发到网易云>>>>>>>>>>>>>>>>>>

    def to_网易云(self):
        # d.app_stop("com.netease.cloudmusic");
        # 启动网易云音乐App
        d.app_start("com.netease.cloudmusic","com.netease.cloudmusic.activity.MainActivity");sleep(5)
        # 点击_我的音乐>点击歌单>点击分享
        d(description="我的音乐").click()  #"我的"
        sleep(2)
        d(text="失眠疗养院").click();sleep(7)
        d(resourceId="com.netease.cloudmusic:id/ri").click()  # 点击分享
        # d(resourceId="com.netease.cloudmusic:id/ahb").click()  # 点击分享
        d(text="云音乐动态").click()
        # 点击_输入框
        d.clear_text()
        d(text="一起聊聊吧~").set_text(self.content)
        # 点击_+图片
        d.xpath('//android.support.v7.widget.RecyclerView/android.widget.ImageView[1]').click()
        d(text="全部照片").click()
        d(text="微博").click();sleep(1)
        # 循环点击图片
        try:
            for i in range(1, self.index + 1):
                ele = d.xpath('//*[@resource-id="com.netease.cloudmusic:id/ps"]/android.widget.RelativeLayout[{}]/android.widget.RelativeLayout[1]/android.widget.TextView[1]'.format(i))
                ele.click()
        except:pass

        d.xpath('//android.support.v7.widget.LinearLayoutCompat').click() #点击完成
        d(text="分享").click()

        d.app_start("com.hengye.share","com.hengye.share.module.status.StatusFavoriteActivity");
        d(description="取消收藏").click()
        d.app_start("com.netease.cloudmusic")
