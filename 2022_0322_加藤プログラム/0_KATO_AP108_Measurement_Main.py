# coding: UTF-8
import random
import time
import polymate.mini as pp
import pygame
import sys
import numpy as np

"""基本入力部分だよ！！！！！！！"""
"システム関係"
R = 40		##スレッショルド抵抗値
nComPort = 'COM4'	##「デバイスとプリンター」でシリアルポートの番号を確認する

"ファイル関係"
ReStartPoint=0 ##途中復帰用ファイル番号
file_name = "tinpo"  	##基本ファイル名
electrude=["REF=A1","CH1=C5","CH2=C3","CH3=C1","CH4=Cz","CH5=C2","CH6=C4","CH7=C6","GND=A2"] #電極名
motor_name=[""] #動作タグ

"測定関係"
cdtime=3			##カウントダウンの時間
mtime=[3,2,2]		##[タイムチャート1,タイムチャート2,タイムチャート3] 単位は[S]
sampling = 500  	##サンプリング周波数 500 or 1000
trialnum = 3
##1種類の動作の取得数
chnum=7			##使用チャンネル数

#おまじない
nCount = sampling*sum(mtime)
hPM = pp.create(sampling, chnum, nCount)

#ELE端子(入力端子)
pp.setup_ele(hPM,  1, 'ELE', 1, 1000)
pp.setup_unit(hPM,  1, 'uV')
pp.setup_ele(hPM,  2, 'ELE', 2, 1000)
pp.setup_unit(hPM,  2, 'uV')
pp.setup_ele(hPM,  3, 'ELE', 3, 1000)
pp.setup_unit(hPM,  3, 'uV')
pp.setup_ele(hPM,  4, 'ELE', 4, 1000)
pp.setup_unit(hPM,  4, 'uV')
pp.setup_ele(hPM,  5, 'ELE', 5, 1000)
pp.setup_unit(hPM,  5, 'uV')
pp.setup_ele(hPM,  6, 'ELE', 6, 1000)
pp.setup_unit(hPM,  6, 'uV')
pp.setup_ele(hPM,  7, 'ELE', 7, 1000)
pp.setup_unit(hPM,  7, 'uV')
#pp.setup_ele(hPM,  8, 'ELE', 8, 1000)
#pp.setup_unit(hPM,  8, 'mV')

#EXT(出力端子)
#pp.setup_ele(hPM,  9, 'EXT', 1,    1, 'ON')
#pp.setup_ele(hPM, 10, 'EXT', 2,    1, 'OF')
#pp.setup_unit(hPM,  9, 'mV')
#pp.setup_unit(hPM, 10, 'mV')

"""システム処理部だよ！！！"""
##ポート開放##
nRET = pp.open(hPM, nComPort, '19200')  ##ボーレート(通信速度)　:　19200　etc…

###pygame画面設定###
pygame.init()                                   # Pygameの初期化
screen = pygame.display.set_mode((1500, 800))    # 1000 800の画面
pygame.display.set_caption("measurement")              # タイトルバーに表示する文字
font = pygame.font.Font("ipaexm.ttf", 100)               # フォントの設定(55px)

### 抵抗測定 ###
def resistance():
	pp.start_impd(hPM)
	nIMPD, nResult = pp.data_impd(hPM)
	pp.stop_impd(hPM)
	print(nIMPD[0:chnum+1])
	if (max(nIMPD[0:chnum+1]) > R):
		print('電極の接触不良です！')
		close()
	if (min(nIMPD[0:chnum+1]<0.1)):
		print('Bluetooth接続不良です！')
		close()
	print( '抵抗測定終了' )

###pygame＆polymate＆システム終了
def close():
	pp.close(hPM)
	pp.release(hPM)
	pygame.display.quit()
	pygame.quit()
	sys.exit()

"""実験プログラムはここからだよ！！！"""
###連番リスト
motor_list = [i%(int(len(motor_name))) for i in range(trialnum*int(len(motor_name)))]

###カウントダウン###
def countdown(tnum,mnum):
	for i in range(cdtime):
		screen.fill((255, 255, 255))
		##カウントダウン
		word=str(cdtime-i)+"秒"+str(tnum)+"回目"
		text1 = font.render(word, True, (0, 0, 0))  # 描画する文字列の設定
		screen.blit(text1, [580, 270])  # 文字列の表示位置
		##動作指示
		text2 = font.render(motor_name[mnum], True, (255, 0, 0))
		screen.blit(text2, [660, 350])
		##更新
		pygame.display.update()
		time.sleep(1)

###白色インジケータ
def indicator_float(t):
	pygame.draw.line(screen, (0, 0, 0), (t, 440), (t, 410),3)
	pygame.display.update()

###測定###
def measurement(nC,motor_num,ex_num,sumnum):
	resistance()
	countdown(sumnum,motor_num)
	debug_time=time.time()
	i=1
	n=0
	t=0

	#画面設定
	screen.fill((255, 255, 255))
	screen.fill((255, 255, 0), (400+50*(mtime[0]*2), 410, 50*(mtime[1]*2), 30))#(左上x,y,横幅,縦幅)
	indicator_float(400)
	pygame.display.update()

	# ファイル作成
	fName = file_name +motor_name[motor_num]+str(ex_num) + '.TXT'
	nFile = open("C:./測定データ/" + fName, 'w')

	#測定開始
	pp.start(hPM)
	while(nC > 0):
		nNums = pp.nums(hPM)
		#0.5秒間隔でインジケータが動く
		if(n - t >= sampling/2):
			t=n
			indicator_float(i * 50 + 400)
			i += 1

		if( nNums >= 10 ):
			nC -= nNums
			if( nC < 0 ):
				nNums += nC
			nDATAs, nNums = pp.data( hPM, nNums )
			n+=int(len(nDATAs))
			np.savetxt(nFile, nDATAs, delimiter='\t')
	screen.fill((255, 255, 255))
	text2 = font.render("REST", True, (0, 0, 0))
	screen.blit(text2, [660, 350])
	pygame.display.update()
	pp.stop(hPM)
	nFile.close()
	mResulttime=time.time() - debug_time
	if(mResulttime>(sum(mtime)*1.5)):
		print("測定遅延時間が大きすぎます")
		pp.close(hPM)
		pp.release(hPM)
		sys.exit()
	return mResulttime

def main():
	mCountlist=np.zeros(int(len(motor_name)))
	RTave=0
	for m in motor_list:
		resistance()
		RT=measurement(nCount, int(m), int(mCountlist[m]+ReStartPoint),sum(mCountlist))
		mCountlist[m]+=1
		RTave+=RT/len(motor_list)

	#実行環境出力と終了処理
	mFile = open("C:./測定データ/" + "_ファイル形式" + file_name + ".txt", 'w')
	pp.start_impd(hPM)
	nIMPD, nResult = pp.data_impd(hPM)
	pp.stop_impd(hPM)
	textdata=[str(electrude),"\n",str(nIMPD),"\n",str(sampling),"\n","チャート時間"+str(mtime),"\n","実測定時間"+str(RTave)]
	mFile.writelines(textdata)
	mFile.close()
	close()

"おまじない"
if __name__=="__main__":
	main()