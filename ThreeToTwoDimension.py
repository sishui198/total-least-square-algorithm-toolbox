# -*- coding: cp936 -*-
##����ģ��
import arcpy,math,os,shutil

##��ά���굽��ά�����ת��
def ThreeToTwoDimension(shp):
    #������ʱ�ļ��У�����Ϊresult��
    result = os.path.join(os.path.dirname(shp),"result")
    if os.path.exists(result):
        shutil.rmtree(result)
    os.mkdir(result)
    #������Ŷ�ά������ļ�
    txt = os.path.join(result,os.path.basename(shp)[0:-3]+"txt")
    fp = open(txt,"w")
    #д���һ���㣨ԭ�㣩
    fp.write(str(0)+"\t"+str(0)+"\n")
    
    #������������
    pointsArray=[]
    rows =arcpy.SearchCursor(shp)
    for row in rows:
        points=row.shape
        pointsArray.append([points.firstPoint.X,points.firstPoint.Y,points.firstPoint.Z])
    del row
    del rows

    #��ȡ����ΪͶӰ׼��
    #�׵�
    x1=pointsArray[0][0]
    y1=pointsArray[0][1]
    z1=pointsArray[0][2]
    #β��
    x2=pointsArray[len(pointsArray)-1][0]
    y2=pointsArray[len(pointsArray)-1][1]
    z2=pointsArray[len(pointsArray)-1][2]
    #��β�����
    distance = math.pow(x2-x1,2)+math.pow(y2-y1,2)+math.pow(z2-z1,2)
    
    #����shp�ļ�
    for i in range(1,len(pointsArray)-1,1):
        #�м������
        x0=pointsArray[i][0]
        y0=pointsArray[i][1]
        z0=pointsArray[i][2]
        
        k1=(x1-x0)*(x2-x1)+(y1-y0)*(y2-y1)+(z1-z0)*(z2-z1)
        k2=-k1/distance
        #���������
        xn=k2*(x2-x1)+x1
        yn=k2*(y2-y1)+y1
        zn=k2*(z2-z1)+z1
        #ͶӰ������
        newx=math.sqrt(math.pow(xn-x1,2)+math.pow(yn-y1,2)+math.pow(zn-z1,2))
        newy=math.sqrt(math.pow(xn-x0,2)+math.pow(yn-y0,2)+math.pow(zn-z0,2))
        fp.write(str(newx)+"\t"+str(newy)+"\n")

    #д�����һ����
    fp.write(str(math.sqrt(distance))+"\t"+str(0)+"\n")
    fp.write("-END-")
    fp.close()
    return pointsArray


##���Գ���
if __name__=="__main__":
    shp = r"C:\Users\Administrator\Desktop\test\output.shp"
    Array=ThreeToTwoDimension(shp)
