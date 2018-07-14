# -*- coding: cp936 -*-
##����ģ��
import os
from GetCrossPoint import GetCrossPoint

##����������С���˸������飬��������ı��ļ�
def CreateTLSMatchingAssistTxt(SourcePath,TLSMatchingAssistPath):
    #����Ƿ����ͬ���ļ�
    if os.path.exists(TLSMatchingAssistPath):
       os.remove(TLSMatchingAssistPath)
    #���ļ���Ϊ��д��׼��
    TLSMatchingAssistfpr= open(SourcePath,"r")
    TLSMatchingAssistfpw= open(TLSMatchingAssistPath,"w")
    for line in TLSMatchingAssistfpr.readlines():
       if line !="-END-":
          TLSMatchingAssistfpw.writelines(str(1)+"\t"+line)
    TLSMatchingAssistfpr.close()
    TLSMatchingAssistfpw.close()

##�����㴴��ֱ�ߣ�������б�ʺͽؾ�
def CreateLineFromTwoPoint(linenumber1,linenumber2,PointSourcePath):
    #��ȡ�ı��ļ���������������
    fp= open(PointSourcePath,"r")
    indexofpoint = -1
    for line in fp.readlines():
        indexofpoint= indexofpoint+1
        if indexofpoint==linenumber1:
            x1=float(line.split('\t')[1])
            y1=float(line.split('\t')[2])
        elif indexofpoint==linenumber2:
            x2=float(line.split('\t')[1])
            y2=float(line.split('\t')[2])
    #����б�ʺͽؾ�
    k= (y2-y1)/(x2-x1)
    b=y1-k*x1
    print "a=%s,b=%s"%(k,b)
    fp.close()
    return k,b
    
##�����ı��ļ�����������Ϣ
def CreateIndexAndPointTxtAfterDouglasCompress(SourcePath,preturnpoints,pointIndexsToKeep):
    txtpath = SourcePath[0:-4]+"C.txt"
    if os.path.exists(txtpath):
       os.remove(txtpath)
       
    txtpathfp=open(txtpath,"w")
    for i in range(0,len(pointIndexsToKeep),1):
        txtpathfp.write(str(preturnpoints[i].X)+"\t"+str(preturnpoints[i].Y)+"\t"+str(pointIndexsToKeep[i])+"\n")
    txtpathfp.close()

##�����ı��ļ�����������С������Ϻ�ĵ������
def CreateTLSCrossPointTxt(SourcePath,indexandlineArrayTotal,preturnpoints):
    #�����ı��ļ���
    TLSCrossPointpath = SourcePath[0:-4]+"D.txt"
    if os.path.exists(TLSCrossPointpath):
       os.remove(TLSCrossPointpath)
       
    TLSCrossPointpathfp=open(TLSCrossPointpath,"w")
    #д���һ����
    TLSindex=0 
    TLSCrossPointpathfp.write((str(0)+"\t"+str(0)+"\t"+str(TLSindex)+"\n"))

    #д���м��
    for i in range(0,len(indexandlineArrayTotal)-1,1):
        TLSindex = TLSindex +1
        #����м�㲢д��
        TLSx,TLSy=GetCrossPoint(indexandlineArrayTotal[i][2],indexandlineArrayTotal[i][3],indexandlineArrayTotal[i+1][2],indexandlineArrayTotal[i+1][3])
        TLSCrossPointpathfp.write((str(TLSx)+"\t"+str(TLSy)+"\t"+str(TLSindex)+"\n"))
    #д�����һ����    
    TLSindex = TLSindex +1
    LastLineX = str(preturnpoints[len(preturnpoints)-1].X)
    LastLineY = str(preturnpoints[len(preturnpoints)-1].Y)
    TLSCrossPointpathfp.write(LastLineX+"\t"+LastLineY+"\t"+str(TLSindex)+"\n")   
    TLSCrossPointpathfp.close()











