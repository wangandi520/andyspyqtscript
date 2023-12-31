# encoding:utf-8
# https://github.com/wangandi520

import sys
import zipfile
import rarfile
import datetime
import time

from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout, QLabel, QPushButton, QTableWidget, \
    QTableWidgetItem, QHeaderView, QProgressBar
from PyQt5.QtCore import QSize, QUrl
from pathlib import Path
from hashlib import sha1
from classandysFileListWidget import andysFileListWidget
from classandysAboutButton import andysDonateButton


# pip install pyqt5 pyqt5-tools rarfile pillow

class MyQWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('老王SHA1生成校验器v1.2')
        self.fileListWidget = andysFileListWidget()
        self.fileListWidget.setDeleteFileButtonDisabled()
        self.fileInfoWidget = QTableWidget()
        self.allFileInfoArray = []
        self.sha1ProgressBar = QProgressBar()
        self.sha1ProgressBar.setMinimum(0)
        self.sha1ProgressBar.setMaximum(100)
        self.sha1ProgressBar.setValue(0)

        rightLayout = QVBoxLayout()
        rightTopLayout = QHBoxLayout()
        rightBottomLayout = QHBoxLayout()
        mainLayout = QVBoxLayout()

        self.getAllSha1Button = QPushButton('计算Sha1')
        self.toHtmlButton = QPushButton('输出Html')
        self.toMarkdownButton = QPushButton('输出Markdown')
        self.toSha1Button = QPushButton('输出Sha1')
        self.donateButton = andysDonateButton('捐赠')
        self.setMinimumSize(1600, 800)
        self.setAcceptDrops(True)

        rightLayout.setContentsMargins(9, 9, 9, 9)

        # 事件
        self.fileListWidget.fileListChangedSignal.connect(self.fileListChangedSlot)
        self.getAllSha1Button.clicked.connect(self.getAllSha1)
        self.toHtmlButton.clicked.connect(self.toHtmlSlot)
        self.toMarkdownButton.clicked.connect(self.toMarkdownSlot)
        self.toSha1Button.clicked.connect(self.toSha1Slot)

        # Layout设置
        rightTopLayout.addWidget(self.getAllSha1Button)
        rightTopLayout.addWidget(self.toHtmlButton)
        rightTopLayout.addWidget(self.toMarkdownButton)
        rightTopLayout.addWidget(self.toSha1Button)
        rightTopLayout.addWidget(self.donateButton)
        rightLayout.addLayout(rightTopLayout)
        rightLayout.addLayout(rightBottomLayout)
        rightLayout.addWidget(self.fileInfoWidget)
        mainLayout.addWidget(self.fileListWidget)
        mainLayout.addLayout(rightLayout)
        mainLayout.addWidget(self.sha1ProgressBar)
        mainLayout.setStretchFactor(self.fileListWidget, 1)
        mainLayout.setStretchFactor(rightLayout, 2)
        self.setLayout(mainLayout)
        self.sha1ProgressBar.close()

    def toHtmlSlot(self):
        # 转换成html格式
        returnFileInfo = [
            '<html><head><title>文件信息</title><style>table{width:auto;}table,td{border:1px solid #000000;table-layout:fixed;border-collapse:collapse;}table td:first-child{width:auto;}table td{min-width:100px;}a{text-decoration: none;}table tr:first-child{background-color:#eee;}tr:hover{background-color:#eee;}</style></head><body><table id="allFileTable"><tr><td>文件夹名</td><td>SHA1校验码</td><td>文件类型</td><td>文件大小</td><td>修改时间</td><td>是否加密</td><td>压缩包内文件数量</td><td>压缩包内文件夹数量</td><td>扩展名对应的文件数量</td></tr>']

        for eachInfo in self.allFileInfoArray:
            newContent = '<tr>'
            for eachString in eachInfo:
                newContent = newContent + '<td>' + str(eachString) + '</td>'
            returnFileInfo.append(newContent + '</tr>')
        returnFileInfo.append('</table></body></html>')
        self.writeFile('html', returnFileInfo)

    def toMarkdownSlot(self):
        # 转换成markdown格式
        returnFileInfo = ['|文件夹名|SHA1校验码|文件类型|文件大小|修改时间|是否加密|压缩包内文件数量|压缩包内文件夹数量|扩展名对应的文件数量|\n',
                          '| --- | --- | --- | --- | --- | --- | --- | --- | --- |\n']

        for eachInfo in self.allFileInfoArray:
            newContent = '|'
            for eachString in eachInfo:
                newContent = newContent + str(eachString) + '|'
            returnFileInfo.append(newContent + '\n')
        self.writeFile('md', returnFileInfo)

    def toSha1Slot(self):
        returnFileInfo = []
        for eachInfo in self.allFileInfoArray:
            returnFileInfo.append(eachInfo[1] + ' *' + eachInfo[0] + '\n')
        self.writeFile('sha', returnFileInfo)

    def fileListChangedSlot(self):
        if len(self.fileListWidget.getAllFileListArray()) == 0:
            self.fileInfoWidget.clear()
            self.fileInfoWidget.setColumnCount(0)
            self.fileInfoWidget.setRowCount(0)
            self.allFileInfoArray.clear()
            self.sha1ProgressBar.setValue(0)

    def getAllSha1(self):
        self.sha1ProgressBar.show()
        if len(self.fileListWidget.getAllFileListArray()) == 1 and self.fileListWidget.getAllFileListArray()[
            0].suffix == '.sha':
            self.sha1ProgressBar.setValue(0)
            self.fileInfoWidget.setColumnCount(3)
            self.fileInfoWidget.setHorizontalHeaderLabels(['校验是否成功', '文件名', 'SHA1校验码'])
            getShaFileContent = self.readFile(self.fileListWidget.getAllFileListArray()[0])
            progressStep = int(100 / len(getShaFileContent))
            for eachFileSha1 in getShaFileContent:
                tempSha1 = eachFileSha1.split(' *')[0]
                tempFileName = eachFileSha1.split(' *')[1]
                if not Path.exists(Path(tempFileName)):
                    tempFileName = str(self.fileListWidget.getAllFileListArray()[0].parent.joinpath(tempFileName))
                print(Path(tempFileName))
                print(Path(tempFileName).name)
                print(str(Path(tempFileName).name) == str(Path(tempFileName)))
                if str(Path(tempFileName)) == str(Path(tempFileName).name):
                    if self.getSha1(self.fileListWidget.getAllFileListArray()[0].parent.joinpath(tempFileName)) == tempSha1:
                        rowCount = self.fileInfoWidget.rowCount()
                        self.fileInfoWidget.insertRow(self.fileInfoWidget.rowCount())
                        self.fileInfoWidget.setItem(rowCount, 0, QTableWidgetItem('校验成功'))
                        print('1')
                        self.fileInfoWidget.setItem(rowCount, 1, QTableWidgetItem(tempFileName))
                        self.fileInfoWidget.setItem(rowCount, 2, QTableWidgetItem(tempSha1))
                    else:
                        rowCount = self.fileInfoWidget.rowCount()
                        self.fileInfoWidget.insertRow(self.fileInfoWidget.rowCount())
                        print('2')
                        self.fileInfoWidget.setItem(rowCount, 0, QTableWidgetItem('!!校验失败'))
                        self.fileInfoWidget.setItem(rowCount, 1, QTableWidgetItem(tempFileName))
                        self.fileInfoWidget.setItem(rowCount, 2, QTableWidgetItem(tempSha1))
                else:
                    if self.getSha1(tempFileName) == tempSha1:
                        rowCount = self.fileInfoWidget.rowCount()
                        self.fileInfoWidget.insertRow(self.fileInfoWidget.rowCount())
                        self.fileInfoWidget.setItem(rowCount, 0, QTableWidgetItem('校验成功'))
                        self.fileInfoWidget.setItem(rowCount, 1, QTableWidgetItem(tempFileName))
                        self.fileInfoWidget.setItem(rowCount, 2, QTableWidgetItem(tempSha1))
                    else:
                        rowCount = self.fileInfoWidget.rowCount()
                        self.fileInfoWidget.insertRow(self.fileInfoWidget.rowCount())
                        self.fileInfoWidget.setItem(rowCount, 0, QTableWidgetItem('!!校验失败'))
                        self.fileInfoWidget.setItem(rowCount, 1, QTableWidgetItem(tempFileName))
                        self.fileInfoWidget.setItem(rowCount, 2, QTableWidgetItem(tempSha1))

                self.sha1ProgressBar.setValue(progressStep)
            self.sha1ProgressBar.setValue(100)
            self.fileInfoWidget.resizeColumnsToContents()
        else:
            self.sha1ProgressBar.setValue(0)
            self.fileInfoWidget.setColumnCount(9)
            self.fileInfoWidget.setHorizontalHeaderLabels(
                ['文件名', 'SHA1校验码', '文件类型', '文件大小', '修改时间', '是否加密', '压缩包内文件数量', '压缩包内文件夹数量', '扩展名对应的文件数量'])
            progressStep = int(100 / (len(self.fileListWidget.getAllFileListArray()) - self.fileInfoWidget.rowCount()))
            for i in range(self.fileInfoWidget.rowCount(), len(self.fileListWidget.getAllFileListArray())):
                self.fileInfoWidget.insertRow(self.fileInfoWidget.rowCount())
                eachFilePath = self.fileListWidget.getAllFileListArray()[i]
                dirCount = 0
                fileCount = 0
                fileType = {}
                tempFileType = ''

                isEncrypted = False
                if zipfile.is_zipfile(eachFilePath):
                    zf = zipfile.ZipFile(eachFilePath)
                    for eachFile in zf.infolist():
                        isEncrypted = eachFile.flag_bits & 0x1 
                        if eachFile.is_dir():
                            dirCount = dirCount + 1
                        else:
                            fileCount = fileCount + 1
                            if Path(eachFile.filename).suffix not in fileType:
                                fileType[Path(eachFile.filename).suffix] = 1
                            else:
                                fileType[Path(eachFile.filename).suffix] = fileType[Path(eachFile.filename).suffix] + 1
                    zf.close()
                if rarfile.is_rarfile(eachFilePath):
                    rf = rarfile.RarFile(eachFilePath)
                    isEncrypted = rf.needs_password()
                    for eachFile in rf.infolist():
                        if eachFile.is_dir():
                            dirCount = dirCount + 1
                        else:
                            fileCount = fileCount + 1
                            if Path(eachFile.filename).suffix not in fileType:
                                fileType[Path(eachFile.filename).suffix] = 1
                            else:
                                fileType[Path(eachFile.filename).suffix] = fileType[Path(eachFile.filename).suffix] + 1
                    rf.close()
                for key in sorted(fileType):
                    tempFileType = tempFileType + key[1:] + '=' + str(fileType[key]) + ', '
                if tempFileType == '':
                    tempFileType = '非压缩包压缩'
                if not rarfile.is_rarfile(eachFilePath) and not zipfile.is_zipfile(eachFilePath):
                    dirCount = '非压缩包'
                    fileCount = '非压缩包'
                tmpSha1 = self.getSha1(eachFilePath)

                self.fileInfoWidget.setItem(i, 0, QTableWidgetItem(eachFilePath.name))
                self.fileInfoWidget.setItem(i, 1, QTableWidgetItem(tmpSha1))
                self.fileInfoWidget.setItem(i, 2, QTableWidgetItem(eachFilePath.suffix[1:]))
                self.fileInfoWidget.setItem(i, 3, QTableWidgetItem((self.formatFileSize(eachFilePath.stat().st_size))))
                self.fileInfoWidget.setItem(i, 4, QTableWidgetItem(
                    datetime.datetime.fromtimestamp(eachFilePath.stat().st_mtime).strftime('%Y-%m-%d %H:%M:%S')))
                if isEncrypted:
                    self.fileInfoWidget.setItem(i, 5, QTableWidgetItem('是'))
                else:
                    self.fileInfoWidget.setItem(i, 5, QTableWidgetItem('否'))
                self.fileInfoWidget.setItem(i, 6, QTableWidgetItem(str(fileCount)))
                self.fileInfoWidget.setItem(i, 7, QTableWidgetItem(str(dirCount)))
                self.fileInfoWidget.setItem(i, 8, QTableWidgetItem(tempFileType[:-2]))
                self.fileInfoWidget.setItem(i, 9, QTableWidgetItem(tmpSha1))

                eachFileInfoArray = []
                if self.fileListWidget.getIfFirstDrop():
                    eachFileInfoArray.append(str(eachFilePath.relative_to(self.fileListWidget.getFirstDropDir())))
                else:
                    eachFileInfoArray.append(str(eachFilePath))
                eachFileInfoArray.append(tmpSha1)
                eachFileInfoArray.append(eachFilePath.suffix[1:])
                eachFileInfoArray.append((self.formatFileSize(eachFilePath.stat().st_size)))
                eachFileInfoArray.append(
                    datetime.datetime.fromtimestamp(eachFilePath.stat().st_mtime).strftime('%Y-%m-%d %H:%M:%S'))     
                if isEncrypted:
                    eachFileInfoArray.append('是')
                else:
                    eachFileInfoArray.append('否')
                eachFileInfoArray.append(str(fileCount))
                eachFileInfoArray.append(str(dirCount))
                eachFileInfoArray.append(tempFileType[:-2])
                self.allFileInfoArray.append(eachFileInfoArray)
                self.sha1ProgressBar.setValue(self.sha1ProgressBar.value() + progressStep)
            self.sha1ProgressBar.setValue(100)
            self.fileInfoWidget.resizeColumnsToContents()
        self.sha1ProgressBar.close()

    def formatFileSize(self, sizeBytes):
        # 格式化文件大小
        sizeBytes = float(sizeBytes)
        result = float(abs(sizeBytes))
        suffix = "B"
        if (result > 1024):
            suffix = "KB"
            mult = 1024
            result = result / 1024
        if (result > 1024):
            suffix = "MB"
            mult *= 1024
            result = result / 1024
        if (result > 1024):
            suffix = "GB"
            mult *= 1024
            result = result / 1024
        if (result > 1024):
            suffix = "TB"
            mult *= 1024
            result = result / 1000
        if (result > 1024):
            suffix = "PB"
            mult *= 1024
            result = result / 1024
        return format(result, '.2f') + suffix

    def getSha1(self, filePath):
        # 计算sha1
        sha1Obj = sha1()
        try:
            with open(filePath, 'rb') as f:
                sha1Obj.update(f.read())
        except FileNotFoundError:
            print(str(filePath) + '文件不存在')
        return sha1Obj.hexdigest()

    def writeFile(self, suffix, filereadlines):
        if self.fileListWidget.getIfFirstDrop():
            newfile = open(str(self.fileListWidget.getAllFileListArray()[0].parent.joinpath(
                self.fileListWidget.getAllFileListArray()[0].parent.name)) + ' ' + time.strftime("%Y%m%d", time.localtime()) + '.' + suffix, mode='w', encoding='UTF-8')
        else:
            newfile = open(str(Path.cwd()) + '\\' + Path.cwd().name + ' ' + time.strftime("%Y%m%d", time.localtime()) + '.' + suffix, mode='w', encoding='UTF-8')
        newfile.writelines(filereadlines)
        newfile.close()

    def readFile(self, filePath):
        # 读取文件
        try:
            with open(filePath, mode='r', encoding='UTF-8') as file:
                filereadlines = file.readlines()
            for i in filereadlines:
                # 去掉空行
                if i == '\n':
                    filereadlines.remove(i)
            # remove '\n' in line end
            for i in range(len(filereadlines)):
                filereadlines[i] = filereadlines[i].rstrip()
            return filereadlines
        except UnicodeDecodeError:
            with open(filePath, mode='r', encoding='ANSI') as file:
                filereadlines = file.readlines()
            for i in filereadlines:
                # 去掉空行
                if i == '\n':
                    filereadlines.remove(i)
            # remove '\n' in line end
            for i in range(len(filereadlines)):
                filereadlines[i] = filereadlines[i].rstrip()
            return filereadlines
        except FileNotFoundError:
            print(str(filePath) + '文件不存在')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mywidget = MyQWidget()
    mywidget.show()
    sys.exit(app.exec_())
