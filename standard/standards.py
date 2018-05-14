# -*- coding: utf-8 -*-


from base import *
from collections import OrderedDict
from pyexcel_xls import get_data
from base import *


def read_file():
    xls_data = get_data(r"standard/JiJia_201711_12.xlsx")
    # print ("Get data type:", type(xls_data))
    sheet = xls_data['统计信息']
    notfound = 0
    count = 0
    ratio = 0
    missList = []
    #for each in range(1,len(sheet)):   正式测试的时候, 用这句话来替换
    for each in range(1, 50):
        rawList = sheet[each]
        list = [process_address(rawList[0]), rawList[3], "南", rawList[5], rawList[4], rawList[2]]

        standard_price = float(rawList[6])

        base0 = base(list)
        expected_price = base0.getPrice()

        if isinstance(expected_price, str):
            print(" ............", list)
            print(expected_price)
            notfound += 1
            missList.append(list)
            continue;
        else:
            error_ratio = float('%.2f' % (((expected_price - standard_price) / standard_price) * 100))
            print("*****************************")
            print("expected: ", expected_price, "; standard: ", standard_price, "; error ratio: ", error_ratio, ' %');
            print("*****************************\n")
            count += 1
            ratio += abs(error_ratio)
    # print("*********************")
    # print("Missed:", notfound, "; Get:", count)
    # print("Average Ratio: ", ratio / count)

    file = open("standard/missList.txt", 'w')  # 'a'意思是追加，这样在加了之后就不会覆盖掉源文件中的内容，如果是w则会覆盖。
    file.write("Missed: %s;" %notfound )
    file.write("Get: %s; \n " %count)
    file.write("Average Ratio: %.2f %%\n" % (float(ratio)/int(count)) )
    file.write("****************************\n")
    file.write("********Missed List*********\n")
    for each in missList:
        file.write(str(each))
        file.write("\n")
    file.close()


def process_address(raw):
    start = raw.index('区') + 1
    if raw.find('镇') != -1:
        start = raw.index('镇') + 1

    nong = raw.find('弄') + 1
    hao = raw.find('号') + 1
    if nong > start:
        end = nong
    elif hao > start:
        end = hao
    elif nong > start and hao > start:
        end = min(nong, hao)
    else:
        return raw[start:]
    return raw[start:end]


if __name__ == '__main__':
    read_file()