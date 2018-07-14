# -*- coding: cp936 -*-
##����ģ��
import numpy as np
import scipy as Sci
import scipy.linalg
import math

##������С�������������
def TLSMatching(M):
   #���������
   (p,q) = M.shape
   #ϵ����
   A = M[:,0:q-1]
   #������
   b = M[:,-1]
   #���ϵ����������
   (m,n) = A.shape
   #�������QR�ֽ�
   C = np.concatenate((A,b),1)
   [Q,R] = Sci.linalg.qr(C)
   CR = R[1:,1:]
   # ����ֵ�ֽ��ƣ�SVD��
   U1, S1, Vh = Sci.linalg.svd(CR)
   N1 = Vh.T
   # ��LSTLS����
   a0 = np.matrix(0)
   a1 = np.concatenate((a0,Sci.zeros((1,n-1))),1)
   a2 = np.concatenate((Sci.zeros((n-1,1)),Sci.eye(n-1)),1)
   a3 = np.concatenate((a1,a2),0)
   xLSTLS =(A.H*A-math.pow(S1[n-1,],2)*a3).I*A.H*b
   print "a=%s,b=%s"%(xLSTLS[1,0],xLSTLS[0,0])
   return xLSTLS[1,0],xLSTLS[0,0]
