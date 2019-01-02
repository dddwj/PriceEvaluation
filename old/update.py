# -*- coding: utf-8 -*-
# 给数据库中所有NewDiskID的房源配上小区名(NewDiskName)
import pymysql

conn = pymysql.connect(host='101.132.154.2', port=3306, user='housing', passwd='housing', db='housing', charset='utf8')
for NewDiskID in range(0,22488):
    cursor = conn.cursor()
    sql = "select BasePriceApril.NewDiskID,NewDisk.NewDiskName,BasePrice from BasePriceApril, NewDisk " \
          "where NewDisk.NewDiskID = %s and BasePriceApril.NewDiskID = NewDisk.NewDiskID;"
    cursor.execute(sql,NewDiskID);
    result = cursor.fetchone()
    if (result == None):
        continue
        # BasePrice = None
        # NewDiskName = None
    else:
        BasePrice = result[2]
        NewDiskName = result[1]
    cursor2 = conn.cursor()
    sql2 = "insert into NewBasePrice (NewDiskID,NewDiskName,BasePrice) values(%s,%s,%s)"
    cursor2.execute(sql2, (NewDiskID,NewDiskName,BasePrice))
    conn.commit()
    print(NewDiskID,", ",NewDiskName,", ",BasePrice)
conn.close()

