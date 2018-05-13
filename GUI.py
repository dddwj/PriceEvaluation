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
        #定义全局布局，注意参数self
        g = QGridLayout()
        v = QVBoxLayout()

        self.resize(840, 500)
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

        self.val=QLabel('value',self)

        # 表格
        self.table = QTableWidget(3, 8)
        self.table.setHorizontalHeaderLabels(
            ['地址', '楼层', '总楼层', '朝向', '面积', '均价', '竣工年份', '挂牌时间'])

        self.table.setShowGrid(False)  # 不显示网格线


        # def query(self):
        #     sql =""      #"SELECT address,floor.etc"
        #     self.queryModel.setQuery(sql)
        #     return

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
        g.addWidget(self.val,6,1)
        v.addWidget(self.table)
        Layout.addLayout(g, 0, 0)
        Layout.addLayout(v, 1, 0)
        self.show()


    def showInfo(self):
        base0 = base(self.getElements())
        self.val.setText(str(base0.getPrice()))
        self.val.adjustSize()
        self.showLists(base0.get3Houses())
        return

    def getElements(self):
        #
        # Inspect every input element here! Make it valid.
        # Some notifications to be shown.
        #
        address = self.addressLineEdit.text()
        floor = self.floorLineEdit.text()
        maxfloor = self.maxfloorLineEdit.text()
        aspect = self.aspectComboBox.currentText()
        square = self.squareLineEdit.text()
        comyear = self.comyearLineEdit.text()
        return [address, floor, aspect, square, maxfloor, comyear]

    def showLists(self,ThreeLists):
        #
        # Show THREE Houses(type: List) on UI here( ->showInfo(self) ).
        # List structure: [address, floor, aspect, square, maxfloor, comyear]
        #
        print(ThreeLists)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex= SearchWidget()
    sys.exit(app.exec_())
