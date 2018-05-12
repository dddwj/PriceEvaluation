class modification():

    def getPrice(self, avg_price):
        self.avg_price = avg_price

    def getInfo(self, list):
        self.info = list

    def run(self, avg_price, list):
        self.getPrice(avg_price)
        self.getInfo(list)
        self.avg_price = self.modi_direction()
        self.avg_price = self.modi_floor()
        print("avg_price =", self.avg_price)
        return self.avg_price

    def modi_direction(self):
        direction = self.info[2]
        raw_price = self.avg_price
        if direction == "南":
            raw_price
        elif direction == '东':
            raw_price = raw_price * (1-0.015)
        elif direction == '西':
            raw_price = raw_price * (1-0.020)
        elif direction == '北':
            raw_price = raw_price * (1-0.040)
        elif direction == '南北':
            raw_price
        elif direction == '暂无':
            raw_price = raw_price * (1-0.020)

        print("Direction modified:", raw_price)
        return raw_price

# 南（3） 0%      东 -1.5%     西（2） -2%      北（1）  -4%       暂无（0） -2%      南北(4) 0%


    def modi_floor(self):
        floor = int(self.info[1])
        height = int(self.info[4])
        raw_price = self.avg_price
        if floor == 1 :
            raw_price *= (1-0.03)
        elif floor == 2:
            raw_price *= (1-0.01)
        elif floor == 3:
            raw_price *= (1 - 0.005)
        elif floor == 4:
            raw_price *= (1 - 0.00)
        elif floor == 5:
            raw_price *= (1 - 0.00)
        elif floor == 6:
            raw_price *= (1 + 0.005)
        elif floor == 7:
            raw_price *= (1 + 0.01)
        elif floor == height:
            raw_price *= (1.01 + (0.005*(floor - 7 - 1)))
        else:
            raw_price *= (1.01 + (0.005*(floor - 7)))

        print("Floor modified:", raw_price)
        return raw_price



if __name__ == '__main__':
    modi = modification()
    modi.run(994.9948,['西藏南路1739弄', '10', '南北', '103', '31'])