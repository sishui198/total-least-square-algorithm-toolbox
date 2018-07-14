# -*- coding: cp936 -*-
##����ģ��
import numpy as np
import scipy as Sci
import scipy.linalg
import arcpy

##������������
arcpy.env.overwriteOutput=True

##��������
shp = arcpy.GetParameterAsText(0)
resshp = arcpy.GetParameterAsText(1)
outshp = arcpy.GetParameterAsText(2)

##shp=r"C:\Users\Administrator\Desktop\temp\TLS.shp"
##resshp=r"C:\Users\Administrator\Desktop\temp\TLS_LS.shp"
##outshp=r"C:\Users\Administrator\Desktop\temp\TLS_TLS.shp"

##���ڴ洢�㼯
pointsArray=[]
rows=arcpy.SearchCursor(shp)
for row in rows:
    points = row.shape
    pointsArray.append([1.0,points.firstPoint.X,points.firstPoint.Y])
del row,rows

# ��������
M = np.mat(pointsArray)

(p,q) = M.shape

# ��ȡϵ������
A = M[:,0:q-1]

# ��ȡ�۲�ֵ����
b = M[:,-1]

# ��ȡϵ�������������
(m,n) = A.shape

# ��LS����
xLS = (A.H*A).I*A.H*b

# ��LS������
vLS = A*xLS-b

# ��LS�����
qLS = np.sqrt(vLS.H*vLS/(m-n))

# �����������
C = np.concatenate((A,b),1)

# ϵ�����й̶���ʱ��QR�ֽ�
[Q,R] = Sci.linalg.qr(C)

CR = R[1:,1:]
# ����ֵ�ֽ��ƣ�SVD��
U1, S1, Vh = Sci.linalg.svd(CR)
N1 = Vh.T

# ��LSTLS����
a0 = np.matrix(0)
a1 = np.concatenate((a0,Sci.zeros((1,n-1))),1)
a2 = np.concatenate((Sci.zeros((n-1,1)),Sci.eye(n-1)),1)
a3 = np.concatenate((a1,a2),0)

xLSTLS =(A.H*A-np.power(S1[n-1,],2)*a3).I*A.H*b

# ��LSTLS�в����
test1 = U1[0:m-1,n-1].reshape(-1,1)
test2 = N1[n-1,0:].reshape(1,-1)
test3 = Sci.zeros((m-1,1))
test4 = test1*S1[n-1,]*test2

b1 = np.concatenate((a0,Sci.zeros((1,n))),1)
b2 = np.concatenate((test3,test4),1)
b3 = np.concatenate((b1,b2),0)

CCLSTLS = Q.conj().T*b3

vLSTLS = CCLSTLS[:,n].H*CCLSTLS[:,n]+CCLSTLS[:,n-1].H*CCLSTLS[:,n-1]

# ��LSTLS�����
qLSTLS = np.sqrt(vLSTLS/(m-n))

print "a1=%s,b1=%s"%(xLS[1,0],xLS[0,0])
print "a2=%s,b2=%s"%(xLSTLS[1,0],xLSTLS[0,0])

##�㼯�е��׵�
x1=pointsArray[0][1]
y1=pointsArray[0][2]
##�㼯�е�β��
x2=pointsArray[len(pointsArray)-1][1]
y2=pointsArray[len(pointsArray)-1][2]

##����б�ʺͽؾഴ��shp�ļ�
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

##������С����ֱ��
CreateLine(xLS[1,0],xLS[0,0],resshp)
##����������С����ֱ��
CreateLine(xLSTLS[1,0],xLSTLS[0,0],outshp)

arcpy.AddMessage("��ͨ��С�����������%.4f"%(qLS[0,0]))
arcpy.AddMessage("������С�����������%.4f"%(qLSTLS[0,0]))

print "Done!"

















