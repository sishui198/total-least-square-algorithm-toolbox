# -*- coding: cp936 -*-
##����ģ��
import math

##ִ�е�����˹ѹ��
def GetDouglasPeuckerReduction(Points,Tolerance):
    #����㼯��������3������ִ��ѹ��
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

        #ѹ�� 
        DouglasPeucker(Points, firstPoint, lastPoint, Tolerance, pointIndexsToKeep)
        #ѹ�������㼯
        returnPoints = []
        #���������������
        pointIndexsToKeep.sort()
        
        print "������ĸ���:%r"%len(pointIndexsToKeep)

        #���뱣���ĵ㵽������
        for index in pointIndexsToKeep:
            returnPoints.append(Points[index])
        return returnPoints,pointIndexsToKeep

##ִ�е������㣬�������������
def DouglasPeucker(points,firstPoint,lastPoint,tolerance,pointIndexsToKeep):
    maxDistance = 0.0
    indexFarthest = 0

    #�жϸ����ĵ㼯�����е㵽��β�����ߵ����ֱ����    
    for i in range(firstPoint,lastPoint,1): 
        distance = PerpendicularDistance(points[firstPoint], points[lastPoint], points[i])
        if distance > maxDistance:
            maxDistance = distance
            indexFarthest = i
    #���е���  
    if(maxDistance > tolerance and indexFarthest != 0):
        # Add the largest point that exceeds the tolerance
        pointIndexsToKeep.append(indexFarthest)        
        DouglasPeucker(points, firstPoint, indexFarthest, tolerance,pointIndexsToKeep)
        DouglasPeucker(points, indexFarthest, lastPoint, tolerance, pointIndexsToKeep)

##��point��point1��point2���ߵĴ�ֱ����
def PerpendicularDistance(point1,point2,point):
    #���׹�ʽ�������
    area = math.fabs(0.5 * (point1.X * point2.Y + point2.X * point.Y + point.X * point1.Y - point2.X * point1.Y - point.X * point2.Y - point1.X * point.Y))

    bottom = math.sqrt(math.pow(point1.X - point2.X, 2) + math.pow(point1.Y - point2.Y, 2))
    height = area / bottom * 2
    return height
