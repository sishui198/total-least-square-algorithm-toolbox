# -*- coding: cp936 -*-
##导入模块
import os
from GetCrossPoint import GetCrossPoint

##创建总体最小二乘辅助数组，并保存成文本文件
def CreateTLSMatchingAssistTxt(SourcePath,TLSMatchingAssistPath):
    #检查是否存在同名文件
    if os.path.exists(TLSMatchingAssistPath):
       os.remove(TLSMatchingAssistPath)
    #打开文件，为读写做准备
    TLSMatchingAssistfpr= open(SourcePath,"r")
    TLSMatchingAssistfpw= open(TLSMatchingAssistPath,"w")
    for line in TLSMatchingAssistfpr.readlines():
       if line !="-END-":
          TLSMatchingAssistfpw.writelines(str(1)+"\t"+line)
    TLSMatchingAssistfpr.close()
    TLSMatchingAssistfpw.close()

##由两点创建直线，并返回斜率和截距
def CreateLineFromTwoPoint(linenumber1,linenumber2,PointSourcePath):
    #读取文本文件，获得两点的坐标
    fp= open(PointSourcePath,"r")
    indexofpoint = -1
    for line in fp.readlines():
        indexofpoint= indexofpoint+1
        if indexofpoint==linenumber1:
            x1=float(line.split('\t')[1])
            y1=float(line.split('\t')[2])
        elif indexofpoint==linenumber2:
            x2=float(line.split('\t')[1])
            y2=float(line.split('\t')[2])
    #计算斜率和截距
    k= (y2-y1)/(x2-x1)
    b=y1-k*x1
    print "a=%s,b=%s"%(k,b)
    fp.close()
    return k,b
    
##创建文本文件保存数组信息
def CreateIndexAndPointTxtAfterDouglasCompress(SourcePath,preturnpoints,pointIndexsToKeep):
    txtpath = SourcePath[0:-4]+"C.txt"
    if os.path.exists(txtpath):
       os.remove(txtpath)
       
    txtpathfp=open(txtpath,"w")
    for i in range(0,len(pointIndexsToKeep),1):
        txtpathfp.write(str(preturnpoints[i].X)+"\t"+str(preturnpoints[i].Y)+"\t"+str(pointIndexsToKeep[i])+"\n")
    txtpathfp.close()

##创建文本文件保存总体最小二乘拟合后的点的坐标
def CreateTLSCrossPointTxt(SourcePath,indexandlineArrayTotal,preturnpoints):
    #创建文本文件名
    TLSCrossPointpath = SourcePath[0:-4]+"D.txt"
    if os.path.exists(TLSCrossPointpath):
       os.remove(TLSCrossPointpath)
       
    TLSCrossPointpathfp=open(TLSCrossPointpath,"w")
    #写入第一个点
    TLSindex=0 
    TLSCrossPointpathfp.write((str(0)+"\t"+str(0)+"\t"+str(TLSindex)+"\n"))

    #写入中间点
    for i in range(0,len(indexandlineArrayTotal)-1,1):
        TLSindex = TLSindex +1
        #求得中间点并写入
        TLSx,TLSy=GetCrossPoint(indexandlineArrayTotal[i][2],indexandlineArrayTotal[i][3],indexandlineArrayTotal[i+1][2],indexandlineArrayTotal[i+1][3])
        TLSCrossPointpathfp.write((str(TLSx)+"\t"+str(TLSy)+"\t"+str(TLSindex)+"\n"))
    #写入最后一个点    
    TLSindex = TLSindex +1
    LastLineX = str(preturnpoints[len(preturnpoints)-1].X)
    LastLineY = str(preturnpoints[len(preturnpoints)-1].Y)
    TLSCrossPointpathfp.write(LastLineX+"\t"+LastLineY+"\t"+str(TLSindex)+"\n")   
    TLSCrossPointpathfp.close()











