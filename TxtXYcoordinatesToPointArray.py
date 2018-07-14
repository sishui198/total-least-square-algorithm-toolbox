# -*- coding: cp936 -*-
##����ģ��
import arcpy
import fileinput

##��ȡ�ı��ļ������ɵ㼯
def TxtXYcoordinatesToPointArray(txtpath):
    #���������ڴ洢X��Y����
    pnt = arcpy.CreateObject("point")
    #�����㼯
    pntarray = arcpy.CreateObject("Array")

    fc = fileinput.input(txtpath)
    for line in fc:
        #�ָ�������
        values = line.replace("\n", "").split("\t")
        #������־
        if values[0] != "-END-":
            pnt.X,pnt.Y = values[0] , values[1]
            pntarray.add(pnt)
    fc.close()
    return pntarray

##���Գ���
if __name__=="__main__":
    infc = r"C:\Users\Administrator\Desktop\temp\result\output.txt"
    PointArray=TxtXYcoordinatesToPointArray(infc)

