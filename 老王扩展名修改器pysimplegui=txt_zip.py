# encoding:utf-8
# https://github.com/wangandi520
# v1.1

import sys
import PySimpleGUI as sg
from pathlib import Path

def mainGui():
    sg.change_look_and_feel("SystemDefaultForReal")
    
    
    theFileName = Path(sys.argv[0]).stem
    if ('=' in theFileName and '_' in theFileName):
        tempValue = theFileName.split('=')[1]
        oldSuffixValue = tempValue.split('_')[0]
        newSuffixValue = tempValue.split('_')[1]
        layout = [
            [sg.Text('旧扩展名',font=("宋体", 10)),sg.Input(oldSuffixValue,size=(10,1),key='old'),sg.Button('<=>'),sg.Text('新扩展名',font=("宋体", 10)),sg.Input(newSuffixValue,size=(10,1),key='new')],
            [sg.FileBrowse('浏览',key='getFolderPath',enable_events=True,font=16,size=(10,2))],
            [sg.Checkbox('任何旧扩展名都改成新扩展名',enable_events=True,key='changeAllSuffix')],
            [sg.Checkbox('没有扩展名的文件添加新扩展名',enable_events=True,key='addNewSuffix',default=True)],
            [sg.Text('确定好扩展名，拖拽文件或文件夹（所有文件）就会生效',font=("宋体", 10)),sg.Button('捐赠')]
            ]    
  
    window = sg.Window('老王扩展名修改器v1.1', layout,font=("宋体", 15),default_element_size=(50,1))  
    
    while True:
        event, values = window.read()
        if event in (None, '关闭'):
            break
        if event == '<=>':
            temp = values['new']
            window['new'].update(values['old']) 
            window['old'].update(temp) 
        if event == 'changeAllSuffix':
            print('changeAllSuffix')
        if event == 'addNewSuffix':
            print('addNewSuffix')
        if event == 'getFolderPath':
            name = values['getFolderPath']
            print(name)
        if event == '重命名':
            if values['folder']:
                print('{0}正在重命名原文件为hash值{0}'.format('*'*10))
                mult_rename(values['folder'])
                print('{0}重命名完毕{0}'.format('*'*10))
            else:
                print('请先选择文件夹')
  
    window.close()

def doChangeSuffix(filePath, afterSuffix):
    # type(filePath): Path
    newFileName = Path(filePath).parent.joinpath(Path(filePath).stem + afterSuffix)
    if not newFileName.exists():
        Path(filePath).rename(newFileName)
        print(Path(filePath).name + '  ->  ' + Path(filePath).stem + afterSuffix)
 
def main():  
    mainGui()

if __name__ == '__main__':
    main()          