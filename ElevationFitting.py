# -*- coding: cp936 -*-
##导入模块
import numpy as np
import scipy as Sci
import os

##参数设置
txtpath=arcpy.GetParameterAsText(0)
checkpath=arcpy.GetParameterAsText(1)
resultpath=arcpy.GetParameterAsText(2)
Flag=arcpy.GetParameterAsText(3)




##读入拟合点数据
M = np.mat(np.loadtxt(txtpath))
##读入检核点数据
MM = np.mat(np.loadtxt(checkpath))

##取矩阵的行列值
(p,q) = M.shape
##取系数矩阵A
A=M[:,0:q-1]
##取观测值阵L
L=M[:,q-1]

(a,b)=MM.shape
A1=MM[:,0:b-1]
L1=MM[:,b-1]

##判断是否等精度
##不等精度计算   
if Flag=="true":
    ##观测值的近似值
    x0=0.0
    y0=0.0
    for i in range(0,p,1):
        x0 +=A[i,1]
        y0 +=A[i,2]
    x0=x0/p
    y0=y0/p

    ##系数阵行向量协因素阵确定
    Qx=Sci.eye(p)
    ##观测值协因素阵的确定
    Ql=20*(Sci.eye(p))

    ##系数阵列向量协因素阵确定
    Q0=Sci.eye(q-1)
    Q0[0,0]=0
    Q0[1,1]=1
    Q0[1,3]=2*x0
    Q0[1,5]=y0
    Q0[2,2]=1
    Q0[2,4]=2*y0
    Q0[2,5]=x0
    Q0[3,1]=2*x0
    Q0[3,3]=4*x0**2
    Q0[3,5]=2*x0*y0
    Q0[4,2]=2*y0
    Q0[4,4]=4*y0**2
    Q0[4,5]=2*x0*y0
    Q0[5,1]=y0
    Q0[5,2]=x0
    Q0[5,3]=2*x0*y0
    Q0[5,4]=2*x0*y0
    Q0[5,5]=x0**2+y0**2

    ##迭代限差值
    ddxc=0.000000001
    ##迭代次数
    ii=0
    ##中间参数
    pL=np.linalg.pinv(Ql)
    N=A.H*pL*A
    c=A.H*pL*L
    v=0
    X0=np.linalg.pinv(N)*c
    ##WTLS参数
    X1=np.linalg.pinv(A.H*np.linalg.pinv(Ql+(X0.H*Q0*X0)[0,0]*Qx)*A)*A.H*np.linalg.pinv(Ql+(X0.H*Q0*X0)[0,0]*Qx)*L

    ##迭代
    while X1.any() !=0:
        K1=np.linalg.pinv(Ql+(X1.H*Q0*X1))*(L-A*X1)
        v1=K1.H*Qx*K1
        X2=np.linalg.pinv(A.H*np.linalg.pinv(Ql+(X1.H*Q0*X1)[0,0]*Qx)*A-v1[0,0]*Q0)*A.H*np.linalg.pinv(Ql+(X1.H*Q0*X1)[0,0]*Qx)*L
        H=X2-X1
        if np.sqrt(H.H*H) <= ddxc:
            break
        X1=X2
        ii = ii+1

    ##取矩阵的行列值
    [n,m]=A.shape
    ##LS参数
    xLS=X0

    vLS=A*xLS-L
    ##LS中误差
    qLS=np.sqrt(vLS.H*vLS/(n-m))

    vLSJH=A1*xLS-L1
    ##LS检核中误差
    qLSJH=np.sqrt(vLSJH.H*vLSJH/a)                                                             

    ##计算TLS拟合中误差
    qTLS=np.sqrt((K1.H*(L-A*X2))/(n-m))

    vTLSJH=A1*X2-L1
    ##计算TLS检核中误差
    qTLSJH=np.sqrt(vTLSJH.H*vTLSJH/a)

    ##成果输出
    if os.path.exists(resultpath):
        os.remove(resultpath)
    fp=open(resultpath,"w")
    j,k=L1.shape
    for i in range(0,j,1):
        fp.write(str(i+1)+"\t%.6f\t%.6f\n"%(L1[i,0],(A1*X2)[i,0]))
    fp.write("加权总体最小二乘中误差：\t%.6f\n"%(qTLS[0,0]))
    fp.write("加权总体最小二乘检核中误差：\t%.6f\n"%(qTLSJH[0,0]))
    fp.close()
##等精度计算
else:
    ##取矩阵的行列值
    [n,m]=A.shape
    ##迭代限差值
    ddxc=0.000000001
    ##迭代次数
    ii=0
    ##中间参数
    N=A.H*A                                          
    c=A.H*L
    v=0
    X1=np.linalg.pinv(N)*c
    ##迭代
    while X1.any() !=0:
        v=(L-A*X1).H*(L-A*X1)/(1+X1.H*X1)
        X2=np.linalg.pinv(N)*(c+X1*v)
        H=X2-X1
        if np.sqrt(H.H*H)<=ddxc:
            break
        X1=X2
        ii=ii+1

    ##TLS中误差    
    qTLS=np.sqrt(v/(n-m))                    
                                                                                                                                                                              
    vTLSJH=A1*X2-L1
    ##TLS检核中误差
    qTLSJH=np.sqrt(vTLSJH.H*vTLSJH/a)

    ##成果输出
    if os.path.exists(resultpath):
        os.remove(resultpath)
    fp=open(resultpath,"w")

    j,k=L1.shape
    for i in range(0,j,1):
        fp.write(str(i+1)+"\t%.4f\t%.4f\n"%(L1[i,0],(A1*X2)[i,0]))
    fp.write("总体最小二乘中误差：\t%.6f\n"%(qTLS[0,0]))
    fp.write("总体最小二乘检核中误差：\t%.6f\n"%(qTLSJH[0,0]))
    fp.close()











