import os
import json 
import threading
import time
#时间戳转年月日
def TimeStampToTime(timestamp):
    timeStruct = time.localtime(timestamp)
    return time.strftime('%Y-%m-%d %H:%M:%S',timeStruct)
#初始化服务
#获取用户名
userName = os.popen("whoami").read()
userName = userName.split("\\")[1].strip()
#获取桌面所在目录
desktopPath = "C:\\Users\\%s\\Desktop" %userName
print(desktopPath)
#获取配置文件
configFile = open("D:\\Cleaner\\config.json",'r')
config = json.loads(configFile.read())
checkTime = config["checkTime"]
outdatedTime = config["outdatedTime"]
isDelete = config["isDelete"]
isUploadLog = config["isUploadLog"]
#获取文件白名单
whiteListFile = open("D:\\Cleaner\\whitelist.txt",'r').read()
whiteList = whiteListFile.split("\n")
#获取白名单数组最后一个值是否为空，如果是则删除最后一个值
if(whiteList[len(whiteList)-1] == ""):
    whiteList.pop(len(whiteList)-1)
#获取完成，记录日志后进入定期扫描
path = os.getcwd()
log = open("D:\\Cleaner\\logs.txt","w")
initTimeStamp = time.time()
initTime = TimeStampToTime(initTimeStamp)
log.write("%s init service success" % initTime)
#定期扫描
def scan():
    #创建字典
    fileTimeName = {}
    #获取全部文件名
    files = os.listdir(desktopPath)
    #获取全部文件更改时间
    for i in files:
        fileTime = (os.path.getatime(desktopPath+"\\"+i))
        fileTimeName[i] = int(fileTime)
    #将字典写入文件
    fileJson = json.dumps(fileTimeName)
    with open('D:\\Cleaner\\file.json', 'w') as json_file:
        json_file.write(fileJson)
    #记录日志
    log.write("%s scan success" % initTime)
    #新建线程
    timer = threading.Timer(checkTime*60,scan)
    timer.start()
def checkTimedOut():
    #获取文件列表
    fileJson = open("D:\\Cleaner\\file.json",'r').read()
    fileTimeName = json.loads(fileJson)
    #创建列表
    outdatedFile = []
    for key,value in fileTimeName.items():
        if(int(time.time()) - value >= 86400):
            outdatedFile.append(key)
    #删除文件
    #是否为空数组，为空则不进行删除操作
    if(outdatedFile):
        for i in outdatedFile:
            #是否直接删除文件
            if(isDelete):
                os.remove(desktopPath+"\\"+i)
            else:
                #移动文件至回收站
                os.system("move %s\\%s D:\\Cleaner\\recycle"%(desktopPath,i))
        #记录日志
        log.write("%s remove %s file success"%(initTime,len(outdatedFile)))
        timer = threading.Timer(checkTime*60,checkTimedOut)
        timer.start()
scan()
checkTimedOut()