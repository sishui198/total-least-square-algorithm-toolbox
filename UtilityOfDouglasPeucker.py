# -*- coding: cp936 -*-
##导入模块
import math

##执行道格拉斯压缩
def GetDouglasPeuckerReduction(Points,Tolerance):
    #如果点集个数少于3个，不执行压缩
    pointIndexsToKeep = []
    if(len(Points) < 3):
        return Points,pointIndexsToKeep
    else:
        firstPoint = 0
        lastPoint = len(Points)-1        

        # Add the first and last index to the keepers
        pointIndexsToKeep.append(firstPoint)
        pointIndexsToKeep.append(lastPoint)

        # The first and the last point can not be the same
        while(Points[firstPoint].X == Points[lastPoint].X and Points[firstPoint].Y == Points[lastPoint].Y):
            lastPoint -=1

        #压缩 
        DouglasPeucker(Points, firstPoint, lastPoint, Tolerance, pointIndexsToKeep)
        #压缩后保留点集
        returnPoints = []
        #保留点号重新排序
        pointIndexsToKeep.sort()
        
        print "处理后点的个数:%r"%len(pointIndexsToKeep)

        #存入保留的点到集合中
        for index in pointIndexsToKeep:
            returnPoints.append(Points[index])
        return returnPoints,pointIndexsToKeep

##执行迭代运算，求出保留点的序号
def DouglasPeucker(points,firstPoint,lastPoint,tolerance,pointIndexsToKeep):
    maxDistance = 0.0
    indexFarthest = 0

    #判断给定的点集中所有点到首尾点连线的最大垂直距离    
    for i in range(firstPoint,lastPoint,1): 
        distance = PerpendicularDistance(points[firstPoint], points[lastPoint], points[i])
        if distance > maxDistance:
            maxDistance = distance
            indexFarthest = i
    #进行迭代  
    if(maxDistance > tolerance and indexFarthest != 0):
        # Add the largest point that exceeds the tolerance
        pointIndexsToKeep.append(indexFarthest)        
        DouglasPeucker(points, firstPoint, indexFarthest, tolerance,pointIndexsToKeep)
        DouglasPeucker(points, indexFarthest, lastPoint, tolerance, pointIndexsToKeep)

##点point到point1和point2连线的垂直距离
def PerpendicularDistance(point1,point2,point):
    #海伦公式计算面积
    area = math.fabs(0.5 * (point1.X * point2.Y + point2.X * point.Y + point.X * point1.Y - point2.X * point1.Y - point.X * point2.Y - point1.X * point.Y))

    bottom = math.sqrt(math.pow(point1.X - point2.X, 2) + math.pow(point1.Y - point2.Y, 2))
    height = area / bottom * 2
    return height
