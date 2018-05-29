# -*- coding: utf-8 -*-
from searchOneDisk import search_by_disk
import pymysql


class search_nearby:
    def __init__(self,address=None):
        self.address = address
        self.disk = None
        self.nearbyAddress = []
        self.__run()

    def __run(self):
        conn = pymysql.connect(host='101.132.154.2', port=3306, user='housing', passwd='housing', db='housing',
                               charset='utf8')
        # print("Connected To DB")

        cursor = conn.cursor()
        sql = "select NewDiskName from NewDisk,DiskAddress where RoadLaneNo like %s and NewDisk.NewDiskID = DiskAddress.NewDiskID"
        cursor.execute(sql,self.address+'%')
        temp = cursor.fetchone()
        if(cursor.rownumber == 0):
            print("Disk Not Found!")
            self.nearbyAddress.append(self.address)
            return
        self.disk = temp[0]
        print("DiskName: ", self.disk)

        sbd = search_by_disk(self.disk,"")
        diskDetail = sbd.getElements()
        if diskDetail == None:
            self.nearbyAddress.append(self.address)
            return
        else:
            diskGPS = diskDetail[3]
            diskLong = diskDetail[6]
            diskLati = diskDetail[7]
            print("Disk Coordination: ",diskLong,diskLati)


        cursor = conn.cursor()
        sql = "select NewDisk.NewDiskID, NewDiskName,RoadLaneNo,Longtitude,Latitude,abs(Longtitude-%s) as longt ," \
              "abs(Latitude-%s) as latit, sqrt(pow(abs(Longtitude-%s),2)+pow(abs(Latitude-%s),2)) as distance " \
              "from NewDisk, DiskAddress " \
              "where NewDisk.NewDiskID = DiskAddress.NewDiskID " \
              "having longt < 180 and latit < 180 " \
              "order by distance asc"


        cursor.execute(sql, (diskLong,diskLati,diskLong,diskLati))
        temp = cursor.fetchall()
        self.nearbyAddress = []
        for count in range(1,cursor.rownumber):
            if(count > 5):
                break
            else:
                self.nearbyAddress.append(temp[count][2])
                # print(temp[count])
        print("NearbyDisks: " ,self.nearbyAddress)

        # for each in nearbyAddress:
        #     search = search_by_address()
        #     search.run([each, '10', '南', '103', '34', '2010'])

    def getAddress(self):
        return self.nearbyAddress


if __name__ ==   '__main__':
    sn = search_nearby("嘉松北路7222弄")