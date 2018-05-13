 # -*- coding: utf-8 -*-
import sys
from modification import modification
from searchByAddress import search_by_address

element = sys.argv[1]
# element = "西藏南路1739弄,10,南,103"
eles = element.split(',')
list = eles
list.append(31)



search = search_by_address()
avg_price = search.run(list)
modi = modification()
expected_price = modi.run(avg_price, list)
price = float('%.4f' % expected_price)
print ("预估价格：",price)

