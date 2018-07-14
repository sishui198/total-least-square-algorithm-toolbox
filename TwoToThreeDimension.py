# -*- coding: cp936 -*-
##导入模块
import arcpy,os
import numpy as np

##读取文本文件，获得二维点集数组
def GetArray1(Txtpath):
    Txtpathfp=open(Txtpath,"r")
    TxtArray=[]
    index=0.0
    for TxtpathLine in Txtpathfp.readlines():
        if TxtpathLine!="-END-":
            TxtpathX=float(TxtpathLine.replace("\n","").split("\t")[0])
            TxtpathY=float(TxtpathLine.replace("\n","").split("\t")[1])
            TxtArray.append([TxtpathX,TxtpathY,index])
            index+=1
    Txtpathfp.close()
    return TxtArray

##读取文本文件，获得总体最小二乘拟合后的坐标集合
def GetArray2(Txtpath):
    Txtpathfp=open(Txtpath,"r")
    TxtArray=[]
    for TxtpathLine in Txtpathfp.readlines():
        TxtpathX=float(TxtpathLine.replace("\n","").split("\t")[0])
        TxtpathY=float(TxtpathLine.replace("\n","").split("\t")[1])
        TxtpathIndex=float(TxtpathLine.replace("\n","").split("\t")[2])
        TxtArray.append([TxtpathX,TxtpathY,TxtpathIndex])
    Txtpathfp.close()
    return TxtArray

##执行转换
def TwoToThreeDimension(infc,ArrayForOrigin):
    ##坐标文件
    Srcpath1=infc
    Srcpath2=infc[0:-4]+"C.txt"
    Srcpath3=infc[0:-4]+"E.txt"
    ##坐标数组
    Origin=GetArray1(Srcpath1)
    Dp=GetArray2(Srcpath2)
    TLS=GetArray2(Srcpath3)

    for j in range(0,len(TLS),1):
        Flag=int(TLS[j][2])
        TLS[j][2]=Dp[Flag][2]

    ##获得首尾点坐标
    #首点
    x1=ArrayForOrigin[0][0]
    y1=ArrayForOrigin[0][1]
    z1=ArrayForOrigin[0][2]
    #尾点
    x2=ArrayForOrigin[len(ArrayForOrigin)-1][0]
    y2=ArrayForOrigin[len(ArrayForOrigin)-1][1]
    z2=ArrayForOrigin[len(ArrayForOrigin)-1][2]
    ##首尾点距离
    distance_AB=np.sqrt(np.power(x2-x1,2)+np.power(y2-y1,2)+np.power(z2-z1,2))

    ##获得所有TLS垂足3维坐标
    ArrayForTLSChuiZu=[]
    for i in TLS:
        Firsta=i[1]
        Firstb=i[0]
        # 垂足坐标
        xn=(Firstb/distance_AB)*(x2-x1)+x1
        yn=(Firstb/distance_AB)*(y2-y1)+y1
        zn=(Firstb/distance_AB)*(z2-z1)+z1
        ArrayForTLSChuiZu.append([xn,yn,zn])
    ##获得所有原来坐标点垂足3维坐标
    ArrayForOriginChuiZu=[]
    for i in Origin:
        Firsta=i[1]
        Firstb=i[0]
        # 垂足坐标
        xn=(Firstb/distance_AB)*(x2-x1)+x1
        yn=(Firstb/distance_AB)*(y2-y1)+y1
        zn=(Firstb/distance_AB)*(z2-z1)+z1
        ArrayForOriginChuiZu.append([xn,yn,zn])

    ##求原来点的垂直单位向量
    ArrayForOriginVector=[]
    for i in range(0,len(ArrayForOrigin),1):
        Vectorx=ArrayForOrigin[i][0]-ArrayForOriginChuiZu[i][0]
        Vectory=ArrayForOrigin[i][1]-ArrayForOriginChuiZu[i][1]
        Vectorz=ArrayForOrigin[i][2]-ArrayForOriginChuiZu[i][2]
        VectorLength=np.sqrt(np.power(Vectorx,2)+np.power(Vectory,2)+np.power(Vectorz,2))
        ArrayForOriginVector.append([Vectorx/VectorLength,Vectory/VectorLength,Vectorz/VectorLength])


    ##保存计算结果
    Srcpath=infc[0:-4]+"F.txt"
    if os.path.exists(Srcpath):
        os.remove(Srcpath)
        
    outfp=open(Srcpath,"w")
    print x1,y1,z1
    ##写入首点
    outfp.write(str(x1)+"\t"+str(y1)+"\t"+str(z1)+"\n")
    ##循环写入中间点
    for i in range(1,len(TLS)-1,1):
        ##利用共面和向量原理，求解三维坐标
        height=abs(TLS[i][1])
        ##垂足坐标
        xm=ArrayForTLSChuiZu[i][0]
        ym=ArrayForTLSChuiZu[i][1]
        zm=ArrayForTLSChuiZu[i][2]
        ##平行向量
        Dpindex=int(TLS[i][2]-1)
        VectorA=ArrayForOriginVector[Dpindex][0]
        VectorB=ArrayForOriginVector[Dpindex][1]
        VectorC=ArrayForOriginVector[Dpindex][2]
        ##求解
        xc=xm+height*VectorA
        yc=ym+height*VectorB
        zc=zm+height*VectorC
        print xc,yc,zc
        ##写入
        outfp.write(str(xc)+"\t"+str(yc)+"\t"+str(zc)+"\n")

    ##写入最后一点
    print x2,y2,z2
    outfp.write(str(x2)+"\t"+str(y2)+"\t"+str(z2)+"\n")
    outfp.close()


















