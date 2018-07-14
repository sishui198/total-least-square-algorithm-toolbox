# -*- coding: cp936 -*-
##导入模块
import arcpy
import fileinput

##读取文本文件，生成点集
def TxtXYcoordinatesToPointArray(txtpath):
    #创建点用于存储X，Y坐标
    pnt = arcpy.CreateObject("point")
    #创建点集
    pntarray = arcpy.CreateObject("Array")

    fc = fileinput.input(txtpath)
    for line in fc:
        #分隔符设置
        values = line.replace("\n", "").split("\t")
        #结束标志
        if values[0] != "-END-":
            pnt.X,pnt.Y = values[0] , values[1]
            pntarray.add(pnt)
    fc.close()
    return pntarray

##测试程序
if __name__=="__main__":
    infc = r"C:\Users\Administrator\Desktop\temp\result\output.txt"
    PointArray=TxtXYcoordinatesToPointArray(infc)

