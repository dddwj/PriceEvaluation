# -*- coding: utf-8 -*-
import pymysql

class search_by_disk:
    def __init__(self, diskName, address):
        self.HousingName = diskName
        self.address = address
        self.conn = pymysql.connect(host='101.132.154.2', port=3306, user='housing', passwd='housing', db='housing',charset='utf8')
        # self.conn = pymysql.connect(host='localhost', port=3306, user='housing', passwd='housing', db='housing',charset='utf8')

    def __getPlate(self):
        sql = "select PropertyID, plate,HousingName from Property where HousingName like %s;";
        cursor = self.conn.cursor()
        cursor.execute(sql, (self.HousingName + '%'))
        temp = cursor.fetchone()
        if cursor.rownumber == 1 :
            self.Plate = temp[1]
            self.HousingName = temp[2]
            self.PropertyID = temp[0]
        else:
            self.Plate = None
            self.PropertyID = None
            print("No Plate for %s" % self.HousingName)
            self.moveOn = False

    def __getCoordinates(self):
        sql = "select NewDiskID, Coordinates,Longtitude,Latitude from NewDisk where PropertyID = %s;";
        cursor = self.conn.cursor()
        cursor.execute(sql, self.PropertyID)
        temp = cursor.fetchone()
        if cursor.rownumber == 1 :
            self.NewDiskID = temp[0]
            self.Coordinates = temp[1]
            self.Long = temp[2]
            self.Lati = temp[3]
        else:
            self.NewDiskID = None
            self.Coordinates = None
            print("No Coordinates for %s" % self.PropertyID)
            self.moveOn = False

    def __getAddress(self):
        sql = "select RoadLaneNo from DiskAddress where NewDiskID = %s;";
        cursor = self.conn.cursor()
        cursor.execute(sql, self.NewDiskID)
        temp = cursor.fetchone()
        if cursor.rownumber == 1:
            self.RoadLaneNo = temp[0]
        else:
            self.RoadLaneNo = None
            print("No Address for %s" % self.NewDiskID)
            self.moveOn = False

    def getElements(self):
        self.moveOn = True
        print("Gathering information.... [in searchOneDisk.getElements]")


        self.__getPlate()
        if not self.moveOn:
            self.conn.close()
            print("Cannot get plate!")
            return

        self.__getCoordinates()
        if not self.moveOn:
            self.conn.close()
            print("Cannot get coordinates!")
            return

        self.__getAddress()
        if not self.moveOn:
            self.conn.close()
            print("Cannot get Address!")
            return

        self.conn.close()
        return [self.HousingName, self.Plate, self.RoadLaneNo, self.Coordinates, self.PropertyID, self.NewDiskID,self.Long,self.Lati]


    def whichPlate(self):
        cursor = self.conn.cursor()
        sql = "select NewDisk.NewDiskID,RoadLaneNo,NewDiskName " \
              "from DiskAddress,NewDisk " \
              "where RoadLaneNo like %s and DiskAddress.NewDiskID = NewDisk.NewDiskID;"
        cursor.execute(sql,self.address+'%')
        temp = cursor.fetchone()
        if  cursor.rownumber == 1 :
            NewDiskID = temp[0]
            address = temp[1]
            Disk = temp[2]

            cursor = self.conn.cursor()
            sql = "select Plate from Property where Property.HousingName like %s"
            cursor.execute(sql, Disk+'%')
            temp = cursor.fetchone()
            if cursor.rownumber == 1 :
                return temp[0]
                # return [Disk,address,NewDiskID]
            else:
                print("Cannot Find Plate!")
                return None
        else:
            print("Cannot Find Disk!")
            return None


if __name__ == '__main__':
    # search = search_by_disk("华理苑",None)
    # print(search.getElements())
    search2 = search_by_disk(None,"西藏南路1739弄")
    print(search2.whichPlate())