# -*- coding: cp936 -*-
##求两直线的交点坐标
def GetCrossPoint(a1,a2,a3,a4):
    #第一条直线的斜率和截距
    k1=float(a1)
    b1=float(a2)
    #第二条直线的斜率和截距
    k2=float(a3)
    b2=float(a4)

    #判断直线是否相交
    if k1==k2 and b1==b2:       
        return "chong he!"
    elif k1==k2 and b1!=b2:
        return "wu jiao dian!"
    else:
        x=(b2-b1)/(k1-k2)
        y=k1*x+b1
        return x,y
