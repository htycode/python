#coding:utf-8
import requests,re,random
import uiautomator2 as u2
import urllib.request
from time import sleep
import os
from tkinter import Tk
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

# 删除文件管理/相册数据
def del_app数据():
    d.shell('pm clear com.cyanogenmod.filemanager') # 清除文件管理缓存
    d.shell('pm clear com.android.gallery')  # 清除相册缓存

def 删除相册图片():
    try:
        d.app_start("io.zhuliang.pipphotos","io.zhuliang.pipphotos.ui.main.MainActivity");
        d(text="微博").long_click(3)
        d(description="删除").click()
        d(text="确定").click()
        sleep(2)
        d.app_stop("io.zhuliang.pipphotos");
    except:pass
# =====================
# =========================================================================================



class 微博转发:

    def __init__(self):
        self.index = 0

    #获取微博图片和文案
    def get_content_img(self):
        删除相册图片()

        del_app数据()
        d.app_stop("com.weico.international");
        d.app_start("com.hengye.share","com.hengye.share.module.status.StatusFavoriteActivity");
        if bool(d(text="我收藏的微博").exists(3)) == True:
            pass

        d.swipe(444, 560, 444, 918);sleep(2)
        # 获得微博文案>>>>>>>>
        d.click(687, 203)
        sleep(2)
        self.content = d(resourceId="com.hengye.share:id/a10").get_text();
        print(self.content)

        # 点击分享_复制链接
        d(description="分享").click()
        d(text="复制链接").click();sleep(1)
        d.press("back")
        # 获取img_urls->下载图片
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

    # 转发到微博>>>>>>>>>>>>>>>>>>>>
    def to_微博(self):
        d.app_start("com.weico.international");sleep(4)

        d(resourceId="com.weico.international:id/home_frg_new").click();sleep(1)
        d(resourceId="com.weico.international:id/home_frg_new").click()
        # 点击_输入框
        d(text="说点什么…").set_text(self.content)
        sleep(1)
        d(resourceId="com.weico.international:id/compose_buttonCam").click()
        d(text="所有图片").click()
        d(text="微博").click()
        sleep(2)

        # 选图片
        index = self.index + 1
        for i in range(1, index):
            d.xpath(
                '//*[@resource-id="com.weico.international:id/act_pick_image"]/android.widget.FrameLayout[{}]/android.view.View[1]'.format(
                    index-i)).click()
        # d(resourceId="com.weico.international:id/act_photo_original_tips").click()  # 点击原图
        d(text="完成").click()
        sleep(2)
        d(resourceId="com.weico.international:id/send_ok").click();
        sleep(5)  # 点击发送

        d.app_start("com.hengye.share", "com.hengye.share.module.status.StatusFavoriteActivity");
        d(description="取消收藏").click()
        d.app_start("com.weico.international");

# 主函数====================================================================
'''
#悬疑片推荐##电影收藏夹##电影##电影推荐#
'''






#=======================================================================
# from PIL import Image
# for i in range(1,len(res)+1):
#     img = Image.open(r"D:\音_视_图\测试\{}.jpg".format(i))
#     print(img.size)
#     cropped = img.crop((0, 0, img.width, img.height-35)) # (left, upper, right, lower)
#     cropped.save(r"D:\音_视_图\测试\{}.jpg".format(i))

# from PIL import Image
# img = Image.open(r"D:\音_视_图\测试\1.jpg")
# print(img.size)


# def to_头条(index, content):
#     d.app_stop("com.netease.cloudmusic");
#     d.app_start("com.android.gallery", "com.android.camera.GalleryPicker");
#     sleep(2)
#     d.app_stop("com.android.gallery");
#     sleep(2)
#
#     d.app_start("com.ss.android.article.news", "com.ss.android.article.news.activity.MainActivity")
#     sleep(4)
#     d(text="发布").click()
#     d(text="发微头条").click()
#     d(text="分享新鲜事").set_text(content + 标签)
#     d.click(208, 510)
#     # d(resourceId="com.ss.android.article.news:id/bfi").click()
#     for i in range(2, index + 2):
#         d.xpath(
#             '//*[@resource-id="com.ss.android.article.news:id/cvw"]/android.widget.RelativeLayout[{}]/android.widget.RelativeLayout[1]'.format(
#                 i)).click()
#
#     d(text="完成").click()
#
