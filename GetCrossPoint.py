# -*- coding: cp936 -*-
##����ֱ�ߵĽ�������
def GetCrossPoint(a1,a2,a3,a4):
    #��һ��ֱ�ߵ�б�ʺͽؾ�
    k1=float(a1)
    b1=float(a2)
    #�ڶ���ֱ�ߵ�б�ʺͽؾ�
    k2=float(a3)
    b2=float(a4)

    #�ж�ֱ���Ƿ��ཻ
    if k1==k2 and b1==b2:       
        return "chong he!"
    elif k1==k2 and b1!=b2:
        return "wu jiao dian!"
    else:
        x=(b2-b1)/(k1-k2)
        y=k1*x+b1
        return x,y
