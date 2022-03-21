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
        helpLayout = QHBoxLayout()
        mainLayout = QHBoxLayout()
        
        self.inputButton = QPushButton('输入')
        self.outputTButton = QPushButton('繁体')
        self.outputSButton = QPushButton('简体')
        self.outputLetterButton = QPushButton('字母')
        self.outputFirstLetterButton = QPushButton('首字母')
        setButtonFunctionLabel = QLabel('设置按钮功能')
        self.setFunctionCopyButton = QRadioButton('复制内容')
        self.setFunctionCopyButton.setChecked(True)
        self.setFunctionRenameButton = QRadioButton('修改文件名')
        helpLabel = QLabel('点击按钮复制对应内容，支持拖拽文件')
        self.inputLineEdit = QLineEdit()
        self.outputTLineEdit = QLineEdit()
        self.outputSLineEdit = QLineEdit()
        self.outputLetterLineEdit = QLineEdit()
        self.outputFirstLetterLineEdit = QLineEdit()
        self.setMinimumSize(500, 200)
        
        self.currentFilePath = ''
        self.setAcceptDrops(True)

        # 事件
        self.fileListWidget.getFilePathSignal.connect(self.doGetFilePathSlot)
        self.setFunctionCopyButton.toggled.connect(lambda isChecked: print(isChecked))
        self.setFunctionRenameButton.toggled.connect(lambda isChecked: print(isChecked))
        self.inputLineEdit.textChanged.connect(self.convertText)
        self.inputButton.clicked.connect(self.doInputText)
        self.outputTButton.clicked.connect(self.doOutputTText)
        self.outputSButton.clicked.connect(self.doOutputSText)
        self.outputLetterButton.clicked.connect(self.doOutputLetterText)
        self.outputFirstLetterButton.clicked.connect(self.doOutputFirstLetterText)
        
        # Layout设置
        inputLayout.addWidget(self.inputButton)
        inputLayout.addWidget(self.inputLineEdit)
        outputTLayout.addWidget(self.outputTButton)
        outputTLayout.addWidget(self.outputTLineEdit)
        outputSLayout.addWidget(self.outputSButton)
        outputSLayout.addWidget(self.outputSLineEdit)
        outputLetterLayout.addWidget(self.outputLetterButton)
        outputLetterLayout.addWidget(self.outputLetterLineEdit)
        outputFirstLetterLayout.addWidget(self.outputFirstLetterButton)
        outputFirstLetterLayout.addWidget(self.outputFirstLetterLineEdit)
        helpLayout.addWidget(setButtonFunctionLabel)
        helpLayout.addWidget(self.setFunctionCopyButton)
        helpLayout.addWidget(self.setFunctionRenameButton)
        helpLayout.addWidget(helpLabel)
        
        
        leftLayout.addWidget(self.fileListWidget)
        rightLayout.addLayout(inputLayout)
        rightLayout.addLayout(outputTLayout)
        rightLayout.addLayout(outputSLayout)
        rightLayout.addLayout(outputLetterLayout)
        rightLayout.addLayout(outputFirstLetterLayout)
        rightLayout.addLayout(helpLayout)
        
        mainLayout.addLayout(leftLayout)
        mainLayout.addLayout(rightLayout)
        self.setLayout(mainLayout)
       

    def doGetFilePathSlot(self, getMessage):
        self.setWindowTitle('老王简繁转换器v1.0 当前文件：' + getMessage)
        #print(getMessage)
        self.currentFilePath = Path(getMessage)
        self.inputLineEdit.setText(Path(getMessage).stem)
        

    def convertText(self):
        self.outputTLineEdit.setText(OpenCC('s2t').convert(self.inputLineEdit.text()))
        self.outputSLineEdit.setText(OpenCC('t2s').convert(self.inputLineEdit.text()))
        self.outputLetterLineEdit.setText(''.join(lazy_pinyin(self.inputLineEdit.text())))
        self.outputFirstLetterLineEdit.setText(''.join(lazy_pinyin(self.inputLineEdit.text(), style=Style.FIRST_LETTER)))
            
            
    def doInputText(self):
        if self.setFunctionCopyButton.isChecked():
            clipboard = QApplication.clipboard()
            clipboard.setText(self.inputLineEdit.text())
        if (self.currentFilePath != '' and self.setFunctionRenameButton.isChecked()):
            Path(self.currentFilePath).rename(Path(self.currentFilePath).parent.joinpath(self.inputLineEdit.text() + Path(self.currentFilePath).suffix))
            self.currentFilePath = Path(self.currentFilePath).parent.joinpath(self.inputLineEdit.text() + Path(self.currentFilePath).suffix)
        
        
    def doOutputTText(self):
        if self.setFunctionCopyButton.isChecked():
            clipboard = QApplication.clipboard()
            clipboard.setText(self.outputTLineEdit.text())
        if (self.currentFilePath != '' and self.setFunctionRenameButton.isChecked()):
            Path(self.currentFilePath).rename(Path(self.currentFilePath).parent.joinpath(self.outputTLineEdit.text() + Path(self.currentFilePath).suffix))
            self.currentFilePath = Path(self.currentFilePath).parent.joinpath(self.outputTLineEdit.text() + Path(self.currentFilePath).suffix)
        
        
    def doOutputSText(self):
        if self.setFunctionCopyButton.isChecked():
            clipboard = QApplication.clipboard()
            clipboard.setText(self.outputSLineEdit.text())
        if (self.currentFilePath != '' and self.setFunctionRenameButton.isChecked()):
            Path(self.currentFilePath).rename(Path(self.currentFilePath).parent.joinpath(self.outputSLineEdit.text() + Path(self.currentFilePath).suffix))
            self.currentFilePath = Path(self.currentFilePath).parent.joinpath(self.outputSLineEdit.text() + Path(self.currentFilePath).suffix)
        
        
    def doOutputLetterText(self):
        if self.setFunctionCopyButton.isChecked():
            clipboard = QApplication.clipboard()
            clipboard.setText(self.outputLetterLineEdit.text())
        if (self.currentFilePath != '' and self.setFunctionRenameButton.isChecked()):
            Path(self.currentFilePath).rename(Path(self.currentFilePath).parent.joinpath(self.outputLetterLineEdit.text() + Path(self.currentFilePath).suffix))
            self.currentFilePath = Path(self.currentFilePath).parent.joinpath(self.outputLetterLineEdit.text() + Path(self.currentFilePath).suffix)
        
        
    def doOutputFirstLetterText(self):
        if self.setFunctionCopyButton.isChecked():
            clipboard = QApplication.clipboard()
            clipboard.setText(self.outputFirstLetterLineEdit.text())
        if (self.currentFilePath != '' and self.setFunctionRenameButton.isChecked()):
            Path(self.currentFilePath).rename(Path(self.currentFilePath).parent.joinpath(self.outputFirstLetterLineEdit.text() + Path(self.currentFilePath).suffix))
            self.currentFilePath = Path(self.currentFilePath).parent.joinpath(self.outputFirstLetterLineEdit.text() + Path(self.currentFilePath).suffix)
        
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    mywidget = MyQWidget()
    mywidget.show()
    sys.exit(app.exec_())