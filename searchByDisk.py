# -*- coding: utf-8 -*-
import pymysql

class search_by_disk:
    def __init__(self, diskName):
        self.HousingName = diskName
    # def __init__(self):
    #     self.HousingName = "耀江花园"

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
        sql = "select NewDiskID, Coordinates from NewDisk where PropertyID = %s;";
        cursor = self.conn.cursor()
        cursor.execute(sql, self.PropertyID)
        temp = cursor.fetchone()
        if cursor.rownumber == 1 :
            self.NewDiskID = temp[0]
            self.Coordinates = temp[1]
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
        self.conn = pymysql.connect(host='101.132.154.2', port=3306, user='housing', passwd='housing', db='housing',
                               charset='utf8')
        print("Connected To DB")

        if self.moveOn:
            self.__getPlate()
        if self.moveOn:
            self.__getCoordinates()
        if self.moveOn:
            self.__getAddress()
        if not(self.moveOn) :
            print ("ERROR!")

        self.conn.close()
        return [self.HousingName, self.Plate, self.RoadLaneNo, self.Coordinates, self.PropertyID, self.NewDiskID]

if __name__ == '__main__':
    search = search_by_disk("华理苑")
    print(search.getElements())
