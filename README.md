## 说明

使用PyQt5编写，生成exe，请运行pyinstaller -F 程序.py

需要pip install pyinstaller

部分脚本命令行版[https://github.com/wangandi520/andyspythonscript](https://github.com/wangandi520/andyspythonscript)

## 各种class用法

from 文件名 import class名，例如from classandysFileListWidget import andysFileListWidget

预览class效果，打开py文件把if __name__ 行下面的注释取消

### classandysFileListWidget.py

实现打开或拖拽文件加入到列表。拖拽文件夹会把里面的所有文件加入到列表。按钮可删除和清空。

## 老王简繁转换器

支持拖拽文件到程序中，可同一个文件多次改名

需要pip install pyqt5 pyqt5-tools pypinyin opencc-python-reimplemented

## 老王随机点名器

选取姓名按钮快捷键：空格，缺席按钮快捷键：B。

需要 pip install pyqt5 pyqt5-tools pandas openpyxl

**1.1版更新：**
支持xls,xlsx

**1.0版更新：**
改用PyQt5重写
暂时不支持xls文件

**0.42版更新：**
更新捐赠二维码

**0.41版更新：**
添加速度调节
修复bug
可快速捐赠

**0.4版更新：**
支持模板的xls文件

**0.3版更新：**
支持多文件同时选取
增加了重置列表按钮
更改了文件切换时重新读取文件的设计
修改缺席名单的命名方式
添加缺席按钮
修正取消打开文件而添加文件的错误

**0.2版更新：**
修正了时间闪烁的问题
修改状态栏显示
增加打开文件后自动选择的功能
增加了字体大小调节
调整了内部设计，修复了剩余数量显示错误
修复文件删除后仍能点名的错误
添加清空列表按钮

### 老王扩展名修改器=db3_rar.pyw

使用PyQt5编写

可以拖拽文件或文件夹，文件夹内所有符合条件的文件都会生效

文件后面的=py_pyw可以让程序读取，格式：=原扩展名_新扩展名

## 作者：Andy
