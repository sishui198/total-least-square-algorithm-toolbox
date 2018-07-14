# -*- coding: cp936 -*-
##导入模块
import arcpy,os

##由点坐标，生成线
def PointToLine(txtpath,shppath):
    #创建用于存储X，Y坐标
    pnt = arcpy.CreateObject("point")
    #创建点组
    pntarray = arcpy.CreateObject("Array")  

    #读取点坐标
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
##测试程序
if __name__=="__main__":
    txtpath=r"C:\Users\Administrator\Desktop\test\result\outputF.txt"
    shppath=r"C:\Users\Administrator\Desktop\test\result\output3.shp"
    PointToLine(txtpath,shppath)
    print "Done!"
