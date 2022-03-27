# encoding:utf-8
# https://github.com/wangandi520

import sys

from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout, QListWidget, QPushButton, QFileDialog, QAbstractItemView
from PyQt5.QtCore import Qt, QObject, pyqtSignal
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
        self.currentSelectedFileListArray = []
        self.fileListWidget = QListWidget()
        self.ifFirstDrop = False
        self.openFileButton = QPushButton('添加')
        self.deleteFileButton = QPushButton('删除')
        self.clearListButton = QPushButton('清空')
        
        # mode = 1，仅加载文件。mode = 2，仅加载文件夹
        #self.mode = 1
        
        self.openFileButton.clicked.connect(self.doOpenFileButton)
        self.deleteFileButton.clicked.connect(self.doDeleteFileButton)
        self.clearListButton.clicked.connect(self.doClearListButton)
        self.fileListWidget.currentRowChanged.connect(self.doCurrentRowChanged)
        self.fileListWidget.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.fileListWidget.selectionModel().selectionChanged.connect(self.doSelectionChanged)
        
        topLayout = QHBoxLayout()
        topLayout.addWidget(self.openFileButton)
        topLayout.addWidget(self.deleteFileButton)
        topLayout.addWidget(self.clearListButton)
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
                    self.ifFirstDrop = False
                    self.allFileListArray.append(Path(filePath[8:]))
                    self.fileListWidget.addItem(Path(filePath[8:]).name)
                    self.fileListChangedSignal.emit()
                if Path.is_dir(Path(filePath[8:])):
                    if(self.ifFirstDrop == False and len(self.allFileListArray) == 0):
                        self.ifFirstDrop = True
                    else:
                        self.ifFirstDrop = False
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
            
    # def getMode(self):
        # return self.mode
        
    def getFirstDrop(self):
        return self.ifFirstDrop
        
    def getCurrentRowFilePath(self):
        if len(self.allFileListArray) > 0:
            return self.allFileListArray[self.fileListWidget.currentRow()]     
            
    def getAllFileListArray(self):
        return self.allFileListArray
        
    def getLastRowFilePath(self):
        if len(self.allFileListArray) > 0:
            return self.allFileListArray[-1]
        
    def getThisRowFilePath(self, rowNumber):
        # index start = 0
        if (rowNumber < len(self.allFileListArray) and len(self.allFileListArray) > 0):
            return self.allFileListArray[rowNumber]
        else:
            return ''
            
    def getCurrentRowFilePath(self):
        if len(self.allFileListArray) > 0:
            return self.allFileListArray[self.fileListWidget.currentRow()]     
            
    def getCurrentRow(self):
        return self.fileListWidget.currentRow()

    def setOpenFileButtonDisabled(self):
        self.openFileButton.setDisabled(True)
        
    def setDeleteFileButtonDisabled(self):
        self.deleteFileButton.setDisabled(True)
        
    def setClearListDisabled(self):
        self.clearListButton.setDisabled(True)
        
    def setCurrentRowFilePath(self, newPath):
        if len(self.allFileListArray) > 0:
            self.allFileListArray[self.fileListWidget.currentRow()] = newPath
            
    # def setMode(self, value):
        # self.mode = value
        # return self.mode
        
    def doSelectionChanged(self):
        # 被选中的文件的路径
        selectedListWidgetItemInOtherArray = [self.allFileListArray[getIndex.row()] for getIndex in self.fileListWidget.selectedIndexes()]
        self.currentSelectedFileListArray = selectedListWidgetItemInOtherArray
    
    def doCurrentRowChanged(self):
        self.currentRowChangedSignal.emit()
        # for i in range(self.fileListWidget.count()):
            # print(self.fileListWidget.item(i).text())
        #for eachItem in self.fileListWidget.selectedItems():
            # print(self.fileListWidget.currentRow())

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
        
        self.fileListChangedSignal.emit()

    def doClearListButton(self):
        self.fileListWidget.clear()
        self.allFileListArray = []
        self.fileListChangedSignal.emit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mywidget = andysFileListWidget()
    mywidget.show()
    sys.exit(app.exec_())
