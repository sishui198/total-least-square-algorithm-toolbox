# -*- coding: cp936 -*-
##����ģ��
import math,arcpy

##��ȡ�ļ��ļ��ض���֮�����Ϣ
def FromTxtGetSpecifyLine(linenumber1,linenumber2,PointSourcePath):
    #���ı��ļ�
    fp= open(PointSourcePath,"r")
    #�����ж�����
    indexofpoint = -1
    
    PointsArray=[]
    for line in fp.readlines():
        indexofpoint= indexofpoint+1
        #�ж϶�ȡ�����Ƿ�������ķ�Χ֮��
        if indexofpoint in range(linenumber1,linenumber2+1,1):
            x1=float(line.replace("\n","").split('\t')[0])
            y1=float(line.replace("\n","").split('\t')[1])
            PointsArray.append([x1,y1])
    fp.close()
    return PointsArray
    

##�����
def ErrorOfDouglasPeuckerFunction(SourcePointsArray):
    #�㼯����β����
    x1=SourcePointsArray[0][0]
    y1=SourcePointsArray[0][1]
    x2=SourcePointsArray[len(SourcePointsArray)-1][0]
    y2=SourcePointsArray[len(SourcePointsArray)-1][1]
    
    #��ӵ�һ������
    DistanceArray=[0.0]
    for i in range(1,len(SourcePointsArray)-1,1):
        #���������ȣ��������
        x0=SourcePointsArray[i][0]
        y0=SourcePointsArray[i][1]
        area = abs(0.5 * (x1 * y2 + x2 * y0 + x0 * y1 - x2 * y1 - x0 * y2 - x1 * y0))
        bottom = math.sqrt(math.pow(x1 - x2, 2) + math.pow(y1 - y2, 2))
        height = area / bottom * 2
        DistanceArray.append(height)
    #������һ������
    DistanceArray.append(0.0)
    return DistanceArray

##ִ������
def ErrorOfDouglasPeuckerMain(infc,pointIndexsToKeep):
    DistanceArrays=[]
    for i in range(0,len(pointIndexsToKeep)-1,1):
        ReturnPointsArray=FromTxtGetSpecifyLine(pointIndexsToKeep[i],pointIndexsToKeep[i+1],infc)
        Flag = pointIndexsToKeep[i+1]-pointIndexsToKeep[i]
        if Flag==1:
            DistanceArrays.append([0.0,0.0])
        elif Flag > 1:
            DistanceArrays.append(ErrorOfDouglasPeuckerFunction(ReturnPointsArray))

    #���������������        
    Distance = 0.0
    index=0
    #���˵��ظ��ĵ�
    for j in range(0,len(DistanceArrays),1):
        ArrayOfJ=DistanceArrays[j]
        if j==0:
            for k in ArrayOfJ:
                Distance = Distance + k
                index=index+1
        else:
            for m in range(1,len(ArrayOfJ),1):
                Distance = Distance + ArrayOfJ[m]
                index=index+1
    print "�ܸ���Ϊ:",index
    print "DouglasPeucker������:",Distance/index
    arcpy.AddMessage("DouglasPeucker������:%.4f"%(Distance/index))
        
##���Գ���
if __name__=="__main__":
    infc = r"C:\Users\Administrator\Desktop\test\result\output.txt"
    pointIndexsToKeep=[0,3,4,5,8,13,16,18,20,22,24,28,29,34,35,38,43,47,49,51,53,56,57,59,61]
    ErrorOfDouglasPeuckerMain(infc,pointIndexsToKeep)



















