# -*- coding: cp936 -*-
##����ģ��
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


##��������
shp = arcpy.GetParameterAsText(0)
Tolerance=float(arcpy.GetParameterAsText(1).split(" ")[0])
TLSTolerance=float(arcpy.GetParameterAsText(2).split(" ")[0])
shppath=arcpy.GetParameterAsText(3)

##shp = r"C:\Users\Administrator\Desktop\test\output.shp"
##Tolerance=0.5
##TLSTolerance=1.0
##shppath=shp[0:-4]+"Result.shp"


"��ά����תΪ��ά"
ArrayForOrigin=ThreeToTwoDimension(shp)

"��ά�������ɵ�"
#��ά����·��
infc=os.path.join(os.path.split(shp)[0],"result",os.path.split(shp)[1].split('.')[0]+".txt")
PointsArray=TxtXYcoordinatesToPointArray(infc)


print "DouglasPeucker Compress Dealing!"
print "����ǰ��ĸ���:%r"%len(PointsArray)

"������˹ѹ��"
pointIndexsToKeep=[]
#����ѹ��������ѹ����ĵ㼯����ŵļ���
preturnpoints,pointIndexsToKeep=GetDouglasPeuckerReduction(PointsArray,Tolerance)
print "DouglasPeucker Compress Completed!"

"������С�������"
txtpath = infc[0:-4]+"A.txt"
#����������С���˸������飬��������ı��ļ�
TxtOperationFunctionsTotal.CreateTLSMatchingAssistTxt(infc,txtpath)
#����������С���ˣ����ش���������ֱ�ߵ���β����ź�б�ʼ��ؾ������
indexandlineArrayTotal=TLSMatchingMain(txtpath,pointIndexsToKeep)
print "������С����������!"

#�����ı��ļ�����ѹ����ĵ㼯����ŵļ���
TxtOperationFunctionsTotal.CreateIndexAndPointTxtAfterDouglasCompress(infc,preturnpoints,pointIndexsToKeep)
#�����ı��ļ�����������С������Ϻ�ĵ������
TxtOperationFunctionsTotal.CreateTLSCrossPointTxt(infc,indexandlineArrayTotal,preturnpoints)

"TLS�����"
TLSSpecialMain(infc,TLSTolerance)

"��ά����ת��Ϊ��ά"
TwoToThreeDimension(infc,ArrayForOrigin)

"ѹ��������shp"
textpath=infc[0:-4]+"F.txt"
PointToLine(textpath,shppath)


from ErrorOfTLS import ErrorOfTLSMain
from ErrorOfDouglasPeucker import ErrorOfDouglasPeuckerMain
"����"
ErrorOfTLSMain(infc,indexandlineArrayTotal)
ErrorOfDouglasPeuckerMain(infc,pointIndexsToKeep)












