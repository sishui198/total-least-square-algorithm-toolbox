# -*- coding: cp936 -*-
##����ģ��
import numpy as np
from TLSMatchingFunction import TLSMatching
import TxtOperationFunctionsTotal

##ִ��������С�������
def TLSMatchingMain(txtpath,pointIndexsToKeep):
    #��������
    MM = np.mat(np.loadtxt(txtpath))
    #����������ֱ�ߵ���β����ź�б�ʼ��ؾ�
    indexandlineArrayTotal=[]

    #����������˹ѹ������������
    for i in range(0,len(pointIndexsToKeep)-1,1):
       #���һ�����ֱ�ߵ���β����ź�б�ʼ��ؾ� 
       indexandlineArray=[]
       if i == 0:
            #����ֱ���׵��β�����
            indexandlineArray.append(0)
            indexandlineArray.append(pointIndexsToKeep[i+1])

            #�������ݣ����ڷֶ����
            M = MM[0:pointIndexsToKeep[i+1]+1,:]      
            print 0,pointIndexsToKeep[i+1]
            #�ж���ϵ�ĸ���
            flag1 = pointIndexsToKeep[i+1]-0
            #����������2��������������С�������
            if flag1 !=1:
                #������С�������
                niheresult1,niheresult2=TLSMatching(M)
                #����б�ʼ��ؾ�
                indexandlineArray.append(niheresult1)
                indexandlineArray.append(niheresult2)
                
                indexandlineArrayTotal.append(indexandlineArray)
            #������Ϊ2�������㴴��ֱ��
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
