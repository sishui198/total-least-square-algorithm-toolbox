# -*- coding: cp936 -*-
##导入模块
import math,arcpy

##读取文件文件特定行之间的信息
def FromTxtGetSpecifyLine(linenumber1,linenumber2,PointSourcePath):
    #打开文本文件
    fp= open(PointSourcePath,"r")
    #设置判断条件
    indexofpoint = -1
    
    PointsArray=[]
    for line in fp.readlines():
        indexofpoint= indexofpoint+1
        #判断读取的行是否在所求的范围之间
        if indexofpoint in range(linenumber1,linenumber2+1,1):
            x1=float(line.replace("\n","").split('\t')[0])
            y1=float(line.replace("\n","").split('\t')[1])
            PointsArray.append([x1,y1])
    fp.close()
    return PointsArray
    
##求点到直线的距离即误差
def ErrorOfTLSFunction(a,b,SourcePointsArray):
    #根据点到直线距离公式，求误差
    SumOfSquares=math.sqrt(math.pow(a,2)+1)
    DistanceArray=[]
    for i in SourcePointsArray:
        PointToLineDistance=float(abs((a*i[0]+b-i[1])/SumOfSquares))
        DistanceArray.append(PointToLineDistance)
    return DistanceArray

##执行运算
def ErrorOfTLSMain(infc,indexandlineArrayTotal):
    DistanceArrays=[]
    for i in indexandlineArrayTotal:
        ReturnPointsArray=FromTxtGetSpecifyLine(i[0],i[1],infc)
        DistanceArrays.append(ErrorOfTLSFunction(i[2],i[3],ReturnPointsArray))

    #遍历数组求均方根
    Distance = 0.0
    index=0
    #过滤掉重复的点
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
    print "总个数为:",index
    print "TLS均方根:",Distance/index
    arcpy.AddMessage("TLS均方根:%.4f"%(Distance/index))
        
##测试程序
if __name__=="__main__":
    infc = r"C:\Users\Administrator\Desktop\test\result\output.txt"
    indexandlineArrayTotal=[[0, 3, 0.093709376270551509, 0.059592811382953192],
                            [3, 4, -0.17129744690350615, 3.893704307117408],
                            [4, 5, 0.098413117788321652, -1.501287529497932],
                            [5, 8, -0.057625303959542712, 2.4697557636949474],
                            [8, 13, 0.060617834738483284, -2.3660424514414213],
                            [13, 16, -0.091709791894039328, 7.654263301800345],
                            [16, 18, 0.1278402841041045, -10.012732620446908],
                            [18, 20, -0.078448870201036539, 8.5072106995081995],
                            [20, 22, 0.10177985907365213, -9.4457792396224072],
                            [22, 24, -0.17749649437638201, 21.366140077964968],
                            [24, 28, 0.061556688828106478, -7.528388493784286],
                            [28, 29, -0.21872094839237935, 31.746823794343943],
                            [29, 34, 0.010195103811808357, -1.3901002317478235],
                            [34, 35, 0.19821565744197173, -33.570092321006065],
                            [35, 38, -0.066309659887196004, 12.831400902637522],
                            [38, 43, -0.0017299542124922518, 0.50559732473782359],
                            [43, 47, 0.10588566787430287, -22.872271328296442],
                            [47, 49, -0.19892369791495351, 49.059427121791359],
                            [49, 51, 0.058006463549946465, -13.941197689775532],
                            [51, 53, -0.064806808773644198, 17.310507267226939],
                            [53, 56, 0.087639482110169142, -22.955631950238612],
                            [56, 57, -0.17822321758075732, 51.353642129794814],
                            [57, 59, 0.05509964585160327, -15.240003514691558],
                            [59, 61, -0.11162923083716481, 34.091192122030023]]     
    ErrorOfTLSMain(infc,indexandlineArrayTotal)
