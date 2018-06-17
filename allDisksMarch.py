# -*- coding: utf-8 -*-
# 计算三月份的所有小区的基价，利用同地址房源检索+附近小区房源检索来计算。
import pymysql

from searchNearby import search_nearby

conn = pymysql.connect(host='101.132.154.2', port=3306, user='housing', passwd='housing', db='housing', charset='utf8')
# conn = pymysql.connect(host='localhost', port=3306, user='housing', passwd='housing', db='housing',charset='utf8')


# try:
#     except Exception as e:
#     print(e)
#
# finally:
#     conn.close()

visited = []
for NewDiskID in range(17640,17641):
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
    # inquiryList = ["白杨路360弄"]
    print("【NewDiskID: ", NewDiskID, "】 here", inquiryList)

    # 若不是公寓，则不处理
    sql0 = "select NewDiskType,MainNewDiskType from NewDisk where NewDiskID = %s;"
    cursor0 = conn.cursor()
    cursor0.execute(sql0,NewDiskID)
    temp0 = []
    temp0 = cursor0.fetchone()
    if temp0 == None:
        print("Cannot find such disk from NewDisk!\n\n\n\n")
        continue
        # print(temp0[0],temp0[1])
    if temp0[1] != '公寓' and temp0[0] != '公寓':
        print(NewDiskID,"Not a 公寓!\n\n\n\n")
        continue

    # 节约开销，房源不足五套时，在inquiryList中的地址只检索附近的房源一次。
    if (visited.__contains__(NewDiskID)):
        print("Visited, Continue!")
        continue
    visited.append(NewDiskID)

    # 开始搜索同地址房源 及 附近房源
    allAveragePrice = []
    for anAddress in inquiryList:
        cursor2 = conn.cursor()
        sql2 = "select avg,guapai_month from guapai_201712 where address like %s union " \
               "select avg,guapai_month from guapai_201711 where address like %s union " \
               "select avg,guapai_month from guapai_201710 where address like %s union " \
               "select avg,guapai_month from guapai_201709 where address like %s union " \
               "select avg,guapai_month from guapai_201708 where address like %s union " \
               "select avg,guapai_month from guapai_201707 where address like %s union " \
               "select avg,guapai_month from guapai_201706 where address like %s union " \
               "select avg,guapai_month from guapai_201705 where address like %s " \
               "order by guapai_month desc " \
               "limit 0,15"
        cursor2.execute(sql2,(anAddress+'%',anAddress+'%',anAddress+'%',anAddress+'%',anAddress+'%',anAddress+'%',anAddress+'%',anAddress+'%'))
        result2 = cursor2.fetchall()
        row2 = cursor2.rowcount
        if (row2 != 0):
            for each in result2:
                allAveragePrice.append(each[0])


        if ( row2 < 5 ):
            print(row2,"...less than 5 resources...searching nearby...")
            sn = search_nearby(anAddress)
            nearbyAddress = sn.getAddress()
            for aNearAddress in nearbyAddress:
                cursor3 = conn.cursor()
                cursor3.execute(sql2, (
                aNearAddress + '%', aNearAddress + '%', aNearAddress + '%', aNearAddress + '%', aNearAddress + '%', aNearAddress + '%',
                aNearAddress + '%', aNearAddress + '%'))
                result3 = cursor3.fetchall()
                row3 = cursor3.rowcount
                print(aNearAddress,row3)
                if (row3 != 0):
                    for each in result3:
                        allAveragePrice.append(each[0])

    print("**********************************")
    print(allAveragePrice)

    count = 0
    sum = 0
    for each in allAveragePrice:
        sum += each
        count += 1
    if( count != 0):
        basePrice = float(sum/count)
        print("*********************************")
        print("basePrice:",basePrice)
        print("\n\n\n")
    else:
        basePrice = None
        print("*********************************")
        print("basePrice:",basePrice)
        print("ERROR: Zero resource!")
        print("\n\n\n")


    cursor4 = conn.cursor()
    sql4 = "insert into BasePrice (NewDiskID,BasePrice) values(%s,%s)"
    cursor4.execute(sql4,(NewDiskID,basePrice))
    conn.commit()

conn.close()



