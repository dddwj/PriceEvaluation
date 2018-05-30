# -*- coding: utf-8 -*-

from collections import OrderedDict
from pyexcel_xls import get_data
from pyexcel_xls import save_data
from base import *
import matplotlib.pyplot as plt
import re

def read_file():
    # xls_data = get_data(r"JiJia_201711_12.xlsx")
    xls_data = get_data(r"楼盘基价_201801.xlsx")
    # print ("Get data type:", type(xls_data))
    # sheet = xls_data['统计信息']
    sheet = xls_data['1月下']
    notfound = 0
    count = 0
    ratio = 0
    missList = []
    errorlist = []
    output = OrderedDict()
    sheet_1 = []
    row_1_data = ["房源信息","分词后", "标准价格", "计算价格", "误差","房源1(id,avg,address,floor,direction,square,height,built_year)","房源2","房源3","房源4","房源5","is住宅"]  # 每一行的数据
    sheet_1.append(row_1_data)


    # for each in range(1,len(sheet)):   正式测试的时候, 用这句话来替换
    for each in range(1,len(sheet)):
        rawList = sheet[each]
        print(rawList)
        if (rawList[1] != '住宅' ):
            isZhuzhai = 0
        else:
            isZhuzhai = 1

        list = [process_address(rawList[0]), rawList[3], "南", rawList[5], rawList[4], rawList[2]]
        # print(list) 已经在searchMain中print了
        standard_price = float(rawList[6])

        base0 = base(list)
        expected_price = base0.getPrice()
        SearchInformation = base0.getSearchInformation()

        if isinstance(expected_price, str):
            print(" ............", list)
            print(expected_price)
            notfound += 1
            missList.append([rawList,list,standard_price,isZhuzhai])
            continue;
        else:
            error_ratio = float('%.2f' % (((expected_price - standard_price) / standard_price) * 100))
            count += 1
            errorlist.append(abs(error_ratio))
            ratio += abs(error_ratio)

            print("*****************************")
            print("expected: ", expected_price, "; standard: ", standard_price, "; error ratio: ", error_ratio, ' %');
            print("*****************************\n")
            sheet_1.append([str(rawList),str(list),str(standard_price),str(expected_price),str(abs(error_ratio)),str(SearchInformation[0]),str(SearchInformation[1]),str(SearchInformation[2]),str(SearchInformation[3]),str(SearchInformation[4]),isZhuzhai])
    # print("*********************")
    # print("Missed:", notfound, "; Get:", count)
    # print("Average Ratio: ", ratio / count)

    # (丢失)结果写入txt
    file = open("missList.txt", 'w')  # 'a'意思是追加，这样在加了之后就不会覆盖掉源文件中的内容，如果是w则会覆盖。
    file.write("Missed: %s; " %notfound )
    file.write("Get: %s;\n" %count)
    file.write("Average Ratio: %.2f %%\n" % (float(ratio)/int(count)) )
    file.write("****************************\n")
    # file.write("********Missed List*********\n")
    # for each in missList:
    #     file.write(str(each))
    #     file.write("\n")
    file.close()

    # 成功&失败结果写入xls
    for each in missList:
        sheet_1.append([str(each[0]),str(each[1]),str(each[2]),"No Result",None,None,None,None,None,None,isZhuzhai])
    output.update({"Sheet1": sheet_1})  # 添加sheet表
    save_data("Result.xls", output)

    # 结果用图来呈现
    # draw_plot(errorlist)


def draw_plot(errorlist):
    x = range(0,len(errorlist))
    y = errorlist
    plt.figure()
    plt.plot(x, y)
    plt.show()


def process_address(raw):
    start = raw.index('区') + 1
    if raw.find("街道") != -1:
        start = raw.index("街道") + 2

    result = re.search(r'(.*)村[0-9]', raw[start:])
    if         result != None:
        string = result[0]
        return string[0:len(string) - 1]
    else:
        if raw.find('镇') != -1 and raw.index('镇') > 4 :
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
