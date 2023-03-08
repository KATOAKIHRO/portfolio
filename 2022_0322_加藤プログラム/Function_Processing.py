import numpy as np
import pandas as pd
import scipy.signal
import math

"method"
#csvファイルの取り込み
#バンドパスフィルタ
#ノッチストップフィルタ
#STFT
#データ抽出
#同期加算平均
#リモンタージュ

"csvファイルの取りこみ"
#(ファイル保存場所、ファイル名)
def csv_retrieve(cd,file_name):
    f_name = file_name+".TXT"
    lst = pd.read_csv(cd+f_name, sep='\t', header=None).values.tolist()
    l = np.array(lst)
    return l

"バンドパスフィルタ"
#(時系列1次元振幅データ,サンプリングレート,[通過域端周波数],[阻止域端],[通過域減衰量],[阻止域減衰量])
def bandpass(x, samplerate, fp, fs, gpass, gstop):
    fn = samplerate / 2
    wp = fp / fn
    ws = fs / fn
    N, Wn = scipy.signal.buttord(wp, ws, gpass, gstop)
    b, a = scipy.signal.butter(N, Wn, "band")
    y = scipy.signal.filtfilt(b, a, x)
    #print("バターワース次数"+str(N))
    #print("バターワース分子係数",b)
    #print("バターワース分母係数",a)
    return y

"ノッチフィルタ"
#(時系列1次元振幅データ,サンプリングレート,[通過域端周波数],[阻止域端],[通過域減衰量],[阻止域減衰量])
def bandstop(x, samplerate, fp, fs, gpass, gstop):
    fn = samplerate / 2
    wp = fp / fn
    ws = fs / fn
    N, Wn = scipy.signal.buttord(wp, ws, gpass, gstop)
    b, a = scipy.signal.butter(N, Wn, "bandstop")
    y = scipy.signal.filtfilt(b, a, x)
    # print("バターワース次数"+str(N))
    # print("バターワース分子係数",b)
    # print("バターワース分母係数",a)
    return y

"STFT"
#(1次元時系列リスト,サンプリング周波数,セグメントのサンプル数,オーバーラップしているサンプル数)
def stft(data,samplerate,segment,overlap):
    f, t, Zxx = scipy.signal.stft(data, fs=samplerate, nperseg=segment,noverlap = overlap,window="hann")
    return f,t,Zxx

"時間抽出"
def tcut(t,data,cuttime):
    t_ind1 = int((cuttime[0] - t[0]) / (t[1] - t[0]))
    t_ind2 = int((cuttime[1] - t[0]) / (t[1] - t[0]))+1
    newt = t[t_ind1:t_ind2]
    newdata = data[:,t_ind1:t_ind2]
    return newt,newdata

"周波数抽出"
def fcut(f,data,cutfreq):
    newdata=[]
    newf=cutfreq
    for cutf in cutfreq:
        newdata.append(data[f.tolist().index(cutf)])
    return newf,newdata

"同期加算平均" ##先頭の次元に試行ごとのデータを入れてください。
def SAA(datalist):
    DATALIST=np.array(datalist)
    num=int(len(datalist))
    newlist=DATALIST[0]/num
    for i in range(num):
        newlist+=DATALIST[i]/num
    newlist-=DATALIST[0]/num#重複した1番目のデータの削除
    return newlist

"リモンタージュ"   ##dataはnumpy配列かつ先頭の次元が電極である必要があります
def Remontage(pole,data,montage):
    DATA=[]
    newpole=[]
    for i in range(int(len(montage))):
        DATA.append(data[montage[i][0]]-data[montage[i][1]])
        newpole.append(pole[montage[i][0]]+"-"+pole[montage[i][1]])
    return newpole,DATA

