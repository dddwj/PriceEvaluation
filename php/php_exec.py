 # -*- coding: utf-8 -*-
import sys
# from modification import modification
# from searchByAddress import search_by_address
import os,sys
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,parentdir)
from base import *

element = sys.argv[1]
# element = "西藏南路1739弄,10,南,103,34,2010"
eles = element.split(',')
base0 = base(eles)
base0.getPrice()


