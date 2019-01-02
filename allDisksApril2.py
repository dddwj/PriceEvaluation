# -*- coding: utf-8 -*-
# 计算四月份的所有小区的基价。
import pymysql
from searchNearby import search_nearby

def getMarchBase(NewDiskID):
    sql7 = "select BasePrice from BasePriceMarch_s where NewDiskID = %s;"
    cursor7 = conn.cursor()
    cursor7.execute(sql7, NewDiskID)
    if (cursor7.rowcount != 0):
        result7 = cursor7.fetchone()
        basePrice = result7[0]
        print("*********************************")
        print("Got BasePrice from March...", basePrice)
    else:
        basePrice = 0
        print("*********************************")
        print("No BasePrice from March!", basePrice)
    return basePrice


conn = pymysql.connect(host='101.132.154.2', port=3306, user='housing', passwd='housing', db='housing', charset='utf8')
# conn = pymysql.connect(host='localhost', port=3306, user='housing', passwd='housing', db='housing',charset='utf8')

visited = []
for NewDiskID in range(1,22488):
    # 若不是公寓，则不处理
    sql0 = "select NewDiskType,MainNewDiskType from NewDisk where NewDiskID = %s;"
    cursor0 = conn.cursor()
    cursor0.execute(sql0, NewDiskID)
    temp0 = []
    temp0 = cursor0.fetchone()
    if temp0 == None:
        print(NewDiskID, "Cannot find such disk from NewDisk!")
        continue
    if temp0[1] != '公寓' and temp0[0] != '公寓':
        print(NewDiskID, "Not a 公寓!")
        continue


    # 查看有没有这个NewDiskID, 若有，把它们所有地址加到待检索列表中。
    sql = "select RoadLaneNo from DiskAddress where NewDiskID = %s;"
    cursor = conn.cursor()
    cursor.execute(sql, NewDiskID)
    temp = cursor.fetchall()
    row = cursor.rowcount
    if row == 0:
        continue
    inquiryList = []
    for aRecord in temp:
        oneRecord = str(aRecord[0])
        if(oneRecord.__contains__('弄') and (oneRecord.__contains__('号') or oneRecord.__contains__('幢'))):
            oneRecord = oneRecord[0:oneRecord.index('弄')+1]
        if(inquiryList.__contains__(oneRecord)):
            continue
        inquiryList.append(oneRecord)
    print("【NewDiskID: ", NewDiskID," 】", inquiryList)

    # 节约开销，房源不足五套时，在inquiryList中的地址只检索附近的房源一次。
    if (visited.__contains__(NewDiskID)):
        print("Visited, Continue!")
        continue
    visited.append(NewDiskID)

    # 开始搜索同地址房源 及 附近房源
    allAveragePrice = []
    visitedanAddress = False        # 节约开销，保证遍历InquiryList中所有房源时，只搜索附近房源一次
    for anAddress in inquiryList:
        cursor2 = conn.cursor()
        sql2 = "select avg,guapai_month from guapai_201803 where address like %s union " \
               "select avg,guapai_month from guapai_201802 where address like %s union " \
               "select avg,guapai_month from guapai_201801 where address like %s union " \
               "select avg,guapai_month from guapai_201712 where address like %s union " \
               "select avg,guapai_month from guapai_201711 where address like %s union " \
               "select avg,guapai_month from guapai_201710 where address like %s union " \
               "select avg,guapai_month from guapai_201709 where address like %s " \
               "order by guapai_month DESC " \
               "limit 0,10"
        cursor2.execute(sql2,(anAddress+'%',anAddress+'%',anAddress+'%',anAddress+'%',anAddress+'%',anAddress+'%',anAddress+'%'))
        result2 = cursor2.fetchall()
        row2 = cursor2.rowcount
        if (row2 != 0):
            for each in result2:
                allAveragePrice.append(each[0])

        if ( row2 < 5 and visitedanAddress == False ):
            print(row2,"...less than 5 resources...searching nearby...")
            sn = search_nearby(anAddress)
            nearbyAddress = sn.getAddress()
            for aNearAddress in nearbyAddress:
                cursor3 = conn.cursor()
                cursor3.execute(sql2, (
                aNearAddress + '%', aNearAddress + '%', aNearAddress + '%', aNearAddress + '%', aNearAddress + '%', aNearAddress + '%',
                aNearAddress + '%'))
                result3 = cursor3.fetchall()
                row3 = cursor3.rowcount
                print(aNearAddress,row3)
                if (row3 != 0):
                    for each in result3:
                        allAveragePrice.append(each[0])
        visitedanAddress = True

    print("**********************************")
    print(allAveragePrice)
    print("Resources Count:",allAveragePrice.__len__())

    MarchBase = getMarchBase(NewDiskID)

    #  计算四月基价

    if(allAveragePrice.__len__() == 0):
        print("AprilBasePrice: Zero resource!")
        continue
    else:
        if(MarchBase != 0):
            allAveragePrice.append(MarchBase)
            allAveragePrice.append(MarchBase)
        count = 0
        sum = 0
        for each in allAveragePrice:
            sum += each
            count += 1
        basePrice = float(sum/count)
        print("AprilBasePrice:",basePrice)



    #  若涨幅超过20%，那么不采用，仍取3月基价
    if(MarchBase != 0):
        rate = (basePrice - MarchBase) / MarchBase * 100
        if (abs(rate) > 20):
            basePrice = MarchBase
            rate = 0
        else:
            pass
    else:
        rate = 99
    print("MarchBase:",MarchBase, "AprilBase:", basePrice,"Rate:", rate)


    cursor4 = conn.cursor()
    sql4 = "UPDATE BasePriceApril SET BasePrice = %s , Rate = %s WHERE NewDiskID = %s;"
    cursor4.execute(sql4,(basePrice, rate, NewDiskID))
    conn.commit()
    print("ID ", NewDiskID, "\n\n")

conn.close()



