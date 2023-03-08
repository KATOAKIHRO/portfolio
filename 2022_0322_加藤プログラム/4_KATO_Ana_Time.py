import Function_Processing as FP
import Function_Analysis as FA
import numpy as np
import csv
import random as rd
import itertools as it

"入力部"
Name=["0126subG_Imagery_After右","0126subG_Imagery_After左","0126subG_Imagery_Afterなし"]
ActName=["Right","Left","None"]
usefile=[i for i in range(20)]
Samplerate=500      #サンプリング周波数
div=[2,0.2]   #[周波数分解能,時間分解能]
CurrentDirectly="C:\\Users\\appon\\PycharmProjects\\2021\\Eeg_ex\\測定データ\\2022_0128_subGFB\\"
Pole=["F3","F4","C3","C4","P3","P4","Cz"]
usepole=[2,3] #S…2つ(右、左)決める G…自由
Pole=[Pole[i] for i in usepole]
cretime=[1,2]
usetime=[0.4,6.6]
motortime=[3,5]
usefreq=np.arange(8,14+div[0],div[0])
ansERD=[-0.66,-1.0]

"データ整形"
def processing(fName,usefNum,utime):
    f=[]
    t=[]
    NOL=[]
    seg=Samplerate/div[0]
    ovl=seg-Samplerate*div[1]
    #print("オーバーラップ率 "+str(ovl/seg))
    for fNum in usefNum:
        L = FP.csv_retrieve(CurrentDirectly, fName + str(fNum))
        CHL = []
        for p in usepole:
            "各種フィルタ"
            ch_l = L[:, p]
            #ch_l = FP.bandpass(ch_l, Samplerate, np.array([7, 15]), np.array([2, 20]), 1, 10)
            f, t, z = FP.stft(ch_l, Samplerate, seg, ovl)
            t = np.round(t, decimals=1)
            z = np.abs(z)
            t, z = FP.tcut(t, z, utime)
            f ,z = FP.fcut(f, z, usefreq)
            CHL.append(z)
        NOL.append(CHL)
    NOL=np.array(NOL)
    return NOL, f, t

"おまじない"
if __name__=="__main__":
    tD=[]
    nD=[]
    sD=[]
    "動作ファイルごとに試行"
    for h in range(int(len(Name))):
        cDATA, f0, t0 = processing(Name[h], usefile, cretime)
        tsDATA, f1, t1 = processing(Name[h], usefile, usetime)
        nDATA, f2, t2 = processing(Name[h], usefile, motortime)
        cDATA = np.transpose(cDATA, (1, 2, 0, 3))  # (pole、freq、num、time)
        tsDATA = np.transpose(tsDATA, (0, 3, 1, 2))  # (num、time、pole、freq)
        nDATA = np.transpose(nDATA, (0, 3, 1, 2))  # (num、time、pole、freq)
        T1 = t1.tolist().index(motortime[0])
        T2 = t1.tolist().index(motortime[1])

        "基準値"
        zM = []
        for i in range(int(len(usepole))):
            zM_temp = []
            for j in range(int(len(f0))):
                zM_temp.append(np.median(cDATA[i][j]))
            zM.append(zM_temp)
        zM = np.array(zM) #(pole、freq)　の　基準値
        "変化率"
        for i in range(int(len(usefile))):
            for j in range(int(len(t1))):
                tsDATA[i][j] = (tsDATA[i][j] - zM) / zM #変化率算出
            for j in range(int(len(t2))):
                nDATA[i][j] = (nDATA[i][j] - zM) / zM #変化率算出
        tsDATA = np.transpose(tsDATA, (3, 0, 2, 1)) #(freq,num,pole、time)
        tDATA = FP.SAA(FP.SAA(tsDATA)) #(freq、num)の2次元削減
        sDATA = FP.SAA(tsDATA)  # (freq)の1次元削減
        nDATA = np.transpose(nDATA, (3, 1, 2, 0))  # (time,freq、pole、num)
        nDATA = FP.SAA(FP.SAA(nDATA))  # (時間、周波数)の2次元削減
        tD.append(tDATA)  # 動作ごとに同期加算値を格納(act,pole,time)
        nD.append(nDATA)  # 動作ごとに同期加算値を格納(act,pole,time)
        sD.append(sDATA)

    "判別率-出力"
    remSCORE=[0,0,0,0,0]
    remERD=[0,0]
    ansSCORE=[0,0,0,0,0]
    HANBETSU=[]
    d_erd = np.round(np.arange(-1.0, -0.1, 0.01), 4)
    x=d_erd
    y=d_erd
    z=[]
    for R in d_erd:
        Z = []
        for L in d_erd:
            ERDthre=[R,L]
            hanbetsu = [0, 0, 0, 0, 0]  # [閾値決定用、右、左、なし, 想起] ##出現回数リスト
            for h in range(int(len(Name))):#動作ごと
                for S in sD[h]:#同動作における試行ごと
                    flag_hanbetsu = [0, 0]
                    for i in range(int(len(usepole))):#電極ごとに閾値を超えているかどうか
                        if (all(S[i][:T1]>ERDthre[i]) and any(S[i][T1:T2]<ERDthre[i])):#指示期間中の想起検知
                            flag_hanbetsu[i] = 1
                        elif (any(S[i][:T1]<ERDthre[i])):#指示期間前の想起検知
                            flag_hanbetsu[i] = -1
                        else:#無運動検知
                            pass
                    if (flag_hanbetsu[0]==1 and flag_hanbetsu[1]==1):#最小値比較(左右どちらも入力があった場合)
                        if (np.amin(S[0][T1:T2])<np.amin(S[1][T1:T2])):
                            flag_hanbetsu[1] = 0
                        else:
                            flag_hanbetsu[0] = 0

                    if ((flag_hanbetsu[0]==1 or flag_hanbetsu[1]==1) and (h==0 or h==1)):#運動判別成功
                        hanbetsu[4] += 1/ (len(usefile)*2)

                    if (flag_hanbetsu[0]==1 and h==0):#右運動判別成功
                        hanbetsu[1] += 1/ len(usefile)

                    if (flag_hanbetsu[1]==1 and h==1):#左運動判別成功
                        hanbetsu[2] += 1/ len(usefile)

                    if (flag_hanbetsu[0]==0 and flag_hanbetsu[1]==0 and h==2):#無運動判別成功
                        hanbetsu[3] += 1/ len(usefile)

            hanbetsu[0] += (hanbetsu[1]+hanbetsu[2]+hanbetsu[3])/3
            Z.append(hanbetsu[0]*100)
            if (hanbetsu[0]>remSCORE[0]):
                remSCORE=hanbetsu
                remERD=ERDthre
            if (ERDthre==ansERD):
                ansSCORE=hanbetsu
        z.append(Z)
    print("---全体,右,左,なし,運動---")
    print("閾値決定用")
    print(remSCORE,remERD)#閾値決定数、閾値組み合わせ
    print("判別評価用")
    print(ansSCORE,ansERD)#指定閾値での判別率
    z=np.array(z)
    FA.dim3PLT(x, y, z,[Pole,"Right Threshold","Left Threshold","Percentage[%]"],mode="3D",zRange=[0,100],xSpan = [np.amin(x),np.amax(x)], zMark=[0])

    "同期加算平均-波形出力"
    "//時間についてのグラフ//"
    ERDthre=-0.3
    tD = np.array(tD)
    tPLTDATA = np.transpose(tD, (1, 0, 2))  # (pole、act、time)
    FA.dim4PLT(t1, ActName, Pole, tPLTDATA, ["Ratio_Time"+str(f1) + "[Hz]", "Time[s]", "", "Ratio[/Hz]"],
               mode="multiline",zRange=[ERDthre*2, abs(ERDthre*2)],
               xSpan=motortime, zMark=[0])
    "//試行回数についてのグラフ//"
    # nD = np.array(nD)
    # nPLTDATA = np.transpose(nD, (1, 0, 2))  # (time、act、pole)
    # FA.dim4PLT(usefile, ActName, Pole, nPLTDATA, ["Ratio_Trial"+str(f2) + "Hz", "Number[times]", "", "Ratio[/(s)(Hz)]"],
    #            mode="multiline", zRange=[ERDthre * 2, ERDthre+abs(ERDthre*4)],
    #            xSpan=[0,0], zMark=[ERDthre, 0, ERDthre+abs(ERDthre*2)])