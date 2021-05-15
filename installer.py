import os
import requests
import json
#版本号
version = "100"
#第一次启动准备
def init():
    #检测更新，如果有更新则提醒
    try:
        latest = requests.get("http://api.blackblaze.cn/cleaner_latest").text
        if(latest > version):
            print("有最新版本，请前往https://hub.fastgit.org/zhishixiang/Desktop-Cleaner/releases下载")
    except:
        pass
    #检测有没有文件夹，如果没有就开始安装
    folder = os.path.exists("D:\\Cleaner")
    if not folder:
        print("欢迎使用桌面清理带师")
        input("是否安装本程序？继续安装请按enter，退出安装请按ctrl+c")
        print("正在创建安装目录")
        os.makedirs("D:\\Cleaner")
    else:
        print("已安装本程序，请勿重复安装！")
        input("按下enter以退出安装")
        assert()
    #创建日志文件
    print("创建日志文件中")
    file = open('D:\\Cleaner\\logs.txt','w')
    file.close
    #创建文件时间记录
    print("创建文件时间记录中")
    file = open('D:\\Cleaner\\file.json','w')
    file.close
    print("创建文件白名单中")
    file = open('D:\\Cleaner\\whitelist.txt','w')
    file.write("desktop.ini\n")
    file.close
    #创建配置文件
    file = open('D:\\Cleaner\\config.json','w')
    file.close
    #复制本文件至安装目录
    path = os.getcwd()
    print("复制主程序中")
    os.system('copy %s\\Service.py D:\\Cleaner\\Service.py'%(path))
    os.system('copy %s\\Panel.py D:\\Cleaner\\Panel.py'%(path))
    os.system('copy %s\\start_cleaner.exe D:\\Cleaner\\start_cleaner.exe'%(path))
    os.system('copy %s\\start_cleaner.xml D:\\Cleaner\\start_cleaner.xml'%(path))
    #向api报告安装完成(仅做统计用途)
    try:
        requests.get("http://api.blackblaze.cn/cleaner_install?&ver=%s"%version)
    except:
        pass
    #安装完成
    print("安装完成，进入配置向导")
    os.system("cls")
    config()
def config():
    print("欢迎进入桌面清理带师配置向导")
    print("请输入数字或者y/n配置")
    print("请注意单位，否则后果自负")
    #配置选项
    checkTimeInput = input("您希望多少分钟检查一次文件是否过期？默认为60 ")
    if(checkTimeInput == ""):
        checkTime = 60
    else:
        checkTime = checkTimeInput
    outdatedTimeInput = input("您希望多少天为文件过期时间？默认为7天 ")
    if(outdatedTimeInput == ""):
        outdatedTime = 7
    else:
        outdatedTime = outdatedTimeInput
    if(input("是否直接删除过期的文件？ y/n 默认为n") == "y"):
        isDelete = True
    else:
        isDelete = False
        #在目录下创建回收站
        os.mkdir("D:\\Cleaner\\recycle")
    isLaunchWithBootInput = input("是否开机启动？ y/n 默认为y")
    if(isLaunchWithBootInput == "" or isLaunchWithBootInput == "y"):
        isLaunchWithBoot = True
        os.system("D:/Cleaner/start_cleaner install")
    else:
        isLaunchWithBoot = False
    isUploadLogInput = input("是否上传日志文件以改进我们的程序？我们不会提供您的数据给任何第三方 y/n 默认为y")
    if(isUploadLogInput == "" or isUploadLogInput == "y"):
        isUploadLog = True
    else:
        isUploadLog = False
    #写入文件
    print("正在写入配置文件")
    configFile = open("D:\\Cleaner\\config.json")
    config = json.dumps({'checkTime':checkTime,'outdatedTime':outdatedTime,'isDelete':isDelete,"isLaunchWithBoot":isLaunchWithBoot,'isUploadLog':isUploadLog})
    with open('D:\\Cleaner\\config.json', 'w') as json_file:
        json_file.write(config)
    #结束安装
    input("配置完成，按enter退出配置向导")
init()

