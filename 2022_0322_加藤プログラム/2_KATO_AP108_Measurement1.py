# coding: UTF-8
import random

import polymate.mini as pp
import sys
import time
import multiprocessing
import numpy as np
import pygame as pg


"入力部"
nComPort = 'COM4'	##「デバイスとプリンター」でシリアルポートの番号を確認する
sampling = 500  	##サンプリング周波数 500 or 1000
R=40				##最大接触抵抗(kΩ)
delay_allow = 1.1 ##遅延許容倍率(1.0以上)

"ファイル関係"
ReStartPoint=0 ##途中復帰用ファイル番号
file_name = ""  	##基本ファイル名
electrude=["REF=A1","CH1=F3","CH2=F4","CH3=C3","CH4=C4","CH5=P3","CH6=P4","CH7=Cz","GND=A2"] #電極名
motor_name=["右","左","なし"] #動作タグ

"測定関係"
mtime=[3,2,2]		##[READY,MOTOR,READY] 単位は[S]
trialnum = 20		## 指示1つにおける測定回数
motor_list=[i%int(len(motor_name)) for i in range(int(trialnum*len(motor_name)))] ##指示配列
random.shuffle(motor_list) #ランダマイズ
chnum=int(len(electrude)-2) #参照電極ならびに接地電極以外の電極数
nCount=sampling*int(np.sum(mtime))

#取得値をキューに送る
def measure(nC,q):
	hPM = pp.create(sampling,chnum, nC)
	nRET = pp.open(hPM, nComPort, '19200')  ##ボーレート(通信速度)　:　19200　etc…
	if (nRET == False):
		print("FALSE")
		exit()
	# ELE端子(入力端子)
	pp.setup_ele(hPM, 1, 'ELE', 1, 1000)
	pp.setup_unit(hPM, 1, 'uV')
	pp.setup_ele(hPM, 2, 'ELE', 2, 1000)
	pp.setup_unit(hPM, 2, 'uV')
	pp.setup_ele(hPM, 3, 'ELE', 3, 1000)
	pp.setup_unit(hPM, 3, 'uV')
	pp.setup_ele(hPM, 4, 'ELE', 4, 1000)
	pp.setup_unit(hPM, 4, 'uV')
	pp.setup_ele(hPM, 5, 'ELE', 5, 1000)
	pp.setup_unit(hPM, 5, 'uV')
	pp.setup_ele(hPM, 6, 'ELE', 6, 1000)
	pp.setup_unit(hPM, 6, 'uV')
	pp.setup_ele(hPM, 7, 'ELE', 7, 1000)
	pp.setup_unit(hPM, 7, 'uV')
	#pp.setup_ele(hPM, 8, 'ELE', 8, 1000)
	#pp.setup_unit(hPM, 8, 'mV')
	# ファイル作成
	ex_num=[ReStartPoint]*int(len(motor_name))
	debug_time2=0
	for motor_num in motor_list:

		pp.start_impd(hPM)
		nIMPD, nResult = pp.data_impd(hPM)
		pp.stop_impd(hPM)
		if (max(nIMPD[0:chnum + 1]) > R):
			print('電極の接触不良です！')
			q.put(10)
			sys.exit()
		if (min(nIMPD[0:chnum + 1] < 0.1)):
			print('Bluetooth接続不良です！')
			q.put(10)
			sys.exit()
		fName = file_name + motor_name[motor_num] + str(ex_num[motor_num]) + '.TXT'
		nFile = open("C:./測定データ/" + fName, 'w')
		n=0
		flag=0
		nCtemp=nC
		#print(time.time()-debug_time2)
		time.sleep(1)
		debug_time = time.time()
		pp.start(hPM)
		while (nCtemp> 0):
			nNums = pp.nums(hPM)
			if (nNums >= 10):
				nCtemp -= nNums
				if (nCtemp < 0):
					nNums += nCtemp
				nDATAs, nNums = pp.data(hPM, nNums)

				n += int(len(nDATAs))
				if (n>=sampling*mtime[0] and flag==0):
					q.put(motor_num)
					#print(debug_time -time.time())
					flag=1
				np.savetxt(nFile, nDATAs, delimiter='\t')
		pp.stop(hPM)
		nFile.close()
		ex_num[motor_num]+=1

		if (time.time()-debug_time>sum(mtime)*delay_allow):
			print("遅延が大きすぎます！")
			print(time.time()-debug_time)
			q.put(10)
			break
	pp.close(hPM)
	pp.release(hPM)
	q.put(10)
	xFile = open("C:./測定データ/"+"RESIST"+ file_name+".TXT", 'w')
	np.savetxt(xFile,nIMPD, delimiter='\t')
	xFile.close()
	print("PROCESS1 FINISH")


def monitor(q):
	###pygame画面設定###
	pg.init()  # Pygameの初期化
	screen = pg.display.set_mode((1500, 800))  # 1000 800の画面
	pg.display.set_caption("measurement")  # タイトルバーに表示する文字
	font = pg.font.Font("ipaexm.ttf", 100)  # フォントの設定(55px)
	Rimg = []
	Limg = []
	for i in range(5):
		img = pg.image.load("C:./画像/右手_Moment" + str(i + 1) + ".jpg")
		Rimg.append(pg.transform.scale(img, (500, 500)))
		img = pg.image.load("C:./画像/左手_Moment" + str(i + 1) + ".jpg")
		Limg.append(pg.transform.scale(img, (500, 500)))
	screen.blit(Rimg[0], (900, 300))
	screen.blit(Limg[0], (130, 300))
	figtext = font.render("+", True, (255, 255, 0))
	screen.blit(figtext, [735, 240])
	movienum = [0, 1, 2, 3, 4, 4, 3, 2, 1, 0]
	pg.display.update()  # 描画処理を実行

	"起動設定時間動作"
	while True:
		sw=9
		sw=q.get()
		if sw == 0:
			#screen.fill((255, 0, 0), (850, 100, 950, 200))  # (左上x,y,横幅,縦幅)
			#pg.display.update()  # 描画処理を実行
			#time.sleep(1)
			# screen.fill((0, 0, 0), (850, 100, 950, 200))  # (左上x,y,横幅,縦幅)
			#pg.display.update()  # 描画処理を実行
			for i in range(2):
				for m in movienum:
					screen.blit(Rimg[m], (900, 300))
					pg.display.update()  # 描画処理を実行
					time.sleep(0.1)
		elif sw == 1:
			# screen.fill((255, 0, 0), (80, 100, 180, 200))  # (左上x,y,横幅,縦幅)
			# pg.display.update()  # 描画処理を実行
			# time.sleep(1)
			# screen.fill((0, 0, 0), (80, 100, 180, 200))  # (左上x,y,横幅,縦幅)
			# pg.display.update()  # 描画処理を実行
			for i in range(2):
				for m in movienum:
					screen.blit(Limg[m], (130, 300))
					pg.display.update()  # 描画処理を実行
					time.sleep(0.1)
		elif sw == 2:
			time.sleep(1)
		elif sw == 3:
			# screen.fill((255, 0, 0), (80, 100, 180, 200))  # (左上x,y,横幅,縦幅)
			# screen.fill((255, 0, 0), (850, 100, 950, 200))  # (左上x,y,横幅,縦幅)
			# pg.display.update()  # 描画処理を実行
			# time.sleep(1)
			# screen.fill((0, 0, 0), (80, 100, 180, 200))  # (左上x,y,横幅,縦幅)
			# screen.fill((0, 0, 0), (850, 100, 950, 200))  # (左上x,y,横幅,縦幅)
			# pg.display.update()  # 描画処理を実行
			for i in range(2):
				for m in movienum:
					screen.blit(Rimg[m], (900, 300))
					screen.blit(Limg[m], (130, 300))
					pg.display.update()  # 描画処理を実行
					time.sleep(0.1)
		elif (sw==10):
			break
		else:
			pass
	pg.quit()  # pygameのウィンドウを閉じる
	print("PROCESS2 FINISH")

"メイン"
if __name__=="__main__":
	q = multiprocessing.Queue()
	p1 = multiprocessing.Process(name="p1", target=measure,args=(nCount,q))
	p2 = multiprocessing.Process(name="p2", target=monitor, args=(q,))
	p1.start()
	p2.start()
	p1.join()
	p2.join()