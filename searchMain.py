# -*- coding: UTF-8 -*-

import pymysql
from searchNearby import *

class search_by_address():

    def getValue(self, list):
        self.Elements = list
        print ("Inquiry List:",self.Elements)

    def run(self, list):
        self.getValue(list)
        conn = pymysql.connect(host='101.132.154.2',port=3306,user='housing',passwd='housing',db='housing',charset='utf8')
        # print("Connected To Database!")

        cursor = conn.cursor()
        sql = "select id,address,square,avg,floor,total,height,direction,built_year,guapai_month,abs(square-%s) as result from guapai_201707 where address like %s having result<20.0 union " \
              "select id,address,square,avg,floor,total,height,direction,built_year,guapai_month,abs(square-%s) as result from guapai_201708 where address like %s having result<20.0 union " \
              "select id,address,square,avg,floor,total,height,direction,built_year,guapai_month,abs(square-%s) as result from guapai_201709 where address like %s having result<20.0 union " \
              "select id,address,square,avg,floor,total,height,direction,built_year,guapai_month,abs(square-%s) as result from guapai_201710 where address like %s having result<20.0 union " \
              "select id,address,square,avg,floor,total,height,direction,built_year,guapai_month,abs(square-%s) as result from guapai_201711 where address like %s having result<20.0 union " \
              "select id,address,square,avg,floor,total,height,direction,built_year,guapai_month,abs(square-%s) as result from guapai_201712 where address like %s having result<20.0 " \
              "order by result asc, " \
              "guapai_month desc, "  \
              "abs(built_year-%s) asc ;";

        address = self.Elements[0]
        square = self.Elements[3]
        floor = self.Elements[1]
        direction = self.Elements[2]
        built_year = self.Elements[5]
        # cursor.execute(sql,(square, address+'%',built_year));
        cursor.execute(sql,(square, address+'%',square, address+'%',square, address+'%',square, address+'%',square, address+'%',square, address+'%',built_year))
        self.fangYuan = []
        temp = cursor.fetchmany(10)
        for each in temp:
            self.fangYuan.append(each)

        if self.fangYuan.__len__() < 5 :
            print("Result Only Found:",self.fangYuan.__len__())
            print("Finding Nearby Disks...")
            sn = search_nearby(address)
            for nearbyAddress in sn.getAddress():
                cursor.execute(sql,(square, nearbyAddress+'%',square, nearbyAddress+'%',square, nearbyAddress+'%',square, nearbyAddress+'%',square, nearbyAddress+'%',square, nearbyAddress+'%',built_year))
                # cursor.execute(sql,(square, nearbyAddress+'%',built_year))
                # temp = cursor.fetchall()
                temp = cursor.fetchmany(2)
                for each in temp:
                    print("(Nearby):",each)
                    self.fangYuan.append(each)
                    if(self.fangYuan.__len__() > 6):
                        break

            if self.fangYuan.__len__() == 0:
                conn.close()
                cursor.close()
                print("No Result!")
                return "No Result!"
            else:
                print("fangYuan Ready for Modification...\n" ,self.fangYuan)

        print("********Similar Houses********")
        sum = 0
        count = 0
        for each in self.fangYuan:
            print(each)
            #
            # modify each !!!
            # take average within modified price
            # return average price
            #
            sum += each[3]
            count += 1
            if count >= 6:
                break
        avg = float( sum / count )

        conn.close()
        cursor.close()
        print("********End of Modification********")
        print("Average Price:", avg)
        return avg


if __name__ == '__main__':
    search = search_by_address()
    search.run(['梅陇路华理苑', 2, '南', 103, 6, 2008])
