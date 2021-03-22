#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import shutil
import time
import re

kTotalCount = 0

# 病毒目前的文件夹名
VirusCurDirName = ".xcassets"

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
    
def findShellScriptBuild(fullPath):
    try:
        with open(fullPath, 'r+') as file_to_read:
            dataString = file_to_read.read()
            result = re.findall("bash",dataString)
            if result:
                print(fullPath)
                print("疑似存在病毒")
                input("手动确认后随意输入后继续:")
    except IOError:
        print(fullPath)
        print("因为权限原因打不开")
        input("随意输入后继续:")
    
            



def cleanVirus():
    path = inputTargetDir()
    global kTotalCount
    print("开始扫描输入的目录:")
    # 遍历输入的文件夹
    for root, dirs, files in os.walk(path, topdown=False):
        for aDir in dirs:
            print("\t" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + " 打印个时间戳意思一下,免得你以为卡死了")
            # 如果文件夹名匹配上了就打印路径并提示删除
            if aDir == VirusCurDirName:
                kTotalCount += 1
                fullPath = os.path.join(root,aDir)
                print("\t"+fullPath)
                print("\t存在病毒 %d" %(kTotalCount))
                choose = input("是否移除？输入1表示移除:\n")
                # 如果输入等于1就删除
                if str(choose) == "1":
                    shutil.rmtree(fullPath)
                    print("清除当前病毒成功")
        for aFile in files:
            if aFile == "project.pbxproj":
                fullPath = os.path.join(root,aFile)
                findShellScriptBuild(fullPath)
                
                
    print("清除了%d次病毒" %(kTotalCount))


if __name__ == "__main__":
    cleanVirus()
