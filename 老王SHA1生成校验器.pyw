# encoding:utf-8
# https://github.com/wangandi520

import sys
import zipfile
import rarfile
import datetime

from opencc import OpenCC
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout, QLabel, QLineEdit, QPushButton, QRadioButton, QTableWidget, QTableWidgetItem, QHeaderView
from PyQt5.QtCore import QSize, QUrl
from pypinyin import pinyin, lazy_pinyin, Style
from pathlib import Path
from hashlib import sha1
from classandysFileListWidget import andysFileListWidget

# pip install pyqt5 pyqt5-tools pypinyin opencc-python-reimplemented

class MyQWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('老王SHA1生成校验器v1.0')
        self.fileListWidget = andysFileListWidget()
        self.fileInfoWidget = QTableWidget()
        self.allFileInfoArray = []
        
        leftLayout = QHBoxLayout()
        rightLayout = QVBoxLayout()
        rightTopLayout = QHBoxLayout()
        outputTLayout = QHBoxLayout()
        outputSLayout = QHBoxLayout()
        outputLetterLayout = QHBoxLayout()
        outputFirstLetterLayout = QHBoxLayout()
        mainLayout = QHBoxLayout()
        
        
        self.toHtmlButton = QPushButton('输出Html')
        self.toMarkdownButton = QPushButton('输出Markdown')
        self.toSha1Button = QPushButton('输出Sha1')
        # self.outputLetterButton = QPushButton('字母')
        # self.outputFirstLetterButton = QPushButton('首字母')
        
        # self.inputLineEdit = QLineEdit()
        # self.outputTLineEdit = QLineEdit()
        # self.outputSLineEdit = QLineEdit()
        # self.outputLetterLineEdit = QLineEdit()
        # self.outputFirstLetterLineEdit = QLineEdit()
        self.setMinimumSize(1400, 600)
        #self.setMinimumWidth(1100)
        self.setAcceptDrops(True)

        # 事件
        self.fileListWidget.fileListChangedSignal.connect(self.fileListChangedSlot)
        #self.fileListWidget.currentRowChangedSignal.connect(self.currentRowChangedSlot)
        # self.inputLineEdit.textChanged.connect(self.convertText)
        # self.oldNameButton.clicked.connect(self.doOldNameText)
        self.toHtmlButton.clicked.connect(self.toHtmlSlot)
        self.toMarkdownButton.clicked.connect(self.toMarkdownSlot)
        self.toSha1Button.clicked.connect(self.toSha1Slot)
        # self.outputSButton.clicked.connect(self.doOutputSText)
        # self.outputLetterButton.clicked.connect(self.doOutputLetterText)
        # self.outputFirstLetterButton.clicked.connect(self.doOutputFirstLetterText)
        
        # Layout设置
   
        leftLayout.addWidget(self.fileListWidget)
        rightTopLayout.addWidget(self.toHtmlButton)
        rightTopLayout.addWidget(self.toMarkdownButton)
        rightTopLayout.addWidget(self.toSha1Button)
        rightLayout.addLayout(rightTopLayout)
        rightLayout.addWidget(self.fileInfoWidget)
        mainLayout.addLayout(leftLayout)
        mainLayout.addLayout(rightLayout)
        mainLayout.setStretchFactor(leftLayout, 1)
        mainLayout.setStretchFactor(rightLayout, 4)
        self.setLayout(mainLayout)    
            
    def toHtmlSlot(self):
        # 转换成html格式
        returnFileInfo = []
        returnFileInfo.append('<html><head><title>文件信息</title><style>table{width:auto;}table,td{border:1px solid #000000;table-layout:fixed;border-collapse:collapse;}table td:first-child{width:auto;}table td{min-width:100px;}a{text-decoration: none;}table tr:first-child{background-color:#eee;}tr:hover{background-color:#eee;}</style></head><body><table id="allFileTable"><tr><td>文件夹名</td><td>文件类型</td><td>文件大小</td><td>修改时间</td><td>压缩包内文件数量</td><td>压缩包内文件夹数量</td><td>扩展名对应的文件数量</td><td>SHA1校验码</td></tr>')
        
        for eachInfo in self.allFileInfoArray:
            newContent = '<tr>'
            for eachString in eachInfo:
                newContent = newContent + '<td>' + str(eachString) + '</td>'
            returnFileInfo.append(newContent + '</tr>')
        returnFileInfo.append('</table></body></html>')
        self.writeFile('html', returnFileInfo)
    
    def toMarkdownSlot(self):
        # 转换成markdown格式
        returnFileInfo = []
        returnFileInfo.append('|文件夹名|文件类型|文件大小|修改时间|压缩包内文件数量|压缩包内文件夹数量|扩展名对应的文件数量|SHA1校验码|\n')
        returnFileInfo.append('| --- | --- | --- | --- | --- | --- | --- | --- |\n')
        
        for eachInfo in self.allFileInfoArray:
            newContent = '|'
            for eachString in eachInfo:
                newContent = newContent + str(eachString) + '|'
            returnFileInfo.append(newContent + '\n')
        self.writeFile('md', returnFileInfo)
    
    def toSha1Slot(self):
        returnFileInfo = []
        for eachInfo in self.allFileInfoArray:
            newContent = ''
            newContent = newContent + eachInfo[0] + ' ' + eachInfo[7] + '\n'
            returnFileInfo.append(eachInfo[7] + ' *' + eachInfo[0] + '\n')
        self.writeFile('sha1', returnFileInfo)
    
    
    def fileListChangedSlot(self):
        fileListCount = len(self.fileListWidget.getAllFileListArray())
        if (fileListCount == 1 and Path(self.fileListWidget.getAllFileListArray()[0]).suffix == '.sha'):
            self.fileInfoWidget.setColumnCount(3)
            self.fileInfoWidget.setHorizontalHeaderLabels(['校验是否成功','文件名','SHA1校验码'])
            self.fileInfoWidget.resizeColumnsToContents()
        elif (fileListCount == 0):
            self.fileInfoWidget.clear()
            self.fileInfoWidget.setColumnCount(0)
            self.fileInfoWidget.setRowCount(0)
            self.allFileInfoArray.clear()
        else:
            self.fileInfoWidget.setColumnCount(8)
            self.fileInfoWidget.setHorizontalHeaderLabels(['文件名','文件类型','文件大小','修改时间','压缩包内文件数量','压缩包内文件夹数量','扩展名对应的文件数量','SHA1校验码'])
            for i in range(self.fileInfoWidget.rowCount(), len(self.fileListWidget.getAllFileListArray())):
                self.fileInfoWidget.insertRow(self.fileInfoWidget.rowCount())
                eachFilePath = self.fileListWidget.getAllFileListArray()[i]
                dirCount = 0
                fileCount = 0
                fileType = {}
                tempFileType = ''
                
                if zipfile.is_zipfile(eachFilePath):
                    zf = zipfile.ZipFile(eachFilePath)
                    for eachFile in zf.infolist():
                        if eachFile.is_dir():
                            dirCount = dirCount + 1
                        else:
                            fileCount = fileCount + 1
                            if (Path(eachFile.filename).suffix not in fileType):
                                fileType[Path(eachFile.filename).suffix] = 1
                            else:
                                fileType[Path(eachFile.filename).suffix] = fileType[Path(eachFile.filename).suffix] + 1
                    zf.close()
                if rarfile.is_rarfile(eachFilePath):
                    rf = rarfile.RarFile(eachFilePath)
                    for eachFile in rf.infolist():
                        if eachFile.is_dir():
                            dirCount = dirCount + 1
                        else:
                            fileCount = fileCount + 1
                            if (Path(eachFile.filename).suffix not in fileType):
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
                self.fileInfoWidget.setItem(i, 1, QTableWidgetItem(eachFilePath.suffix[1:]))
                self.fileInfoWidget.setItem(i, 2, QTableWidgetItem((self.formatFileSize(eachFilePath.stat().st_size))))
                self.fileInfoWidget.setItem(i, 3, QTableWidgetItem(datetime.datetime.fromtimestamp(eachFilePath.stat().st_mtime).strftime('%Y-%m-%d %H:%M:%S')))
                self.fileInfoWidget.setItem(i, 4, QTableWidgetItem(str(fileCount)))
                self.fileInfoWidget.setItem(i, 5, QTableWidgetItem(str(dirCount)))
                self.fileInfoWidget.setItem(i, 6, QTableWidgetItem(tempFileType[:-2]))
                self.fileInfoWidget.setItem(i, 7, QTableWidgetItem(tmpSha1))
                
                eachFileInfoArray = []
                eachFileInfoArray.append(str(eachFilePath))
                eachFileInfoArray.append(eachFilePath.suffix[1:])
                eachFileInfoArray.append((self.formatFileSize(eachFilePath.stat().st_size)))
                eachFileInfoArray.append(datetime.datetime.fromtimestamp(eachFilePath.stat().st_mtime).strftime('%Y-%m-%d %H:%M:%S'))
                eachFileInfoArray.append(str(fileCount))
                eachFileInfoArray.append(str(dirCount))
                eachFileInfoArray.append(tempFileType[:-2])
                eachFileInfoArray.append(tmpSha1)
                self.allFileInfoArray.append(eachFileInfoArray)
                #eachFileInfo.append(str(filePath.relative_to(directoryPath)))
                #print(str(eachFilePath.relative_to(eachFilePath)))
                #eachFileInfo.append(filePath.suffix[1:])
                #eachFileInfo.append(formatFileSize(filePath.stat().st_size))
                #eachFileInfo.append(datetime.datetime.strptime(filePath.stat().st_mtime, "%Y-%m-%d %H:%M:%S.%f"))
                # eachFileInfo.append(datetime.datetime.fromtimestamp(filePath.stat().st_mtime).strftime('%Y-%m-%d %H:%M:%S'))
                
                # eachFileInfo.append(fileCount)
                # eachFileInfo.append(dirCount)
                # tempFileType = ''
                
                # eachFileInfo.append(tempFileType[:-2])
                # eachFileInfo.append(getSha1(filePath))
                
                # dirCount = 0
                # fileCount = 0
                # fileType = {}

                # print(self.formatFileSize(eachFile.stat().st_size))
                # print(type(self.formatFileSize(eachFile.stat().st_size)))
            
            self.fileInfoWidget.resizeColumnsToContents()
            #self.fileInfoWidget.insertRow(0, 0, QTableWidgetItem(self.fileListWidget.getAllFileListArray()[i].name))
            # print(self.fileInfoWidget.item(0,0).text())
        
    def formatFileSize(self, sizeBytes):
    # 格式化文件大小
        sizeBytes = float(sizeBytes)
        result = float(abs(sizeBytes))
        suffix = "B"
        if(result > 1024):
            suffix = "KB"
            mult = 1024
            result = result / 1024
        if(result > 1024):
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
        print(str(Path.cwd()) + '\\' + Path.cwd().name + '.' + suffix)
        newfile = open(str(Path.cwd()) + '\\' + Path.cwd().name + '.' + suffix, mode='w', encoding='UTF-8')
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
        except FileNotFoundError:
            print(str(filePath) + '文件不存在')
      
    def getFileInfo(self, directoryPath, filePath):
        # Path(filePath)
        eachFileInfo = []
        dirCount = 0
        fileCount = 0
        fileType = {}
        
        if zipfile.is_zipfile(filePath):
            zf = zipfile.ZipFile(filePath)
            for eachFile in zf.infolist():
                if eachFile.is_dir():
                    dirCount = dirCount + 1
                else:
                    fileCount = fileCount + 1
                    if (Path(eachFile.filename).suffix not in fileType):
                        fileType[Path(eachFile.filename).suffix] = 1
                    else:
                        fileType[Path(eachFile.filename).suffix] = fileType[Path(eachFile.filename).suffix] + 1
            zf.close()
        if rarfile.is_rarfile(filePath):
            rf = rarfile.RarFile(filePath)
            for eachFile in rf.infolist():
                if eachFile.is_dir():
                    dirCount = dirCount + 1
                else:
                    fileCount = fileCount + 1
                    if (Path(eachFile.filename).suffix not in fileType):
                        fileType[Path(eachFile.filename).suffix] = 1
                    else:
                        fileType[Path(eachFile.filename).suffix] = fileType[Path(eachFile.filename).suffix] + 1
            rf.close()
            
        #eachFileInfo.append(str(filePath.parent.joinpath(filePath.name)))
        eachFileInfo.append(str(filePath.relative_to(directoryPath)))
        eachFileInfo.append(filePath.suffix[1:])
        eachFileInfo.append(formatFileSize(filePath.stat().st_size))
        #eachFileInfo.append(datetime.datetime.strptime(filePath.stat().st_mtime, "%Y-%m-%d %H:%M:%S.%f"))
        eachFileInfo.append(datetime.datetime.fromtimestamp(filePath.stat().st_mtime).strftime('%Y-%m-%d %H:%M:%S'))
        
        eachFileInfo.append(fileCount)
        eachFileInfo.append(dirCount)
        tempFileType = ''
        for key in sorted(fileType):
            tempFileType = tempFileType + key[1:] + '=' + str(fileType[key]) + ', '
        eachFileInfo.append(tempFileType[:-2])
        eachFileInfo.append(getSha1(filePath))
        print(eachFileInfo)
        return eachFileInfo
        

    def checkSha1(self, filePath):
        # 当前文件夹名内有文件夹.sha1的话，就开始校验
        fileName = ''
        getFileContent = ''
        if (Path(filePath)) == (Path.cwd()):
            getFileContent = readFile(Path.cwd().name + '.sha')
        else:
            getFileContent = readFile(Path(filePath).joinpath(Path(filePath).name + '.sha'))
        print()
        for eachFile in getFileContent:
            tempSha1 = eachFile.split(' *')[0]
            tempFileName = eachFile.split(' *')[1]
            if (getSha1(Path(filePath).joinpath(tempFileName)) == tempSha1):
                print('校验成功 ' + tempFileName)
            else:
                print('!校验失败 ' + tempFileName)

    def main(inputPath): 
        del inputPath[0]
        if (len(inputPath) == 0):
            inputPath = [Path.cwd()]
        # 所有信息
        # 每个文件的信息：|文件夹名|文件类型|文件大小|压缩包内文件数量|压缩包内文件夹数量|扩展名对应的文件数量|SHA1校验码
        allFileInfo = []
        allFileSha1 = []
        #转换成html = True, markdown = False
        fileType = True
        for aPath in inputPath:
            if Path.is_dir(Path(aPath)):
                for file in Path(aPath).glob('**/*'): 
                    if Path.is_file(Path(file)):
                        tempFileInfo = getFileInfo(Path(aPath), file)
                        allFileInfo.append(tempFileInfo)
                        allFileSha1.append(tempFileInfo[7] + ' *' + tempFileInfo[0] + '\n')  
                writeFile(Path(aPath).joinpath(Path(aPath).name + '.sha'), allFileSha1)
                if fileType:
                    writeFile(Path(aPath).joinpath(Path(aPath).name + '.html'), arrayFormatToHTML(allFileInfo))
                else:
                    writeFile(Path(aPath).joinpath(Path(aPath).name + '.md'), arrayFormatToMD(allFileInfo))
                
                sha1FileExisted = False
                for fileName in allFileInfo:
                    if (Path(aPath).name + '.sha' in fileName[0]) :
                        sha1FileExisted = True
                        break
                if sha1FileExisted:
                    checkSha1(aPath)
          
            
            if Path.is_file(Path(aPath)) and Path(aPath).suffix == '.sha':
                
                getFileContent = readFile(Path(aPath))
                
                for eachFile in getFileContent:
                    tempSha1 = eachFile.split(' *')[0]
                    tempFileName = eachFile.split(' *')[1]
                    if (getSha1(Path(aPath).parent.joinpath(tempFileName)) == tempSha1):
                        print('校验成功 ' + tempFileName)
                    else:
                        print('!校验失败 ' + tempFileName)
                        
        print()
        print('发布网址 https://github.com/wangandi520/andyspythonscript')
        input('按回车退出')
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    mywidget = MyQWidget()
    mywidget.show()
    sys.exit(app.exec_())