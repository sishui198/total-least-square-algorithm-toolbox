# -*- coding: cp936 -*-
##����ģ��
from TLSSpecialFunction import *
import math

##��������С������Ϻ�ĵ㣬���ƫ��̫�󣬲�ȡ�Ľ���ʩ
def TLSSpecialMain(infc,TLSTolerance):
    #��ȡ�ı��ļ��������ݴ�������
    DPtxtpath=infc[0:-4]+"C.txt"
    TLStxtpath=infc[0:-4]+"D.txt"
    DpArray = ReadTxtToArray(DPtxtpath)
    TLSArray = ReadTxtToArray(TLStxtpath)

    #���ڴ�ŸĽ���
    TLSPointforInsert=[]
    TLSPointforBeforeInsert=[]
    for i in range(0,len(DpArray),1):
        #��ȡ������С������ϵ㼫���Ӧ�ĵ�����˹ѹ����ĵ㣬���������
        x1 = DpArray[i][0]
        y1 = DpArray[i][1]
        x2 = TLSArray[i][0]
        y2 = TLSArray[i][1]
        distance=math.sqrt(math.pow(x2-x1,2)+math.pow(y2-y1,2))

        #�����������޲ִ�иĽ�
        if distance >TLSTolerance :
            print distance
            print DpArray[i][2],DpArray[i][0],DpArray[i][1]
            print TLSArray[i][2],TLSArray[i][0],TLSArray[i][1]
            #�õ�����˹ѹ����ĵ����������С������ϵ�
            TLSArray[i][0]=DpArray[i][0]
            TLSArray[i][1]=DpArray[i][1]

            #�󽻵�
            CrossPointArrayBefore,CrossPointArray=GetCrossPoint(infc,TLSArray[i][2])

            ##�󽻵�
            #�жϽ���ĸ���
            if len(CrossPointArray)==1:
                print "�󽻵�",CrossPointArray[0][0],CrossPointArray[0][1]            
                TLSPointforInsert.append([CrossPointArray[0][0],CrossPointArray[0][1],TLSArray[i][2]])         
            #�����������һ��������������һ��
            elif len(CrossPointArray) > 1:
                CrossPointOnly=[]
                CrossPointOnly.append(CrossPointArray[0][0])
                CrossPointOnly.append(CrossPointArray[0][1])
                CrossPointDistance=math.sqrt(math.pow(CrossPointArray[0][0]-DpArray[i][0],2)+math.pow(CrossPointArray[0][1]-DpArray[i][1],2))            
                for j in range(1,len(CrossPointArray),1):
                    if CrossPointDistance>math.sqrt(math.pow(CrossPointArray[j][0]-DpArray[i][0],2)+math.pow(CrossPointArray[j][1]-DpArray[i][1],2)):
                        CrossPointOnly[0]=CrossPointArray[j][0]
                        CrossPointOnly[1]=CrossPointArray[j][1]
                print "�󽻵�",CrossPointOnly[0],CrossPointOnly[1]           
                TLSPointforInsert.append([CrossPointOnly[0],CrossPointOnly[1],TLSArray[i][2]])        

            #ǰ����
            if len(CrossPointArrayBefore)==1:
                print "ǰ����",CrossPointArrayBefore[0][0],CrossPointArrayBefore[0][1]            
                TLSPointforBeforeInsert.append([CrossPointArrayBefore[0][0],CrossPointArrayBefore[0][1],TLSArray[i][2]])         
            elif len(CrossPointArrayBefore) > 1:
                CrossPointOnly=[]
                CrossPointOnly.append(CrossPointArrayBefore[0][0])
                CrossPointOnly.append(CrossPointArrayBefore[0][1])
                CrossPointDistance=math.sqrt(math.pow(CrossPointArrayBefore[0][0]-DpArray[i][0],2)+math.pow(CrossPointArrayBefore[0][1]-DpArray[i][1],2))            
                for k in range(1,len(CrossPointArrayBefore),1):
                    if CrossPointDistance>math.sqrt(math.pow(CrossPointArrayBefore[k][0]-DpArray[i][0],2)+math.pow(CrossPointArrayBefore[k][1]-DpArray[i][1],2)):
                        CrossPointOnly[0]=CrossPointArrayBefore[k][0]
                        CrossPointOnly[1]=CrossPointArrayBefore[k][1]
                print "ǰ����",CrossPointOnly[0],CrossPointOnly[1]           
                TLSPointforBeforeInsert.append([CrossPointOnly[0],CrossPointOnly[1],TLSArray[i][2]])
                print "-"*30

    #�����ı��ļ����������յ�ѹ���������
    LastTLStxtpath = infc[0:-4]+"E.txt"
    if os.path.exists(LastTLStxtpath):
       os.remove(LastTLStxtpath)

    #��ӸĽ���ĵ㣬��д���ı��ļ�   
    LastTLStxtpathfp=open(LastTLStxtpath,"w")
    for i in range(0,len(TLSArray),1):
        x1=TLSArray[i][0]
        y1=TLSArray[i][1]
        index1=int(TLSArray[i][2])

        for i in range(0,len(TLSPointforBeforeInsert),1):
            if TLSPointforBeforeInsert[i][2]==index1:
                if TLSPointforBeforeInsert[i][0] < x1:
                    LastTLStxtpathfp.write(str(TLSPointforBeforeInsert[i][0])+"\t"+str(TLSPointforBeforeInsert[i][1])+"\t"+str(index1)+"\n")       
        LastTLStxtpathfp.write(str(x1)+"\t"+str(y1)+"\t"+str(index1)+"\n")
        for i in range(0,len(TLSPointforInsert),1):
            if TLSPointforInsert[i][2]==index1:
                LastTLStxtpathfp.write(str(TLSPointforInsert[i][0])+"\t"+str(TLSPointforInsert[i][1])+"\t"+str(index1)+"\n")       
    LastTLStxtpathfp.close()

##���Գ���
if __name__ == "__main__":
    infc = r"C:\Users\Administrator\Desktop\temp\result\output.txt"
    TLSSpecialMain(infc)




