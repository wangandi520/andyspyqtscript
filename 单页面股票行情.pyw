# encoding:utf-8
# https://github.com/wangandi520
# v0.1

import sys
import datetime
import time
import requests

from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout, QLabel, QPushButton, QTableWidget, \
    QTableWidgetItem, QHeaderView, QLineEdit, QStatusBar
from PyQt5.QtGui import QBrush, QColor
from PyQt5.QtCore import QSize, QUrl, Qt, QTimer, QDateTime
from classandysAboutButton import andysDonateButton

# pip install pyqt5 pyqt5-tools requests pillow

class MyQWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('单页面股票行情v0.1')
        self.stockDataWidget = QTableWidget()
        self.inputSearchValueLineEdit = QLineEdit()
        self.inputSearchValueLineEdit.setText('sh600036')
        self.inputSearchValueLineEdit.returnPressed.connect(self.setStockData)
        self.searchButton = QPushButton('查询')
        self.searchButton.setShortcut(Qt.Key_F5)
        self.searchButton.clicked.connect(self.setStockData)
        self.donateButton = andysDonateButton('捐赠')
        
        self.statusBar = QStatusBar()
        self.searchStatus = QLabel('准备就绪')
        self.currentTime = QLabel()
        
        self.statusBar.addWidget(self.searchStatus, 100)
        self.statusBar.addWidget(self.currentTime,100)
        currentClockTimer = QTimer(self)
        currentClockTimer.start(1000)
        currentClockTimer.timeout.connect(self.showNowTime)
        

        topLayout = QHBoxLayout()
        middleLayout = QVBoxLayout()
        bottomLayout = QVBoxLayout()
        mainLayout = QVBoxLayout()
        self.setMinimumSize(430, 580)
        mainLayout.setContentsMargins(10, 10, 10, 10)

        # 设置行数   
        self.stockDataWidget.setRowCount(14)
        self.stockDataWidget.horizontalHeader().setVisible(False)
        # 设置列数 
        self.stockDataWidget.setColumnCount(4)
        self.stockDataWidget.verticalHeader().setVisible(False)
        self.initStockData()
        self.stockDataWidget.setColumnWidth(-1, 100)
        
        # Layout设置
        topLayout.addWidget(self.inputSearchValueLineEdit)
        topLayout.addWidget(self.searchButton)
        topLayout.addWidget(self.donateButton)
        middleLayout.addWidget(self.stockDataWidget)
        bottomLayout.addWidget(self.statusBar)
        mainLayout.addLayout(topLayout)
        mainLayout.addLayout(middleLayout)
        mainLayout.addLayout(bottomLayout)
        self.setLayout(mainLayout)
    def showNowTime(self):
        # 右下角显示时间
        self.currentTime.setText(QDateTime.currentDateTime().toString("yyyy-MM-dd hh:mm:ss ddd"))  
        
    def initStockData(self):
        # 初始化股票表格数据
        # stockDataWidget股票信息基本样式
        # 股票名 股票编号 当前价格 涨跌价格 涨跌百分比
        # 卖五 价格 数量（手）
        # 卖四 价格 数量（手）
        # 卖三 价格 数量（手）
        # 卖二 价格 数量（手）
        # 卖一 价格 数量（手）
        # 买一 价格 数量（手）
        # 买二 价格 数量（手）
        # 买三 价格 数量（手）
        # 买四 价格 数量（手）
        # 买五 价格 数量（手）
        # 今开 今日开盘价 昨收 昨日收盘价
        # 最高 今日最高价 最低 今日最低价
        # 日期 时间
        self.stockDataWidget.setItem(0, 0, QTableWidgetItem('股票名'))
        self.stockDataWidget.setItem(0, 1, QTableWidgetItem('股票编号'))
        self.stockDataWidget.setItem(0, 2, QTableWidgetItem('当前价格'))
        self.stockDataWidget.setItem(0, 3, QTableWidgetItem('涨跌'))
        self.stockDataWidget.setItem(1, 0, QTableWidgetItem('卖五'))
        self.stockDataWidget.setItem(1, 1, QTableWidgetItem('0'))
        self.stockDataWidget.setItem(1, 2, QTableWidgetItem(''))
        self.stockDataWidget.setItem(1, 3, QTableWidgetItem('0'))
        self.stockDataWidget.setItem(2, 0, QTableWidgetItem('卖四'))
        self.stockDataWidget.setItem(2, 1, QTableWidgetItem('0'))
        self.stockDataWidget.setItem(2, 2, QTableWidgetItem(''))
        self.stockDataWidget.setItem(2, 3, QTableWidgetItem('0'))
        self.stockDataWidget.setItem(3, 0, QTableWidgetItem('卖三'))
        self.stockDataWidget.setItem(3, 1, QTableWidgetItem('0'))
        self.stockDataWidget.setItem(3, 2, QTableWidgetItem(''))
        self.stockDataWidget.setItem(3, 3, QTableWidgetItem('0'))
        self.stockDataWidget.setItem(4, 0, QTableWidgetItem('卖二'))
        self.stockDataWidget.setItem(4, 1, QTableWidgetItem('0'))
        self.stockDataWidget.setItem(4, 2, QTableWidgetItem(''))
        self.stockDataWidget.setItem(4, 3, QTableWidgetItem('0'))
        self.stockDataWidget.setItem(5, 0, QTableWidgetItem('卖一'))
        self.stockDataWidget.setItem(5, 1, QTableWidgetItem('0'))
        self.stockDataWidget.setItem(5, 2, QTableWidgetItem(''))
        self.stockDataWidget.setItem(5, 3, QTableWidgetItem('0'))
        self.stockDataWidget.setItem(6, 0, QTableWidgetItem('买一'))
        self.stockDataWidget.setItem(6, 1, QTableWidgetItem('0'))
        self.stockDataWidget.setItem(6, 2, QTableWidgetItem(''))
        self.stockDataWidget.setItem(6, 3, QTableWidgetItem('0'))
        self.stockDataWidget.setItem(7, 0, QTableWidgetItem('买二'))
        self.stockDataWidget.setItem(7, 1, QTableWidgetItem('0'))
        self.stockDataWidget.setItem(7, 2, QTableWidgetItem(''))
        self.stockDataWidget.setItem(7, 3, QTableWidgetItem('0'))
        self.stockDataWidget.setItem(8, 0, QTableWidgetItem('买三'))
        self.stockDataWidget.setItem(8, 1, QTableWidgetItem('0'))
        self.stockDataWidget.setItem(8, 2, QTableWidgetItem(''))
        self.stockDataWidget.setItem(8, 3, QTableWidgetItem('0'))
        self.stockDataWidget.setItem(9, 0, QTableWidgetItem('买四'))
        self.stockDataWidget.setItem(9, 1, QTableWidgetItem('0'))
        self.stockDataWidget.setItem(9, 2, QTableWidgetItem(''))
        self.stockDataWidget.setItem(9, 3, QTableWidgetItem('0'))
        self.stockDataWidget.setItem(10, 0, QTableWidgetItem('买五'))
        self.stockDataWidget.setItem(10, 1, QTableWidgetItem('0'))
        self.stockDataWidget.setItem(10, 2, QTableWidgetItem(''))
        self.stockDataWidget.setItem(10, 3, QTableWidgetItem('0'))
        self.stockDataWidget.setItem(11, 0, QTableWidgetItem('今开'))
        self.stockDataWidget.setItem(11, 1, QTableWidgetItem('0'))
        self.stockDataWidget.setItem(11, 2, QTableWidgetItem('昨收'))
        self.stockDataWidget.setItem(11, 3, QTableWidgetItem('0'))
        self.stockDataWidget.setItem(12, 0, QTableWidgetItem('最高'))
        self.stockDataWidget.setItem(12, 1, QTableWidgetItem('0'))
        self.stockDataWidget.setItem(12, 2, QTableWidgetItem('最低'))
        self.stockDataWidget.setItem(12, 3, QTableWidgetItem('0'))
        self.stockDataWidget.setItem(13, 0, QTableWidgetItem('日期'))
        self.stockDataWidget.setItem(13, 1, QTableWidgetItem('时间'))
        self.stockDataWidget.setItem(13, 2, QTableWidgetItem(''))
        self.stockDataWidget.setItem(13, 3, QTableWidgetItem(''))
        
    def getStockData(self):
        # 获取股票数据
        # 股票数据接口
        # 新浪接口
	# 0：”大秦铁路”，股票名
	# 1：”27.55″，今日开盘价
	# 2：”27.25″，昨日收盘价
	# 3：”26.91″，当前价格
	# 4：”27.55″，今日最高价
	# 5：”26.20″，今日最低价
	# 6：”26.91″，竞买价，即“买一”报价
	# 7：”26.92″，竞卖价，即“卖一”报价
	# 8：”22114263″，成交的股票数，由于股票交易以一百股为基本单位，所以在使用时，通常把该值除以一百
	# 9：”589824680″，成交金额，单位为“元”，为了一目了然，通常以“万元”为成交金额的单位，所以通常把该值除以一万
	# 10：”4695″，“买一”4695股，即47手
	# 11：”26.91″，“买一”报价
	# (12, 13), (14, 15), (16, 17), (18, 19)分别为“买二”至“买四的情况”
	# 20：”3100″，“卖一”3100股，即31手；
	# 21：”26.92″，“卖一”报价
	# (22, 23), (24, 25), (26,27), (28, 29)分别为“卖二”至“卖五的情况”
	# 30：”2008-01-11″，日期
	# 31：”15:05:32″，时间
        interfaceUrl = 'https://hq.sinajs.cn/list='
        headers={'Referer':'https://finance.sina.com.cn'}
        # 腾讯接口
        # interfaceUrl = 'http://qt.gtimg.cn/q='
        # headers={'Referer':''}
        # 获取股票编号
        if self.inputSearchValueLineEdit.text() != '':
            myStockCode = self.inputSearchValueLineEdit.text()
        myUrl = interfaceUrl + myStockCode
        response = requests.post(myUrl, headers = headers)
        # 返回数据以新浪的格式顺序为准
        if response.status_code == 200:
            getWebReturnData =  response.text
        # 从新浪数据转换
        getStockAllData  = getWebReturnData.split('=')[1][1:-3].split(',') 
        if float(getStockAllData[3]) == 0.00:
            return
        # 转换不同接口的数据为统一格式列表
        # 列表数据：
        # 0  股票名
        # 1  股票编号
        # 2  当前价格
        # 3  涨跌价格
        # 4  涨跌百分比
        # 5  卖五价格
        # 6  卖五数量
        # 7  卖四价格
        # 8  卖四数量
        # 9  卖三价格
        # 10 卖三数量
        # 11 卖二价格
        # 12 卖二数量
        # 13 卖一价格
        # 14 卖一数量
        # 15 买一价格
        # 16 买一数量
        # 17 买二价格
        # 18 买二数量
        # 19 买三价格 
        # 20 买三数量
        # 21 买四价格
        # 22 买四数量
        # 23 买五价格
        # 24 买五数量
        # 25 今开 今日开盘价
        # 26 昨收 昨日收盘价
        # 27 最高 今日最高价
        # 28 最低 今日最低价
        # 29 日期
        # 30 时间
        # 转换后的数据列表myStockData
        myStockData = []
        # 涨跌价格
        zhangdiePrice =  round(float(getStockAllData[3]) - float(getStockAllData[2]), 2)
        # 涨跌百分比
        zhangdiePercent = round((float(getStockAllData[3]) - float(getStockAllData[2])) / float(getStockAllData[2]) * 100, 2)
        myStockData.append(getStockAllData[0])
        myStockData.append(myStockCode)
        myStockData.append(str(round(float(getStockAllData[3]), 2)))
        myStockData.append(str(zhangdiePrice))
        myStockData.append(str(zhangdiePercent))
        myStockData.append(str(round(float(getStockAllData[29]), 2)))
        myStockData.append(str(round(int(getStockAllData[28]) / 100)))
        myStockData.append(str(round(float(getStockAllData[27]), 2)))
        myStockData.append(str(round(int(getStockAllData[26]) / 100)))
        myStockData.append(str(round(float(getStockAllData[25]), 2)))
        myStockData.append(str(round(int(getStockAllData[24]) / 100)))
        myStockData.append(str(round(float(getStockAllData[23]), 2)))
        myStockData.append(str(round(int(getStockAllData[22]) / 100)))
        myStockData.append(str(round(float(getStockAllData[21]), 2)))
        myStockData.append(str(round(int(getStockAllData[20]) / 100)))
        myStockData.append(str(round(float(getStockAllData[11]), 2)))
        myStockData.append(str(round(int(getStockAllData[10]) / 100)))
        myStockData.append(str(round(float(getStockAllData[13]), 2)))
        myStockData.append(str(round(int(getStockAllData[12]) / 100)))
        myStockData.append(str(round(float(getStockAllData[15]), 2)))
        myStockData.append(str(round(int(getStockAllData[14]) / 100)))
        myStockData.append(str(round(float(getStockAllData[17]), 2)))
        myStockData.append(str(round(int(getStockAllData[16]) / 100)))
        myStockData.append(str(round(float(getStockAllData[19]), 2)))
        myStockData.append(str(round(int(getStockAllData[18]) / 100)))
        myStockData.append(str(round(float(getStockAllData[1]), 2)))
        myStockData.append(str(round(float(getStockAllData[2]), 2)))
        myStockData.append(str(round(float(getStockAllData[4]), 2)))
        myStockData.append(str(round(float(getStockAllData[5]), 2)))
        myStockData.append(getStockAllData[30])
        myStockData.append(getStockAllData[31])
        return myStockData

    def getRedOrGreen(self, nowPrice, yesterdayPrice):
        # 判断价格颜色，使用当前价格和昨收价格比对
        if float(nowPrice) > float(yesterdayPrice):
            return 'red'
        elif float(nowPrice) == float(yesterdayPrice):
            return 'black'
        elif float(nowPrice) < float(yesterdayPrice):
            return 'green'
        
    def setStockData(self):
        self.searchStatus.setText('查询中')
        myStockData = self.getStockData()
        if myStockData:
            self.stockDataWidget.setItem(0, 0, QTableWidgetItem(myStockData[0]))
            self.stockDataWidget.setItem(0, 1, QTableWidgetItem(myStockData[1]))
            
            tempWidgetItem = QTableWidgetItem(myStockData[2])
            tempWidgetItem.setForeground(QBrush(QColor(self.getRedOrGreen(myStockData[2], myStockData[26]))))
            self.stockDataWidget.setItem(0, 2, tempWidgetItem)
            
            tempWidgetItem = QTableWidgetItem(myStockData[3] + ' ' + myStockData[4] + '%')
            tempWidgetItem.setForeground(QBrush(QColor(self.getRedOrGreen(myStockData[2], myStockData[26]))))
            self.stockDataWidget.setItem(0, 3, tempWidgetItem)
            
            tempWidgetItem = QTableWidgetItem(myStockData[5])
            tempWidgetItem.setForeground(QBrush(QColor(self.getRedOrGreen(myStockData[5], myStockData[26]))))
            self.stockDataWidget.setItem(1, 1, tempWidgetItem)
            self.stockDataWidget.setItem(1, 3, QTableWidgetItem(myStockData[6]))
            
            tempWidgetItem = QTableWidgetItem( myStockData[7])
            tempWidgetItem.setForeground(QBrush(QColor(self.getRedOrGreen(myStockData[7], myStockData[26]))))
            self.stockDataWidget.setItem(2, 1, tempWidgetItem)
            self.stockDataWidget.setItem(2, 3, QTableWidgetItem(myStockData[8]))    
            
            tempWidgetItem = QTableWidgetItem( myStockData[9])
            tempWidgetItem.setForeground(QBrush(QColor(self.getRedOrGreen(myStockData[9], myStockData[26]))))
            self.stockDataWidget.setItem(3, 1, tempWidgetItem)
            self.stockDataWidget.setItem(3, 3, QTableWidgetItem(myStockData[10]))
                    
            tempWidgetItem = QTableWidgetItem(myStockData[11])
            tempWidgetItem.setForeground(QBrush(QColor(self.getRedOrGreen(myStockData[11], myStockData[26]))))
            self.stockDataWidget.setItem(4, 1, tempWidgetItem)
            self.stockDataWidget.setItem(4, 3, QTableWidgetItem(myStockData[12]))
                    
            tempWidgetItem = QTableWidgetItem(myStockData[13])
            tempWidgetItem.setForeground(QBrush(QColor(self.getRedOrGreen(myStockData[13], myStockData[26]))))
            self.stockDataWidget.setItem(5, 1, tempWidgetItem)
            self.stockDataWidget.setItem(5, 3, QTableWidgetItem(myStockData[14]))
                    
            tempWidgetItem = QTableWidgetItem(myStockData[15])
            tempWidgetItem.setForeground(QBrush(QColor(self.getRedOrGreen(myStockData[15], myStockData[26]))))
            self.stockDataWidget.setItem(6, 1, tempWidgetItem)
            self.stockDataWidget.setItem(6, 3, QTableWidgetItem(myStockData[16]))
                    
            tempWidgetItem = QTableWidgetItem(myStockData[17])
            tempWidgetItem.setForeground(QBrush(QColor(self.getRedOrGreen(myStockData[17], myStockData[26]))))
            self.stockDataWidget.setItem(7, 1, tempWidgetItem)
            self.stockDataWidget.setItem(7, 3, QTableWidgetItem(myStockData[18]))
                    
            tempWidgetItem = QTableWidgetItem(myStockData[19])
            tempWidgetItem.setForeground(QBrush(QColor(self.getRedOrGreen(myStockData[19], myStockData[26]))))
            self.stockDataWidget.setItem(8, 1, tempWidgetItem)
            self.stockDataWidget.setItem(8, 3, QTableWidgetItem(myStockData[20]))
                    
            tempWidgetItem = QTableWidgetItem(myStockData[21])
            tempWidgetItem.setForeground(QBrush(QColor(self.getRedOrGreen(myStockData[21], myStockData[26]))))
            self.stockDataWidget.setItem(9, 1, tempWidgetItem)
            self.stockDataWidget.setItem(9, 3, QTableWidgetItem(myStockData[22]))
                    
            tempWidgetItem = QTableWidgetItem(myStockData[23])
            tempWidgetItem.setForeground(QBrush(QColor(self.getRedOrGreen(myStockData[23], myStockData[26]))))
            self.stockDataWidget.setItem(10, 1, tempWidgetItem)
            self.stockDataWidget.setItem(10, 3, QTableWidgetItem(myStockData[24]))
            
            tempWidgetItem = QTableWidgetItem(myStockData[25])
            tempWidgetItem.setForeground(QBrush(QColor(self.getRedOrGreen(myStockData[25], myStockData[26]))))
            self.stockDataWidget.setItem(11, 1, tempWidgetItem)
            tempWidgetItem = QTableWidgetItem(myStockData[26])
            tempWidgetItem.setForeground(QBrush(QColor(self.getRedOrGreen(myStockData[26], myStockData[26]))))
            self.stockDataWidget.setItem(11, 3, tempWidgetItem)
            tempWidgetItem = QTableWidgetItem(myStockData[27])
            tempWidgetItem.setForeground(QBrush(QColor(self.getRedOrGreen(myStockData[27], myStockData[26]))))
            self.stockDataWidget.setItem(12, 1, tempWidgetItem)
            tempWidgetItem = QTableWidgetItem(myStockData[28])
            tempWidgetItem.setForeground(QBrush(QColor(self.getRedOrGreen(myStockData[28], myStockData[26]))))
            self.stockDataWidget.setItem(12, 3, tempWidgetItem)
            self.stockDataWidget.setItem(13, 0, QTableWidgetItem(myStockData[29]))
            self.stockDataWidget.setItem(13, 1, QTableWidgetItem(myStockData[30]))
            self.searchStatus.setText('查询成功')
        else:
            self.searchStatus.setText('查询失败')
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mywidget = MyQWidget()
    mywidget.show()
    sys.exit(app.exec_())
