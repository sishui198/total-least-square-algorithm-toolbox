# -*- coding: cp936 -*-
##����ģ��
import arcpy,os

##�ɵ����꣬������
def PointToLine(txtpath,shppath):
    #�������ڴ洢X��Y����
    pnt = arcpy.CreateObject("point")
    #��������
    pntarray = arcpy.CreateObject("Array")  

    #��ȡ������
    fp=open(txtpath,"r")
    for line in fp.readlines():
        lineArray=line.replace("\n","").split("\t")
        pnt.X,pnt.Y,pnt.Z = float(lineArray[0]),float(lineArray[1]),float(lineArray[2])
        pntarray.add(pnt)
    fp.close()

    arcpy.env.overwriteOutput = True   
    outPath,outFC=os.path.split(shppath)
    arcpy.CreateFeatureclass_management(outPath,outFC,"POINT","",
                                        "DISABLED","ENABLED")   
    iCur=arcpy.InsertCursor(shppath)
    for i in pntarray:
        feat = iCur.newRow()
        feat.shape=i
        iCur.insertRow(feat)
    del iCur    
##���Գ���
if __name__=="__main__":
    txtpath=r"C:\Users\Administrator\Desktop\test\result\outputF.txt"
    shppath=r"C:\Users\Administrator\Desktop\test\result\output3.shp"
    PointToLine(txtpath,shppath)
    print "Done!"
