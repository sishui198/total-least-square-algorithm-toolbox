# -*- coding: cp936 -*-
##导入模块
import numpy as np
import scipy as Sci
import scipy.linalg
import math

##总体最小二乘拟合主函数
def TLSMatching(M):
   #获得行列数
   (p,q) = M.shape
   #系数阵
   A = M[:,0:q-1]
   #常数项
   b = M[:,-1]
   #获得系数阵行列数
   (m,n) = A.shape
   #构造矩阵，QR分解
   C = np.concatenate((A,b),1)
   [Q,R] = Sci.linalg.qr(C)
   CR = R[1:,1:]
   # 奇异值分解简称（SVD）
   U1, S1, Vh = Sci.linalg.svd(CR)
   N1 = Vh.T
   # 求LSTLS参数
   a0 = np.matrix(0)
   a1 = np.concatenate((a0,Sci.zeros((1,n-1))),1)
   a2 = np.concatenate((Sci.zeros((n-1,1)),Sci.eye(n-1)),1)
   a3 = np.concatenate((a1,a2),0)
   xLSTLS =(A.H*A-math.pow(S1[n-1,],2)*a3).I*A.H*b
   print "a=%s,b=%s"%(xLSTLS[1,0],xLSTLS[0,0])
   return xLSTLS[1,0],xLSTLS[0,0]
