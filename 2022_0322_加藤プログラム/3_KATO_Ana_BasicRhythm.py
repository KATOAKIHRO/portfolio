import Function_Processing as FP
import Function_Analysis as FA
import numpy as np

"入力部"
Name=["1115subX実験B右脚","1115subX実験B左脚","1115subX実験Bなし"]
GName=["Legs-Right","Legs-Left","None"]
usefile=[i for i in range(30)]
Samplerate=500      #サンプリング周波数
FI="OFF"
div=[2,0.2]   #[周波数分解能,時間分解能]
CurrentDirectly="C:\\Users\\appon\\PycharmProjects\\2021\\Eeg_ex\\測定データ\\2021_1115_subADE\\"
Pole=["C5","C3","C1","Cz","C2","C4","C6"]
#cretime=[1,3]
usetime=[1,4]
usepole=[0,1,2,3,4,5,6]
usefreq=np.arange(div[0],55,div[0])
Remontage=[[0,3],[1,3],[2,3],[4,3],[5,3],[6,3]]
Pole=[Pole[i] for i in usepole]

"データ整形"
def processing(fName,usefNum,utime):
    f=[]
    t=[]
    NOL=[]
    seg=Samplerate/div[0]
    ovl=seg-Samplerate*div[1]
    print("オーバーラップ率 "+str(ovl/seg))
    for fNum in usefNum:
        L = FP.csv_retrieve(CurrentDirectly, fName+str(fNum))
        CHL=[]
        for p in usepole:
            "各種フィルタ"
            ch_l = L[:,p]
            if (FI=="OFF"):
                pass
            else:
                ch_l = FP.bandpass(ch_l, Samplerate, np.array([6, 40]), np.array([2, 50]), 1, 10)
            f, t, z = FP.stft(ch_l, Samplerate, seg,ovl)
            t=np.round(t, decimals=1)
            z=np.abs(z)
            t, z = FP.tcut(t, z, utime)
            f, z = FP.fcut(f,z,usefreq)
            CHL.append(z)
        NOL.append(CHL)
    return NOL,f,t

"おまじない"
if __name__=="__main__":
    "測定-振幅スペクトル表記"
    print("測定-振幅スペクトル表記")
    D_Amp=[]
    for n in Name:
        DATA ,f, t = processing(n,usefile,usetime)
        DATA = np.transpose(DATA, (0,3,1,2)) #(試行,時間,電極,周波数)
        DATA = FP.SAA(FP.SAA(DATA))
        #P,DATA = FP.Remontage(Pole,DATA,Remontage)
        D_Amp.append(DATA)
    D_Amp=np.array(D_Amp)
    D_Amp=np.transpose(D_Amp,(1,0,2)) #(動作、電極、周波数)
    FA.dim4PLT(f, GName, Pole, D_Amp, ["Rest IMP", "Frequncy[Hz]","","Amplitude[uV/s]"], mode="multiline",zRange=[0, 5],xSpan=[0,0],zMark=[0])

    "測定-変化率表記"
    print("測定-変化率表記")
    fPLTDATA = []
    for h in range(int(len(Name))):
        cDATA, f0, t0 = processing(Name[h], usefile, cretime)
        fDATA, f1, t1 = processing(Name[h], usefile, usetime)
        cDATA = np.transpose(cDATA, (1, 2, 0, 3))  # (電極、周波数、試行、時間)
        fDATA = np.transpose(fDATA, (0, 3, 1, 2))  # (試行、時間、電極、周波数)
        ERDthre = np.std(cDATA)

        "基準値"
        zM = []
        for i in range(int(len(usepole))):
            zM_temp = []
            for j in range(int(len(f0))):
                zM_temp.append(np.median(cDATA[i][j]))
            zM.append(zM_temp)
        zM = np.array(zM)  # (電極、周波数)　の　基準値
        "変化率"
        for i in range(int(len(usefile))):
            for j in range(int(len(t1))):
                fDATA[i][j] = (fDATA[i][j] - zM) / zM  # 変化率算出
        fDATA = np.transpose(fDATA, (0, 1, 2, 3))  # (試行,時間、電極、周波数)
        print(np.shape(fDATA))
        fDATA = FP.SAA(FP.SAA(fDATA))  # (試行、時間)の2次元削減
        fPLTDATA.append(fDATA)  # 動作ごとに同期加算値を格納

    AVENUM = int(len(usefile)) * int(len(t1))  # 平均回数
    fPLTDATA = np.array(fPLTDATA)
    D = np.transpose(fPLTDATA, (1, 0, 2))  # (周波数、動作、電極)

    "周波数についてのグラフ"
    FA.dim4PLT(f1, GName, Pole, D, ["Ratio_Time"+str(usetime) + "s", "Frequency[Hz]", "", "Ratio[/(s)(Hz)]"],
               mode="multiline",zRange=[-0.2 * 3, 0.2 * 3],
               xSpan=[0,0], zMark=[-0.2, 0, 0.2])