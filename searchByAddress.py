# -*- coding: UTF-8 -*-

import pymysql

class search_by_address():


    def getValue(self, list):
        self.inputValues = list
        print("GOT VALUES")

    def run(self, list):
        self.getValue(list)
        conn = pymysql.connect(host='101.132.154.2',port=3306,user='housing',passwd='housing',db='housing',charset='utf8')
        print("Connected To Database!")

        cursor = conn.cursor()
        sql = "select id,address,square,avg,floor,total,abs(square-%s) as result from guapai_201708 where address like %s having result<10.0 order by result asc ;";

        address = self.inputValues[0]
        square = self.inputValues[3]
        floor = self.inputValues[1]
        direction = self.inputValues[2]

        sum = 0
        cursor.execute(sql,(square, address+'%'))
        fangYuan = cursor.fetchmany(5)
        for each in fangYuan:
            print(each)
            sum += each[3]
        avg = sum / 5
        expected = float(avg) * float(square) / 10000

        if cursor.rownumber == 0:
            print("Result NOT Found!")
            conn.close()
            cursor.close()
            return "No Result!"

        conn.close()
        cursor.close()
        print("Average Price:", expected, "w")
        return expected


if __name__ == '__main__':
    search = search_by_address()
    search.run(['西藏南路1739弄', '10', '南', '103','2010'])
