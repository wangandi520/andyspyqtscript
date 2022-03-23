# encoding:utf-8
# https://github.com/wangandi520

import sys

from opencc import OpenCC
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout, QLabel, QLineEdit, QPushButton, QRadioButton
from PyQt5.QtCore import QSize, QUrl
from pypinyin import pinyin, lazy_pinyin, Style
from pathlib import Path
from classandysFileListWidget import andysFileListWidget

# pip install pyqt5 pyqt5-tools pypinyin opencc-python-reimplemented

class MyQWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('老王简繁转换器v1.0')
        self.fileListWidget = andysFileListWidget()
        
        inputLayout = QHBoxLayout()
        leftLayout = QHBoxLayout()
        rightLayout = QVBoxLayout()
        outputTLayout = QHBoxLayout()
        outputSLayout = QHBoxLayout()
        outputLetterLayout = QHBoxLayout()
        outputFirstLetterLayout = QHBoxLayout()
        mainLayout = QHBoxLayout()
        
        self.oldNameButton = QPushButton('原名')
        self.outputTButton = QPushButton('繁体')
        self.outputSButton = QPushButton('简体')
        self.outputLetterButton = QPushButton('字母')
        self.outputFirstLetterButton = QPushButton('首字母')
        
        self.inputLineEdit = QLineEdit()
        self.outputTLineEdit = QLineEdit()
        self.outputSLineEdit = QLineEdit()
        self.outputLetterLineEdit = QLineEdit()
        self.outputFirstLetterLineEdit = QLineEdit()
        self.setMinimumSize(600, 200)
        
        self.oldAllFilePathList = []
        self.setAcceptDrops(True)

        # 事件
        self.fileListWidget.fileListChangedSignal.connect(self.fileListChangedSlot)
        self.fileListWidget.currentRowChangedSignal.connect(self.currentRowChangedSlot)
        self.inputLineEdit.textChanged.connect(self.convertText)
        self.oldNameButton.clicked.connect(self.doOldNameText)
        self.outputTButton.clicked.connect(self.doOutputTText)
        self.outputSButton.clicked.connect(self.doOutputSText)
        self.outputLetterButton.clicked.connect(self.doOutputLetterText)
        self.outputFirstLetterButton.clicked.connect(self.doOutputFirstLetterText)
        
        # Layout设置
        inputLayout.addWidget(self.oldNameButton)
        inputLayout.addWidget(self.inputLineEdit)
        outputTLayout.addWidget(self.outputTButton)
        outputTLayout.addWidget(self.outputTLineEdit)
        outputSLayout.addWidget(self.outputSButton)
        outputSLayout.addWidget(self.outputSLineEdit)
        outputLetterLayout.addWidget(self.outputLetterButton)
        outputLetterLayout.addWidget(self.outputLetterLineEdit)
        outputFirstLetterLayout.addWidget(self.outputFirstLetterButton)
        outputFirstLetterLayout.addWidget(self.outputFirstLetterLineEdit)
                
        leftLayout.addWidget(self.fileListWidget)
        rightLayout.addLayout(inputLayout)
        rightLayout.addLayout(outputTLayout)
        rightLayout.addLayout(outputSLayout)
        rightLayout.addLayout(outputLetterLayout)
        rightLayout.addLayout(outputFirstLetterLayout)
        mainLayout.addLayout(leftLayout)
        mainLayout.addLayout(rightLayout)
        mainLayout.setStretchFactor(leftLayout, 1)
        mainLayout.setStretchFactor(rightLayout, 2)
        self.setLayout(mainLayout)    
            
    def fileListChangedSlot(self):
        self.oldAllFilePathList = self.fileListWidget.getAllFileListArray()
        self.convertText()
            
    def currentRowChangedSlot(self):
        self.convertText()
        
    def convertText(self):
        self.inputLineEdit.setText(str(self.fileListWidget.getCurrentRowFilePath().stem))
        self.outputTLineEdit.setText(OpenCC('s2t').convert(self.inputLineEdit.text()))
        self.outputSLineEdit.setText(OpenCC('t2s').convert(self.inputLineEdit.text()))
        self.outputLetterLineEdit.setText(''.join(lazy_pinyin(self.inputLineEdit.text())))
        self.outputFirstLetterLineEdit.setText(''.join(lazy_pinyin(self.inputLineEdit.text(), style=Style.FIRST_LETTER)))
            
    def doOldNameText(self):
        tempAllFilePathList = []
        for eachNewFile, eachOldFile in zip(self.fileListWidget.getAllFileListArray(), self.oldAllFilePathList):
            eachNewFile.rename(eachOldFile) 
        self.fileListWidget.updateAllFileListArray(self.oldAllFilePathList)
        self.fileListWidget.reloadFileListWidget()
            
    def doOutputTText(self):
        tempAllFilePathList = []
        for eachFilePath in self.fileListWidget.getAllFileListArray():
            newFilePath = eachFilePath.parent.joinpath(OpenCC('s2t').convert(str(eachFilePath.name)))
            eachFilePath.rename(newFilePath)
            tempAllFilePathList.append(newFilePath)
        self.fileListWidget.updateAllFileListArray(tempAllFilePathList)
        self.fileListWidget.reloadFileListWidget()
                
    def doOutputSText(self):
        tempAllFilePathList = []
        for eachFilePath in self.fileListWidget.getAllFileListArray():
            newFilePath = eachFilePath.parent.joinpath(OpenCC('t2s').convert(str(eachFilePath.name)))
            eachFilePath.rename(newFilePath)
            tempAllFilePathList.append(newFilePath)
        self.fileListWidget.updateAllFileListArray(tempAllFilePathList)
        self.fileListWidget.reloadFileListWidget()
         
    def doOutputLetterText(self):
        tempAllFilePathList = []
        for eachFilePath in self.fileListWidget.getAllFileListArray():
            newFilePath = eachFilePath.parent.joinpath(''.join(lazy_pinyin(str(eachFilePath.stem))) + eachFilePath.suffix)
            eachFilePath.rename(newFilePath)
            tempAllFilePathList.append(newFilePath)
        self.fileListWidget.updateAllFileListArray(tempAllFilePathList)
        self.fileListWidget.reloadFileListWidget()
         
    def doOutputFirstLetterText(self):
        tempAllFilePathList = []
        for eachFilePath in self.fileListWidget.getAllFileListArray():
            newFilePath = eachFilePath.parent.joinpath(''.join(lazy_pinyin(str(eachFilePath.stem), style=Style.FIRST_LETTER)) + eachFilePath.suffix)
            eachFilePath.rename(newFilePath)
            tempAllFilePathList.append(newFilePath)
        self.fileListWidget.updateAllFileListArray(tempAllFilePathList)
        self.fileListWidget.reloadFileListWidget()
          
if __name__ == '__main__':
    app = QApplication(sys.argv)
    mywidget = MyQWidget()
    mywidget.show()
    sys.exit(app.exec_())