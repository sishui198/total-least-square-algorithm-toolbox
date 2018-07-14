# -*- coding: cp936 -*-
##导入模块
import os,arcpy
import numpy as np
from ThreeToTwoDimension import ThreeToTwoDimension
from TxtXYcoordinatesToPointArray import TxtXYcoordinatesToPointArray
from UtilityOfDouglasPeucker import GetDouglasPeuckerReduction
import TxtOperationFunctionsTotal
from TLSMatchingMain import TLSMatchingMain
from TLSSpecialMain import TLSSpecialMain
from TwoToThreeDimension import TwoToThreeDimension
from PointToLine import PointToLine


##参数设置
shp = arcpy.GetParameterAsText(0)
Tolerance=float(arcpy.GetParameterAsText(1).split(" ")[0])
TLSTolerance=float(arcpy.GetParameterAsText(2).split(" ")[0])
shppath=arcpy.GetParameterAsText(3)

##shp = r"C:\Users\Administrator\Desktop\test\output.shp"
##Tolerance=0.5
##TLSTolerance=1.0
##shppath=shp[0:-4]+"Result.shp"


"三维坐标转为二维"
ArrayForOrigin=ThreeToTwoDimension(shp)

"二维坐标生成点"
#二维坐标路径
infc=os.path.join(os.path.split(shp)[0],"result",os.path.split(shp)[1].split('.')[0]+".txt")
PointsArray=TxtXYcoordinatesToPointArray(infc)


print "DouglasPeucker Compress Dealing!"
print "处理前点的个数:%r"%len(PointsArray)

"道格拉斯压缩"
pointIndexsToKeep=[]
#进行压缩，返回压缩后的点集和序号的集合
preturnpoints,pointIndexsToKeep=GetDouglasPeuckerReduction(PointsArray,Tolerance)
print "DouglasPeucker Compress Completed!"

"总体最小二乘拟合"
txtpath = infc[0:-4]+"A.txt"
#创建总体最小二乘辅助数组，并保存成文本文件
TxtOperationFunctionsTotal.CreateTLSMatchingAssistTxt(infc,txtpath)
#进行总体最小二乘，返回存放所有拟合直线的首尾点序号和斜率及截距的数组
indexandlineArrayTotal=TLSMatchingMain(txtpath,pointIndexsToKeep)
print "总体最小二乘拟合完成!"

#创建文本文件保存压缩后的点集和序号的集合
TxtOperationFunctionsTotal.CreateIndexAndPointTxtAfterDouglasCompress(infc,preturnpoints,pointIndexsToKeep)
#创建文本文件保存总体最小二乘拟合后的点的坐标
TxtOperationFunctionsTotal.CreateTLSCrossPointTxt(infc,indexandlineArrayTotal,preturnpoints)

"TLS最后处理"
TLSSpecialMain(infc,TLSTolerance)

"二维坐标转化为三维"
TwoToThreeDimension(infc,ArrayForOrigin)

"压缩后生成shp"
textpath=infc[0:-4]+"F.txt"
PointToLine(textpath,shppath)


from ErrorOfTLS import ErrorOfTLSMain
from ErrorOfDouglasPeucker import ErrorOfDouglasPeuckerMain
"误差处理"
ErrorOfTLSMain(infc,indexandlineArrayTotal)
ErrorOfDouglasPeuckerMain(infc,pointIndexsToKeep)












