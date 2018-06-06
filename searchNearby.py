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
        # conn = pymysql.connect(host='localhost', port=3306, user='housing', passwd='housing', db='housing',
        #                        charset='utf8')
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
        if (str(self.disk).endswith('*')):
            self.disk = self.disk[0:len(self.disk) - 1]
        if (str(self.disk).endswith('期')):
            self.disk = str(self.disk)[0:str(self.disk).index('期') - 1]
        if (str(self.disk).__contains__('（')):
            self.disk = str(self.disk)[0:str(self.disk).index('（') - 1]
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
              "having longt < 150 and latit < 150 " \
              "order by distance asc"


        cursor.execute(sql, (diskLong,diskLati,diskLong,diskLati))
        temp = cursor.fetchall()
        self.nearbyAddress = []
        diskcount = 0
        for count in range(1,cursor.rownumber):
            if(diskcount > 4):
                break
            else:
                onedisk = str(temp[count][2])
                if(onedisk.__contains__('镇')):
                    onedisk = onedisk[onedisk.index('镇')+1:]
                if(onedisk.__contains__('弄') and onedisk.__contains__('号')):
                    onedisk = onedisk[0:onedisk.index('弄')+1]
                if(onedisk.endswith('期')):
                    onedisk = onedisk[0:onedisk.index('期')-1]
                if(self.nearbyAddress.__contains__(onedisk)):
                    continue;
                else:
                    self.nearbyAddress.append(onedisk)
                    diskcount += 1
                # print(temp[count])
        print("NearbyDisks: " ,self.nearbyAddress)

        # for each in nearbyAddress:
        #     search = search_by_address()
        #     search.run([each, '10', '南', '103', '34', '2010'])

    def getAddress(self):
        return self.nearbyAddress


if __name__ ==   '__main__':
    sn = search_nearby("嘉松北路7222弄")