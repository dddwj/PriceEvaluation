# -*- coding: utf-8 -*-

from modification import modification
from searchMain import search_by_address

class base():
    # def __init__(self):
    #     self.list = ['西藏南路1739弄', '10', '南', '103', '34', '2010']

    def __init__(self,list):
        self.list = list

    def __run(self):
        search = search_by_address()
        avg_price = search.run(self.list)
        self.houses = search.fangYuan;

        if isinstance(avg_price, str):
            price = avg_price
        else:
            modi = modification(avg_price,self.list)
            expected_price = modi.run()
            price = float('%.4f' % expected_price)
        print("Final Price = ",price)
        return price

    def getPrice(self):
        price = self.__run()
        if isinstance(price, str):
            return price
        else:
            return price

    def get3Houses(self):
        threeHouses = []
        for count in range(len(self.houses)) :
            if count >= 3:
                break
            # List structure: [address, floor, aspect, square, maxfloor, comyear]
            threeHouses.append([self.houses[count][1],self.houses[count][4],self.houses[count][7],self.houses[count][2],self.houses[count][6],self.houses[count][8]])
        return threeHouses

    def getSearchInformation(self):
        SearchInformation = [None,None,None,None,None]
        for count in range(len(self.houses)):
            if count >=5:
                break
            SearchInformation[count] = [self.houses[count][0],self.houses[count][3],self.houses[count][1],self.houses[count][4],self.houses[count][7],self.houses[count][2],self.houses[count][6],self.houses[count][8]]
        return SearchInformation





if __name__ == '__main__':
    base0 = base(['西藏南路1739弄', '10', '南', '103', '34', '2010']);
    base0.getPrice()
