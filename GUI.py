# -*- coding: utf-8 -*-
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtSql import *
from base import *

class SearchWidget(QWidget):
    search_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setUpUI()

    def setUpUI(self):

        Layout = QGridLayout(self)

        g = QGridLayout()
        v = QVBoxLayout()

        self.resize(500, 500)
        self.setWindowTitle("二手房估价")
        self.searchLabel = QLabel("二手房估价")
        self.searchLabel.setAlignment(Qt.AlignCenter)
        self.searchLabel.setFixedHeight(100)

        self.addressLabel = QLabel("地    址: ")
        self.addressLineEdit = QLineEdit()
        self.addressLineEdit.setFixedHeight(30)
        self.addressLineEdit.setFixedWidth(180)

        self.floorLabel = QLabel("楼    层: ")
        self.floorLineEdit = QLineEdit()
        self.floorLineEdit.setFixedHeight(30)
        self.floorLineEdit.setFixedWidth(180)

        self.maxfloorLabel = QLabel("总 楼 层: ")
        self.maxfloorLineEdit = QLineEdit()
        self.maxfloorLineEdit.setFixedHeight(30)
        self.maxfloorLineEdit.setFixedWidth(180)

        self.aspectLable = QLabel("朝    向: ")
        self.aspectComboBox = QComboBox()
        aspect = ['南', '北', '南北', '东', '西','暂无']
        self.aspectComboBox.setFixedHeight(30)
        self.aspectComboBox.setFixedWidth(180)
        self.aspectComboBox.addItems(aspect)

        self.squareLabel = QLabel("面    积: ")
        self.squareLineEdit = QLineEdit()
        self.squareLineEdit.setFixedHeight(30)
        self.squareLineEdit.setFixedWidth(180)

        self.comyearLabel = QLabel("竣工年份: ")
        self.comyearLineEdit = QLineEdit()
        self.comyearLineEdit.setFixedHeight(30)
        self.comyearLineEdit.setFixedWidth(180)

        self.confirmbutton = QPushButton("确认")
        self.confirmbutton.setFixedWidth(60)
        self.confirmbutton.setFixedHeight(35)
        self.confirmbutton.clicked.connect(self.showInfo)

        self.plateButton = QPushButton("板块估价")
        self.plateButton.setFixedWidth(120)
        self.plateButton.setFixedHeight(35)
        self.plateButton.clicked.connect(self.showInfo2)

        self.val2 = QLabel('[板块，均价]', self)

        g.addWidget(self.addressLabel,0,0)
        g.addWidget(self.addressLineEdit,0,1)
        g.addWidget(self.floorLabel,1,0)
        g.addWidget(self.floorLineEdit,1,1)
        g.addWidget(self.maxfloorLabel,2,0)
        g.addWidget(self.maxfloorLineEdit,2,1)
        g.addWidget(self.aspectLable,3,0)
        g.addWidget(self.aspectComboBox,3,1)
        g.addWidget(self.squareLabel,4,0)
        g.addWidget(self.squareLineEdit,4,1)
        g.addWidget(self.comyearLabel,5,0)
        g.addWidget(self.comyearLineEdit,5,1)
        g.addWidget(self.confirmbutton,6,0)
        g.addWidget(self.plateButton, 7, 0)
        g.addWidget(self.val2, 7, 1)
        Layout.addLayout(g, 0, 0)
        Layout.addLayout(v, 1, 0)

    def showInfo(self):
        Elements = self.getElements()
        # 警告
        if Elements[0] == '' or Elements[1]== '' or Elements[3] == '' or Elements[4] == '':
            print(QMessageBox.warning(self, "警告", "请填写完整", QMessageBox.Yes, QMessageBox.Yes))
            return
        if Elements[5] == None:
            Elements[5] == 2000
        base0 = base(Elements)
        self.Newwindow = Window2(base0.get5Houses())
        self.Newwindow.show()
        average_price = base0.getAvg()
        self.Newwindow.val2.setText("%.2d" % average_price)
        self.close()
        # self.val.setText(str(base0.getPrice()))
        # self.val.adjustSize()
        return

    def showInfo2(self):
        Elements = self.getElements()
        if Elements[0] == '':
            print(QMessageBox.warning(self, "警告", "请填写地址", QMessageBox.Yes, QMessageBox.Yes))
            return
        else:
            base0 = base(Elements)
            self.val2.setText(str(base0.getPlateprice()))
            self.val2.adjustSize()

    def getElements(self):
        address = self.addressLineEdit.text()
        floor = self.floorLineEdit.text()
        maxfloor = self.maxfloorLineEdit.text()
        aspect = self.aspectComboBox.currentText()
        square = self.squareLineEdit.text()
        comyear = self.comyearLineEdit.text()
        return [address, floor, aspect, square, maxfloor, comyear]









class Window2(QWidget):
    def __init__(self, fiveHouses):
        super(Window2, self).__init__()
        self.setWindowTitle("类似房源")
        self.resize(800,350)
        self.fiveHouse = fiveHouses
        self.selectedHouse = []
        self.checkBoxList = []
        print(self.fiveHouse)


        self.remindLabel = QLabel("请选择三套类似房源：")
        tableWidget=QTableWidget()
        tableWidget.setRowCount(5)
        tableWidget.setColumnCount(8)
        tableWidget.setHorizontalHeaderLabels(['勾选','编号','地址','楼层','总楼层','朝向','面积','竣工年份'])
        tableWidget.setVerticalHeaderLabels(['1','2','3','4','5'])
        tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)

        for i in range(5):  # 填入数据
            tableWidget.setItem(i, 1, QTableWidgetItem(str(i+1)))
            for j in range(2, 8):
                tableWidget.setItem(i, j, QTableWidgetItem(str(self.fiveHouse[i][j-2])))
        for i in range(5):
            for j in range(1):
                qcheck = QCheckBox()
                self.checkBoxList.append(qcheck)
                tableWidget.setCellWidget(i,j,qcheck)

        self.button = QPushButton("确认")
        self.button.setFixedWidth(60)
        self.button.setFixedHeight(35)
        self.button.clicked.connect(self.showPrice)

        self.val=QLabel('value',self)
        self.val2 = QLabel('value', self)

        self.returnbutton = QPushButton("返回")
        self.returnbutton.setFixedWidth(60)
        self.returnbutton.setFixedHeight(35)
        self.returnbutton.clicked.connect(self.back)



        Layout = QGridLayout(self)
        g = QGridLayout()
        v = QGridLayout()
        g.addWidget(self.remindLabel,0,0)
        g.addWidget(tableWidget,2,0)
        v.addWidget(self.button,0,1)
        v.addWidget(self.val,0,2)
        v.addWidget(self.val2, 1, 2)
        v.addWidget(self.returnbutton,0,3)
        Layout.addLayout(g, 0, 0)
        Layout.addLayout(v, 1, 0)

    def back(self):
        ex = SearchWidget()
        ex.show()
        self.hide()



    def showPrice(self):
        self.selectedHouse.clear()
        for i in range(5):
            if self.checkBoxList[i].isChecked():
                self.selectedHouse.append(self.fiveHouse[i])
        print("Selected Houses:",self.selectedHouse)
        count = 0
        total = 0
        for each in self.selectedHouse:

            #### Modify Each! ####

            total += each[6]
            count += 1
        average_price = float(total)/float(count)
        print("Average price (To Be Modified)",average_price)
        self.val.setText("%.2d" %average_price)


    # def run(self):
    #     for i in range(5):
    #         for j in range(1):
    #             qcheck = QCheckBox()
    #             if qcheck.isChecked():
    #                 checklist.append(tableWidget(i, 1))
        #这里一直改不对OTZ
        #for i in range(5):
        #    check=0
        #    for j in range(1):
        #        if qcheck.isChecked():
        #           check=check + 1

        #if check != 3:
        #    print(QMessageBox.warning(self, "警告", "请选择三套房源", QMessageBox.Yes, QMessageBox.Yes))
        #else:
        #    self.val=
        #    return

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex= SearchWidget()
    # ex= Window2([['西藏南路1108弄', 20, 30, 4, 130.0, 2008, 80770.0], ['西藏南路1739弄1-9号', 10, 20, 4, 130.0, 2008, 96154.0], ['西藏南路1739弄1-9号', 21, 31, 4, 130.0, 2008, 76924.0], ['西藏南路1200弄', 19, 30, 3, 130.0, 2008, 80770.0], ['西藏南路1739弄1-9号', 21, 31, 4, 130.0, 2008, 76924.0]])
    ex.show()
    app.exec_()
