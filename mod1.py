# -*- coding: utf-8 -*-
# by Lawrence Zhao

class Mod1():

    def run1(self):
        self.__modi_direction()
        self.__modi_floor()
        self.__monthcoe()
        self.__coeff()
        self.__calculate()

    def __init__(self, each, floor, avg):
        self.house = each
        self.floor = floor
        self.junjia= avg
        #array:0:id 1:address 2:square 3:avg 4:floor 5:total 6:height 7:direction 8:built_year 9:guapai_month
        #print("aaaaaaa",self.house[0])


    def __modi_direction(self):
        self.direction_para = 0
        self.direction_coe = 0
        #print(self.house[9])
        # 南（3） 0%      东 -1.5%     西（2） -2%      北（1）  -4%       暂无（0） -2%      南北(4) 0%
        # direction_para:朝向参数 direction_coe:百分比参数
        #     case "暂无":    return 0;
        #     case "北":      return 1;
        #     case "西南":    return 2;
        #     case "南":      return 3;
        #     case "南北":    return 4;
        #     case "西":      return 5;
        #     case "东":      return 6;
        #     case "东西":    return 7;
        #     case "东南":    return 8;
        #     case "东北":    return 9;
        if self.house[7] == 3:
            self.direction_para = 0
        elif self.house[7] == 6:
            self.direction_para = -1.5
        elif self.house[7] == 5:
            self.direction_para = -2
        elif self.house[7] == 1:
            self.direction_para = -4
        elif self.house[7] == 4:
            self.direction_para = 0
        elif self.house[7] == 0:
            self.direction_para = -2

        self.direction_coe = 100 / (100 + self.direction_para)

        #print('diretion_coe:', self.direction_coe)

    def __modi_floor(self):
        # floor_para:朝向参数 floor_coe:百分比参数
        self.floor_para = 0
        self.floor_coe = 0

        self.floor_para = 0.5*(int(self.house[4])-int(self.floor))
        self.floor_coe = 100/(100+self.floor_para)
        #print('floor coe of is', self.floor_coe)


    def __monthcoe(self):
        self.monthcoe=0
        self.currentMon = self.house[9]+12
        if self.currentMon-self.house[9] <= 2:
            self.monthcoe=1.1
        else:
            self.monthcoe=1

    def __coeff(self):
        self.modifiedCoe = 0
        self.modifiedCoe = (self.direction_coe + 0.9078*self.floor_coe) / 2
        #print(self.modifiedCoe)

    def __calculate(self):
        self.avgprice = 0
        self.avgprice = 1.11321*float(self.junjia)*float(self.modifiedCoe)*float(self.monthcoe)
        # print('avh isisisisisiis', self.avgprice)
        #print(self.avgprice)
        return self.avgprice

