from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QLabel, QInputDialog, QTextBrowser)
import sys


from modification import modification
from searchByAddress import search_by_address



class GUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()


    def initUI(self):
        self.setGeometry(500, 300, 500, 300)
        self.setWindowTitle('二手房估价')
        self.lb1 = QLabel('地址：', self)
        self.lb1.move(20, 20)
        self.lb2 = QLabel('楼层：', self)
        self.lb2.move(20, 80)
        self.lb3 = QLabel('朝向：', self)
        self.lb3.move(20, 140)
        self.lb4 = QLabel('面积：', self)
        self.lb4.move(20, 200)
        self.lb6 = QLabel('西藏南路1739弄', self)
        self.lb6.move(80, 20)
        self.lb7 = QLabel('10', self)
        self.lb7.move(80, 80)
        self.lb8 = QLabel('南', self)
        self.lb8.move(80, 140)
        self.lb9 = QLabel('90', self)
        self.lb9.move(80, 200)
        self.bt1 = QPushButton('修改地址', self)
        self.bt1.move(200, 18)
        self.bt2 = QPushButton('修改楼层', self)
        self.bt2.move(200, 78)
        self.bt3 = QPushButton('修改朝向', self)
        self.bt3.move(200, 138)
        self.bt4 = QPushButton('修改面积', self)
        self.bt4.move(200, 198)

        btn = QPushButton('确认', self)
        btn.move(20, 240)
        btn.clicked.connect(self.runSearch)
        # 预估价格暂时显示之后修改
        self.val = QLabel('100w', self);
        self.val.move(200, 250)

        self.show()
        self.bt1.clicked.connect(self.showDialog)
        self.bt2.clicked.connect(self.showDialog)
        self.bt3.clicked.connect(self.showDialog)
        self.bt4.clicked.connect(self.showDialog)

    def showDialog(self):
        sender = self.sender()
        aspect = ['南', '北', '南北','东','西','暂无']
        if sender == self.bt1:
            text, ok = QInputDialog.getText(self, '修改地址', '请输入地址：')
            if ok:
                self.lb6.setText(text)
                self.lb6.adjustSize()
        elif sender == self.bt2:
            text, ok = QInputDialog.getInt(self, '修改楼层', '请输入楼层：', min=1)
            if ok:
                self.lb7.setText(str(text))
                self.lb7.adjustSize()
        elif sender == self.bt3:
            text, ok = QInputDialog.getItem(self, '修改朝向', '请选择朝向：', aspect)
            if ok:
                self.lb8.setText(str(text))
                self.lb8.adjustSize()
        elif sender == self.bt4:
            text, ok = QInputDialog.getInt(self, '修改面积', '请输入面积：', min=1)
            if ok:
                self.lb9.setText(str(text))
                self.lb9.adjustSize()

    def showNotFound(self):
        text, ok = QInputDialog.getInt(self, '找不到类似房源', '请重新输入')
        if ok:
            self.lb7.adjustSize()

    # 输入的值
    def Value(self):
        address = self.lb6.text()
        floor = self.lb7.text()
        direction = self.lb8.text()
        square = self.lb9.text()
        return [address, floor, direction, square,31]

    def getValue(self):
        inputVal = self.Value()
        print(inputVal)
        return inputVal

    def runSearch(self):
        #print("RUN SEARCH")
        list = self.getValue()
        search = search_by_address()
        avg_price = search.run(list)
        if isinstance(avg_price, str):
            self.showNotFound()
        else:
            modi = modification()
            expected_price = modi.run(avg_price, list)
            # expected_price = avg_price
            
            price = float('%.4f' % expected_price)
            self.val.setText( str(price) + "万")
            self.val.adjustSize()

        return


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = GUI()
    sys.exit(app.exec_())

