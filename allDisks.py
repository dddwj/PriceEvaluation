# -*- coding: utf-8 -*-
import pymysql

from searchNearby import search_nearby

# conn = pymysql.connect(host='101.132.154.2', port=3306, user='housing', passwd='housing', db='housing', charset='utf8')
conn = pymysql.connect(host='localhost', port=3306, user='housing', passwd='housing', db='housing',charset='utf8')
cursor = conn.cursor()

# try:
#     except Exception as e:
#     print(e)
#
# finally:
#     conn.close()

visited = []
for NewDiskID in range(192,193):
    sql = "select RoadLaneNo from DiskAddress where NewDiskID = %s;"
    cursor.execute(sql,NewDiskID)
    temp = cursor.fetchall()
    row = cursor.rowcount
    if row == 0:
        continue
    inquiryList = []
    for aRecord in temp:
        inquiryList.append(aRecord[0])
    # inquiryList = ["白杨路360弄"]
    print("【NewDiskID: ",NewDiskID,"】 here",inquiryList)


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

        if (visited.__contains__(NewDiskID)):
            print("Visited, Continue!")
            continue
        visited.append(NewDiskID)

        if ( row2 < 5 ):
            print("...less than 5 resources...searching nearby...")
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



