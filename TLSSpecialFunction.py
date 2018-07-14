# -*- coding: cp936 -*-
##����ģ��
import os,math
import numpy as np
from shapely.geometry.polygon import LineString

##��ȡ�ı��ļ�������Ϣ��������
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

##��ȡ�ı��ļ��������������������
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

##��ֱ�ߵ���β�����꣬��������
def GetStraightLinecoordinates(startx,starty,endx,endy):
    StraightLine=[]
    StraightLine.append((startx,starty))
    StraightLine.append((endx,endy))
    return StraightLine

##ִ������
def GetCrossPoint(infc,NeedIndex):
    #��������
    Curve=LineString(GetCurveLinecoordinates(infc))

    #��ȡ�ı��ļ������������С����ѹ������������
    TLSTxtpath= infc[0:-4]+"D.txt"    
    TLSfp= open(TLSTxtpath,"r")
    TLSLine=[]
    for line in TLSfp.readlines():
        x0=float(line.replace("\n", "").split("\t")[0])
        y0=float(line.replace("\n", "").split("\t")[1])
        TLSLine.append((x0,y0))
    TLSfp.close()

    #�󽻵�
    for i in range(0,len(TLSLine)-1,1):
        if i == NeedIndex:
            ##�󽻵�
            #����ֱ��
            LineA=LineString(GetStraightLinecoordinates(TLSLine[i][0],TLSLine[i][1],TLSLine[i+1][0],TLSLine[i+1][1]))    
            #��ý���
            CrossPoint=LineA.intersection(Curve)
            #��Ž���
            CrossPointArrays=[]
            #�жϽ�������
            if str(type(CrossPoint))== "<class 'shapely.geometry.multipoint.MultiPoint'>":
                for j in range(0,len(list(CrossPoint)),1):
                    CrossPointArrays.append([list(CrossPoint)[j].x,list(CrossPoint)[j].y])
            elif str(type(CrossPoint))== "<class 'shapely.geometry.point.Point'>":
                CrossPointArrays.append([CrossPoint.x,CrossPoint.y])

            #ǰ����
            LineB=LineString(GetStraightLinecoordinates(TLSLine[i-1][0],TLSLine[i-1][1],TLSLine[i][0],TLSLine[i][1]))
            print "ǰֱ��",TLSLine[i-1][0],TLSLine[i-1][1],TLSLine[i][0],TLSLine[i][1]
            CrossPoint2=LineB.intersection(Curve)
            CrossPointArraysBefore=[]
            if str(type(CrossPoint2))== "<class 'shapely.geometry.multipoint.MultiPoint'>":
                for k in range(0,len(list(CrossPoint2)),1):
                    CrossPointArraysBefore.append([list(CrossPoint2)[k].x,list(CrossPoint2)[k].y])
            elif str(type(CrossPoint2))== "<class 'shapely.geometry.point.Point'>":
                CrossPointArraysBefore.append([CrossPoint2.x,CrossPoint2.y])
          
    return CrossPointArraysBefore,CrossPointArrays
























