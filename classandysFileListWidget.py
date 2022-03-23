# encoding:utf-8
# https://github.com/wangandi520

import sys

from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout, QListWidget, QPushButton, QFileDialog
from PyQt5.QtCore import QObject, pyqtSignal
from pathlib import Path


# pip install pyqt5

class andysFileListWidget(QWidget):

    #列表内容数量发生变化时
    fileListChangedSignal = pyqtSignal()
    #被选中项目变化时
    currentRowChangedSignal = pyqtSignal()
    
    def __init__(self, parent=None):
        # 拖拽文件加入列表。如果拖拽文件夹，里面的所有文件都加入。不重复加入
        super().__init__(parent)

        self.setAcceptDrops(True)
        self.allFileListArray = []
        self.fileListWidget = QListWidget()
        openFileButton = QPushButton('添加')
        deleteFileButton = QPushButton('删除')
        clearListButton = QPushButton('清空')
        
        openFileButton.clicked.connect(self.doOpenFileButton)
        deleteFileButton.clicked.connect(self.doDeleteFileButton)
        clearListButton.clicked.connect(self.doClearListButton)
        self.fileListWidget.currentRowChanged.connect(self.doCurrentRowChanged)

        topLayout = QHBoxLayout()
        topLayout.addWidget(openFileButton)
        topLayout.addWidget(deleteFileButton)
        topLayout.addWidget(clearListButton)
        bottomLayout = QHBoxLayout()
        bottomLayout.addWidget(self.fileListWidget)
        mainLayout = QVBoxLayout()
        mainLayout.addLayout(topLayout)
        mainLayout.addLayout(bottomLayout)
        self.setLayout(mainLayout)
        
    def dragEnterEvent(self, event):
        event.accept()

    def dropEvent(self, event):
        for eachFile in event.mimeData().urls():
            filePath = eachFile.toString()
            if (filePath[0:8] == 'file:///' and Path(filePath[8:]) not in self.allFileListArray):
                if Path.is_file(Path(filePath[8:])):
                    self.allFileListArray.append(Path(filePath[8:]))
                    self.fileListWidget.addItem(Path(filePath[8:]).name)
                    self.fileListChangedSignal.emit()
                if Path.is_dir(Path(filePath[8:])):
                    for file in Path(filePath[8:]).glob('**/*'):
                        if Path.is_file(file):
                            self.allFileListArray.append(file)
                            self.fileListWidget.addItem(file.name)
                            self.fileListChangedSignal.emit()

    def dragMoveEvent(self, event):
        event.accept()

    def updateAllFileListArray(self, newArray):
        self.allFileListArray = newArray
        
    def reloadFileListWidget(self):
        self.fileListWidget.clear()
        for eachFile in self.allFileListArray:
            self.fileListWidget.addItem(eachFile.name)
            
    def getCurrentRowFilePath(self):
        if len(self.allFileListArray) > 0:
            return self.allFileListArray[self.fileListWidget.currentRow()]     
            
    def getAllFileListArray(self):
        return self.allFileListArray
        
    def setCurrentRowFilePath(self, newPath):
        if len(self.allFileListArray) > 0:
            self.allFileListArray[self.fileListWidget.currentRow()] = newPath
            
    def getLastRowFilePath(self):
        if len(self.allFileListArray) > 0:
            return self.allFileListArray[-1]
        
    def getThisRowFilePath(self, rowNumber):
        # index start = 0
        if (rowNumber < len(self.allFileListArray) and len(self.allFileListArray) > 0):
            return self.allFileListArray[rowNumber]
        else:
            return ''

    def getCurrentRow(self):
        return self.fileListWidget.currentRow()

    def doCurrentRowChanged(self):
        self.currentRowChangedSignal.emit()

    def doOpenFileButton(self):
        # 打开文件。如果是文件夹请拖拽。
        tempFileName = QFileDialog.getOpenFileNames(self, "打开文件", ".", "*.*")[0]
        for eachFilePath in tempFileName:
            if (Path(eachFilePath) not in self.allFileListArray):
                if Path.is_file(Path(eachFilePath)):
                    self.allFileListArray.append(Path(eachFilePath))
                    self.fileListWidget.addItem(Path(eachFilePath).name)
                    self.fileListChangedSignal.emit()
                if Path.is_dir(Path(eachFilePath)):
                    for eacheachFilePath in Path(eachFilePath).glob('**/*'):
                        if Path.is_file(eacheachFilePath):
                            self.allFileListArray.append(eacheachFilePath)
                            self.fileListWidget.addItem(eacheachFilePath.name)
                            self.fileListChangedSignal.emit()
        
    def doDeleteFileButton(self):
        if (self.fileListWidget.currentRow() > -1):
            self.fileListWidget.takeItem(self.fileListWidget.row(self.fileListWidget.currentItem()))
            self.allFileListArray.remove(self.allFileListArray[self.fileListWidget.currentRow()])

    def doClearListButton(self):
        self.fileListWidget.clear()
        self.allFileListArray = []


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mywidget = andysFileListWidget()
    mywidget.show()
    sys.exit(app.exec_())
