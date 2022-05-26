#!/usr/bin/python
# -*- coding: UTF-8 -*-
# 开发者公众号: iOS过审技术

import os
import time
import re

kTotalCount = 0


kProjectFile = "project.pbxproj"

Red = "31"
Green = "32"
Yellow = "33"


# 只是让打印酷炫一点
def colorPrint(color, log):
    print("\033[0;%s;m%s\033[0m" % (color, log))


# 获取需要扫描文件夹的路径
def inputTargetDir():
    path = input("请输入需要清理的目录,可以直接将目标文件夹拖到终端(例如:/Users/username/Desktop):\n")
    # 移除输入路径右边的空格
    path = path.rstrip()
    # 判断输入的路径是否存在
    if not os.path.exists(path):
        colorPrint(Red, "输入的路径不存在")
        path = input("请输入需要清理的目录,可以直接将目标文件夹拖到终端(例如:/Users/username/Desktop):\n")
        path = path.rstrip()
    return path


# 16进制转ascii
def hexToAscii(b):
    byte_array = bytearray.fromhex(b)
    return byte_array.decode()


# 找病毒
def findShellScriptBuild(fullPath):
    try:
        # 读取project.pbxproj文件的内容
        with open(fullPath, "r+") as file_to_read:
            dataString = file_to_read.read()

        # 通过正则获取所有shellScript = 后面的内容
        results = re.findall("[s|S]cript = (.*?);", dataString, re.S)
        for aResult in results:
            # 病毒肯定需要使用到xxd
            # aResult不包含xxd就忽略
            if "xxd" not in aResult:
                continue

            colorPrint(Yellow, "\t" + fullPath)
            colorPrint(Red, "\t存在加密后的病毒:")
            colorPrint(Yellow, "\t" + aResult)

            aResult = aResult.replace("\\", "")
            originalVirusList = re.findall('echo "(.*?)"', aResult, re.S)
            if len(originalVirusList) == 0:
                continue

            global kTotalCount
            kTotalCount += 1

            realVirus = ""

            originalVirus = originalVirusList[0]
            curVirusList = originalVirus.split("\n")
            # 把换行的16进制病毒内容转换成ascii,并且拼接
            for partyVirus in curVirusList:
                realVirus += hexToAscii(partyVirus)
            colorPrint(Red, "\t16进制转ascii后的真实病毒:" + realVirus)

            # 将文件里的原始病毒内容替换掉
            for partyVirus in curVirusList:
                restore(fullPath, partyVirus)

            # 将文件里的xxd替换掉
            restore(fullPath, "xxd")
            input("这个文件里的病毒干掉了,随意输入后即可继续清杀:")

    except IOError:
        print(fullPath)
        print("因为权限原因打不开")
        input("随意输入后继续:")


def restore(fullPath, targetString):
    command = "perl -i -pe's/%s//g' %s" % (targetString, fullPath)
    colorPrint(Green, "\t替换:%s为空" % (targetString))
    output = os.popen(command)
    string = output.read()
    output.close()


def cleanVirus():
    colorPrint(Green, "\n如有bug请联系微信公众号: iOS过审技术")
    colorPrint(Yellow, "\t本脚本只能移除项目里的病毒,如果已经中毒,建议抹掉硬盘后重装系统后使用本脚本进行一次查杀")
    path = inputTargetDir()
    global kTotalCount
    colorPrint(Yellow, "\n开始扫描输入目录:")
    # 遍历输入的文件夹
    for root, dirs, files in os.walk(path, topdown=False):
        for aFile in files:
            colorPrint(Green, "\t" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + " 打印个时间戳意思一下,免得你以为卡死了")
            if aFile == kProjectFile:
                fullPath = os.path.join(root, aFile)
                findShellScriptBuild(fullPath)
    colorPrint(Yellow, "清除了%d次病毒" % (kTotalCount))


if __name__ == "__main__":
    cleanVirus()  # 这是清理病毒的方法，#号是python的注释符
