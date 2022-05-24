#!/usr/bin/python
# -*- coding: UTF-8 -*-
# 开发者公众号: iOS过审技术

import os
import shutil
import time
import re
import codecs

kTotalCount = 0


kProjectFile = "project.pbxproj" # 

# 获取需要扫描的文件夹路径
def inputTargetDir():
    path = input("请输入需要清理的目录:\n")
    # 移除输入路径右边的空格
    path = path.rstrip()
    # 判断输入的路径是否存在
    if not os.path.exists(path):
        print("输入的路径不存在")
        path = input("请重新输入需要清理的目录:\n")
        path = path.rstrip()
    return path


# 16进制转ascii
def hexToAscii(b):
    binary_str = codecs.decode(b, "hex")
    return str(binary_str,'utf-8')


# 找病毒
def findShellScriptBuild(fullPath):
    try:
        with open(fullPath, 'r+') as file_to_read:
            dataString = file_to_read.read()
            
        results = re.findall("shellScript = (.*?);",dataString,re.S)
        for aResult in results:
            # 病毒肯定需要使用到xxd
            if "xxd" not in aResult:
                continue

            print("\t" + fullPath)
            print("\t存在加密后的病毒:")
            print("\t" + aResult)

            aResult = aResult.replace("\\","")
            virus = re.findall('echo "(.*?)"',aResult,re.S)
            if len(virus) == 0:
                continue

            realVirus = ""

            curVirus = virus[0]
            curVirusList = curVirus.split("\n")
            for partyVirus in curVirusList:
                realVirus += hexToAscii(partyVirus)
            print("\t16进制转ascii后的真实病毒:" + realVirus)

            # VirusDomian = re.findall(r"http[s]?://(S+)", realVirus)
            # print("\t病毒域名:")
            # print(VirusDomian)
            input("手动确认后随意输入后继续:")
                    
    except IOError:
        print(fullPath)
        print("因为权限原因打不开")
        input("随意输入后继续:")



# def restore(fullPath):
#     targetString = "6375726c202d2d6d61782d74696d652035202d736b2068747470733a2f2f"
#     command = "sed -i 's/%s//g' %s" %(targetString,fullPath)
#     os.system(command)
#     try:
#         with open(fullPath, 'r+') as file_to_read:
#             print("恢复后")
#             dataString = file_to_read.read()
#             print(dataString)
#     except IOError:
#         print(fullPath)
#         print("因为权限原因打不开")
#         input("随意输入后继续:")



# 恢复被病毒注入的部分
# def cleanInject():
#     path = inputTargetDir()
#     global kTotalCount
#     print("开始清理输入的目录:")
#     for root, dirs, files in os.walk(path, topdown=False):
#         for aFile in files:
#             if aFile == "111.rtf": #project.pbxproj
#                 kTotalCount += 1
#                 fullPath = os.path.join(root,aFile)
#                 print("清理文件:%s" %(fullPath))
#                 restore(fullPath)


def cleanVirus():
    path = inputTargetDir()
    global kTotalCount
    print("开始扫描输入的目录:")
    # 遍历输入的文件夹
    for root, dirs, files in os.walk(path, topdown=False):
        for aFile in files:
            fullPath = os.path.join(root,aFile)
            print("\t" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + " 打印个时间戳意思一下,免得你以为卡死了")
            if aFile == kProjectFile: 
                fullPath = os.path.join(root,aFile)
                findShellScriptBuild(fullPath)
    print("清除了%d次病毒" %(kTotalCount))


if __name__ == "__main__":
    cleanVirus() #这是清理病毒的方法，#号是python的注释符