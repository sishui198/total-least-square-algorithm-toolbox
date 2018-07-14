# -*- coding: cp936 -*-
##导入模块
import arcpy,math,os,shutil

##三维坐标到二维坐标的转换
def ThreeToTwoDimension(shp):
    #创建临时文件夹（命名为result）
    result = os.path.join(os.path.dirname(shp),"result")
    if os.path.exists(result):
        shutil.rmtree(result)
    os.mkdir(result)
    #创建存放二维坐标的文件
    txt = os.path.join(result,os.path.basename(shp)[0:-3]+"txt")
    fp = open(txt,"w")
    #写入第一个点（原点）
    fp.write(str(0)+"\t"+str(0)+"\n")
    
    #存放所有坐标点
    pointsArray=[]
    rows =arcpy.SearchCursor(shp)
    for row in rows:
        points=row.shape
        pointsArray.append([points.firstPoint.X,points.firstPoint.Y,points.firstPoint.Z])
    del row
    del rows

    #求取参数为投影准备
    #首点
    x1=pointsArray[0][0]
    y1=pointsArray[0][1]
    z1=pointsArray[0][2]
    #尾点
    x2=pointsArray[len(pointsArray)-1][0]
    y2=pointsArray[len(pointsArray)-1][1]
    z2=pointsArray[len(pointsArray)-1][2]
    #首尾点距离
    distance = math.pow(x2-x1,2)+math.pow(y2-y1,2)+math.pow(z2-z1,2)
    
    #遍历shp文件
    for i in range(1,len(pointsArray)-1,1):
        #中间点坐标
        x0=pointsArray[i][0]
        y0=pointsArray[i][1]
        z0=pointsArray[i][2]
        
        k1=(x1-x0)*(x2-x1)+(y1-y0)*(y2-y1)+(z1-z0)*(z2-z1)
        k2=-k1/distance
        #垂足点坐标
        xn=k2*(x2-x1)+x1
        yn=k2*(y2-y1)+y1
        zn=k2*(z2-z1)+z1
        #投影点坐标
        newx=math.sqrt(math.pow(xn-x1,2)+math.pow(yn-y1,2)+math.pow(zn-z1,2))
        newy=math.sqrt(math.pow(xn-x0,2)+math.pow(yn-y0,2)+math.pow(zn-z0,2))
        fp.write(str(newx)+"\t"+str(newy)+"\n")

    #写入最后一个点
    fp.write(str(math.sqrt(distance))+"\t"+str(0)+"\n")
    fp.write("-END-")
    fp.close()
    return pointsArray


##测试程序
if __name__=="__main__":
    shp = r"C:\Users\Administrator\Desktop\test\output.shp"
    Array=ThreeToTwoDimension(shp)
