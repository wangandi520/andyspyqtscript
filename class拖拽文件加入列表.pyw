# encoding:utf-8
# https://github.com/wangandi520

import sys

from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QListWidget
from pathlib import Path

# pip install pyqt5

class andysFileListWidget(QListWidget):
    def __init__(self, parent=None):
        # 拖拽文件加入列表。如果拖拽文件夹，里面的所有文件都加入。不重复加入
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.allFileListArray = []


    def dragEnterEvent(self, event):
        event.accept()
    
    
    def dropEvent(self, event):
        for eachFile in event.mimeData().urls():
            filePath = eachFile.toString()
            if (filePath[0:8] == 'file:///' and Path(filePath[8:]) not in self.allFileListArray):
                if Path.is_file(Path(filePath[8:])):
                    self.allFileListArray.append(Path(filePath[8:]))
                    self.addItem(Path(filePath[8:]).name)
                if Path.is_dir(Path(filePath[8:])):
                    for file in Path(filePath[8:]).glob('**/*'):
                        if Path.is_file(file):
                            self.allFileListArray.append(file)
                            self.addItem(file.name)
        print(self.allFileListArray)


    def dragMoveEvent(self, event):
        event.accept()

        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    mywidget = andysFileListWidget()
    mywidget.show()
    sys.exit(app.exec_())