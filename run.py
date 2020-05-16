from 微博_网易云 import 微博转发
from time import *
import random

# 微博转发到网易云
while (True):
    微博 = 微博转发()
    微博.get_content_img()
    # 微博.to_微博()
    # sleep(5)
    微博.to_网易云()
    sleep(random.randint(20 * 60, 37 * 60))