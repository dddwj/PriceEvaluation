# -*- coding: utf-8 -*-
import os,sys
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,parentdir)
from base import *
import time



element = sys.argv[1]
print("********************************")
print("Got Elements in Python!",element)
# print(element)
# element = "西藏南路1739弄,10,南,103,34,2010"
eles = element.split(',')
base0 = base(eles)
# base0.getPrice()


filename = '/Users/dddwj/PycharmProjects/PriceEvaluation/php/php_result.txt'

with open(filename,'w') as fileobject: #使用‘w’来提醒python用写入的方式打开
    fileobject.write(time.strftime("%Y-%m-%d %X", time.localtime()))
    fileobject.write("\nGot Elements in Python! %s" % str(element))
    fileobject.write("\nSimilar Houses: %s" % base0.get5Houses())
    fileobject.write("\nPrice = %s" % str(base0.price))
