# -*- coding: cp936 -*-
##导入模块
import numpy as np
import scipy as Sci
import scipy.linalg
import arcpy

##环境变量设置
arcpy.env.overwriteOutput=True

##参数设置
shp = arcpy.GetParameterAsText(0)
resshp = arcpy.GetParameterAsText(1)
outshp = arcpy.GetParameterAsText(2)

##shp=r"C:\Users\Administrator\Desktop\temp\TLS.shp"
##resshp=r"C:\Users\Administrator\Desktop\temp\TLS_LS.shp"
##outshp=r"C:\Users\Administrator\Desktop\temp\TLS_TLS.shp"

##用于存储点集
pointsArray=[]
rows=arcpy.SearchCursor(shp)
for row in rows:
    points = row.shape
    pointsArray.append([1.0,points.firstPoint.X,points.firstPoint.Y])
del row,rows

# 读入数组
M = np.mat(pointsArray)

(p,q) = M.shape

# 提取系数矩阵
A = M[:,0:q-1]

# 提取观测值矩阵
b = M[:,-1]

# 提取系数矩阵的行列数
(m,n) = A.shape

# 求LS参数
xLS = (A.H*A).I*A.H*b

# 求LS改正数
vLS = A*xLS-b

# 求LS中误差
qLS = np.sqrt(vLS.H*vLS/(m-n))

# 构造增广矩阵
C = np.concatenate((A,b),1)

# 系数针有固定列时，QR分解
[Q,R] = Sci.linalg.qr(C)

CR = R[1:,1:]
# 奇异值分解简称（SVD）
U1, S1, Vh = Sci.linalg.svd(CR)
N1 = Vh.T

# 求LSTLS参数
a0 = np.matrix(0)
a1 = np.concatenate((a0,Sci.zeros((1,n-1))),1)
a2 = np.concatenate((Sci.zeros((n-1,1)),Sci.eye(n-1)),1)
a3 = np.concatenate((a1,a2),0)

xLSTLS =(A.H*A-np.power(S1[n-1,],2)*a3).I*A.H*b

# 求LSTLS残差矩阵
test1 = U1[0:m-1,n-1].reshape(-1,1)
test2 = N1[n-1,0:].reshape(1,-1)
test3 = Sci.zeros((m-1,1))
test4 = test1*S1[n-1,]*test2

b1 = np.concatenate((a0,Sci.zeros((1,n))),1)
b2 = np.concatenate((test3,test4),1)
b3 = np.concatenate((b1,b2),0)

CCLSTLS = Q.conj().T*b3

vLSTLS = CCLSTLS[:,n].H*CCLSTLS[:,n]+CCLSTLS[:,n-1].H*CCLSTLS[:,n-1]

# 求LSTLS中误差
qLSTLS = np.sqrt(vLSTLS/(m-n))

print "a1=%s,b1=%s"%(xLS[1,0],xLS[0,0])
print "a2=%s,b2=%s"%(xLSTLS[1,0],xLSTLS[0,0])

##点集中的首点
x1=pointsArray[0][1]
y1=pointsArray[0][2]
##点集中的尾点
x2=pointsArray[len(pointsArray)-1][1]
y2=pointsArray[len(pointsArray)-1][2]

##根据斜率和截距创建shp文件
def CreateLine(a,b,shppath):

    firstpointx=(x1+a*y1-b*a)/(a*a+1)
    firstpointy=(a*x1+y1*a*a+b)/(a*a+1)

    lastpointx=(x2+a*y2-b*a)/(a*a+1)
    lastpointy=(a*x2+y2*a*a+b)/(a*a+1)

    pnt = arcpy.CreateObject("point")
    pntarray = arcpy.CreateObject("Array") 

    pnt.X,pnt.Y=firstpointx,firstpointy
    pntarray.add(pnt)
    pnt.X,pnt.Y=lastpointx,lastpointy
    pntarray.add(pnt)

    polyline = arcpy.Polyline(pntarray)
    arcpy.CopyFeatures_management(polyline, shppath)

##创建最小二乘直线
CreateLine(xLS[1,0],xLS[0,0],resshp)
##创建总体最小二乘直线
CreateLine(xLSTLS[1,0],xLSTLS[0,0],outshp)

arcpy.AddMessage("普通最小二乘拟合中误差：%.4f"%(qLS[0,0]))
arcpy.AddMessage("总体最小二乘拟合中误差：%.4f"%(qLSTLS[0,0]))

print "Done!"

















