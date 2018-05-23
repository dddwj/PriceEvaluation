import pymysql
from searchOneDisk import search_by_disk

class search_plate:
    def __init__(self,address):
        self.address = address
        self.conn = pymysql.connect(host='101.132.154.2', port=3306, user='housing', passwd='housing', db='housing',
                               charset='utf8')



    def whichPlate(self):
        sod = search_by_disk(None,self.address)
        self.plate = sod.whichPlate()
        print(self.plate)
        if self.plate != None:
            return self.plate
        else:
            return "Error"

    def getPlateprice(self):
        cursor = self.conn.cursor()
        sql = "select HousingName,Plate from Property where Plate = %s"
        cursor.execute(sql, self.plate)
        temp = cursor.fetchall()
        DisksInPlate = []
        for each in temp:
            DisksInPlate.append(each[0])
        print(DisksInPlate)

        self.sum = 0
        self.count = 0
        for each in DisksInPlate:
            cursor = self.conn.cursor()
            # sql = "select avg,guapai_month from guapai_201706 where xiaoqu like %s union " \
            #       "select avg,guapai_month from guapai_201709 where xiaoqu like %s union " \
            #       "select avg,guapai_month from guapai_201708 where xiaoqu like %s union " \
            #       "select avg,guapai_month from guapai_201707 where xiaoqu like %s union " \
            sql=  "select avg,guapai_month from guapai_201710 where xiaoqu like %s " \
                  "order by guapai_month desc ;";
            cursor.execute(sql,(each+'%'))
            print(each)
            priceOneDisk = cursor.fetchmany(5)

            for index in range(0,cursor.rownumber):
                self.sum += priceOneDisk[index][0]
                self.count += 1
                print(priceOneDisk[index])
        price = self.sum / self.count
        return price

if __name__ == '__main__':
    sp = search_plate('西藏南路1739弄')
    plate = sp.whichPlate()
    price = sp.getPlateprice()
    print(price)

