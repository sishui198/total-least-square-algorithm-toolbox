# -*- coding: cp936 -*-
##导入模块
import numpy as np
from TLSMatchingFunction import TLSMatching
import TxtOperationFunctionsTotal

##执行总体最小二乘拟合
def TLSMatchingMain(txtpath,pointIndexsToKeep):
    #读入数据
    MM = np.mat(np.loadtxt(txtpath))
    #存放所有拟合直线的首尾点序号和斜率及截距
    indexandlineArrayTotal=[]

    #遍历道格拉斯压缩保留点的序号
    for i in range(0,len(pointIndexsToKeep)-1,1):
       #存放一条拟合直线的首尾点序号和斜率及截距 
       indexandlineArray=[]
       if i == 0:
            #加入直线首点和尾点序号
            indexandlineArray.append(0)
            indexandlineArray.append(pointIndexsToKeep[i+1])

            #分离数据，用于分段拟合
            M = MM[0:pointIndexsToKeep[i+1]+1,:]      
            print 0,pointIndexsToKeep[i+1]
            #判断拟合点的个数
            flag1 = pointIndexsToKeep[i+1]-0
            #若个数大于2个，进行总体最小二乘拟合
            if flag1 !=1:
                #总体最小二乘拟合
                niheresult1,niheresult2=TLSMatching(M)
                #加入斜率及截距
                indexandlineArray.append(niheresult1)
                indexandlineArray.append(niheresult2)
                
                indexandlineArrayTotal.append(indexandlineArray)
            #若个数为2，由两点创建直线
            else:
                niheresult3,niheresult4=TxtOperationFunctionsTotal.CreateLineFromTwoPoint(0,pointIndexsToKeep[i+1],txtpath)
                indexandlineArray.append(niheresult3)
                indexandlineArray.append(niheresult4)
                indexandlineArrayTotal.append(indexandlineArray)
       else:      
            indexandlineArray.append(pointIndexsToKeep[i])
            indexandlineArray.append(pointIndexsToKeep[i+1])
            
            M = MM[pointIndexsToKeep[i]:pointIndexsToKeep[i+1]+1,:]
            print pointIndexsToKeep[i],pointIndexsToKeep[i+1]
            flag1 = pointIndexsToKeep[i+1]-pointIndexsToKeep[i]
            if flag1 !=1:
                niheresult5,niheresult6=TLSMatching(M)
                indexandlineArray.append(niheresult5)
                indexandlineArray.append(niheresult6)
                indexandlineArrayTotal.append(indexandlineArray)
            else:
                niheresult7,niheresult8=TxtOperationFunctionsTotal.CreateLineFromTwoPoint(pointIndexsToKeep[i],pointIndexsToKeep[i+1],txtpath)
                indexandlineArray.append(niheresult7)
                indexandlineArray.append(niheresult8)
                indexandlineArrayTotal.append(indexandlineArray)
    return indexandlineArrayTotal
