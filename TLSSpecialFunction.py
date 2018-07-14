# -*- coding: cp936 -*-
##导入模块
import os,math
import numpy as np
from shapely.geometry.polygon import LineString

##读取文本文件，将信息存入数组
def ReadTxtToArray(txtpath):
    fp= open(txtpath,"r")
    array=[]
    for line in fp.readlines():
        x0=float(line.replace("\n", "").split("\t")[0])
        y0=float(line.replace("\n", "").split("\t")[1])
        index=int(line.replace("\n", "").split("\t")[2])
        array.append([x0,y0,index])
    fp.close()
    return array    

##读取文本文件，将曲线坐标存入数组
def GetCurveLinecoordinates(textpath):
    fp=open(textpath,"r")
    CurveLine=[]
    index = 0
    for line in fp.readlines():
        if line !="-END-":
            index = index+1
            x0=float(line.replace("\n", "").split("\t")[0])
            y0=float(line.replace("\n", "").split("\t")[1])
            CurveLine.append((x0,y0))
    fp.close()
    return CurveLine

##将直线的首尾点坐标，存入数组
def GetStraightLinecoordinates(startx,starty,endx,endy):
    StraightLine=[]
    StraightLine.append((startx,starty))
    StraightLine.append((endx,endy))
    return StraightLine

##执行运算
def GetCrossPoint(infc,NeedIndex):
    #生成曲线
    Curve=LineString(GetCurveLinecoordinates(infc))

    #读取文本文件，获得总体最小二乘压缩点坐标数组
    TLSTxtpath= infc[0:-4]+"D.txt"    
    TLSfp= open(TLSTxtpath,"r")
    TLSLine=[]
    for line in TLSfp.readlines():
        x0=float(line.replace("\n", "").split("\t")[0])
        y0=float(line.replace("\n", "").split("\t")[1])
        TLSLine.append((x0,y0))
    TLSfp.close()

    #求交点
    for i in range(0,len(TLSLine)-1,1):
        if i == NeedIndex:
            ##后交点
            #生成直线
            LineA=LineString(GetStraightLinecoordinates(TLSLine[i][0],TLSLine[i][1],TLSLine[i+1][0],TLSLine[i+1][1]))    
            #获得交点
            CrossPoint=LineA.intersection(Curve)
            #存放交点
            CrossPointArrays=[]
            #判断交点类型
            if str(type(CrossPoint))== "<class 'shapely.geometry.multipoint.MultiPoint'>":
                for j in range(0,len(list(CrossPoint)),1):
                    CrossPointArrays.append([list(CrossPoint)[j].x,list(CrossPoint)[j].y])
            elif str(type(CrossPoint))== "<class 'shapely.geometry.point.Point'>":
                CrossPointArrays.append([CrossPoint.x,CrossPoint.y])

            #前交点
            LineB=LineString(GetStraightLinecoordinates(TLSLine[i-1][0],TLSLine[i-1][1],TLSLine[i][0],TLSLine[i][1]))
            print "前直线",TLSLine[i-1][0],TLSLine[i-1][1],TLSLine[i][0],TLSLine[i][1]
            CrossPoint2=LineB.intersection(Curve)
            CrossPointArraysBefore=[]
            if str(type(CrossPoint2))== "<class 'shapely.geometry.multipoint.MultiPoint'>":
                for k in range(0,len(list(CrossPoint2)),1):
                    CrossPointArraysBefore.append([list(CrossPoint2)[k].x,list(CrossPoint2)[k].y])
            elif str(type(CrossPoint2))== "<class 'shapely.geometry.point.Point'>":
                CrossPointArraysBefore.append([CrossPoint2.x,CrossPoint2.y])
          
    return CrossPointArraysBefore,CrossPointArrays
























