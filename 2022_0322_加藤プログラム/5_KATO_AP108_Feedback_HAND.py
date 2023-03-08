# coding: UTF-8
import polymate.mini as pp
import multiprocessing
import numpy as np
import pygame as pg
import Function_Processing as FP
import time

"入力部"
sampling = 500  	##サンプリング周波数 500 or 1000
pole=["…","F3","F4","C3","C4","P3","P4","Cz"]
nComPort = 'COM4'	##「デバイスとプリンター」でシリアルポートの番号を確認する
div=[2,0.2]			##分解能(周波数分解能、時間分解能)
usefreq=np.arange(8,14+div[0],div[0])
usepole=[5,6] 		##[右:左] 1~8
RCth=[-0.3,-0.3]	#ERD基準[右:左]
creTime=5
ave_num=5
Time=60
fps=10
actnum=2
actinterval=4

"基本システム"
nCount=int(sampling*Time)#実行時間
seg=int(sampling/div[0])
ovl=int(seg-sampling*div[1])
hop=seg-ovl
if (hop<=0):
	exit()
#取得値をキューに送る
def measure(nC,q1):
	hPM = pp.create(sampling, int(len(pole)), nC)
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
	time.sleep(2)
	p1Count=0
	pp.start(hPM)
	while (nC> 0):
		nNums = pp.nums(hPM)
		if (nNums >= 10):
			nC -= nNums
			if (nC < 0):
				nNums += nC
			nDATAs, nNums = pp.data(hPM, nNums)
			p1Count+=int(len(nDATAs))
			#print("p1",p1Count) #遅延確認用
			q1.put(nDATAs)
	pp.stop(hPM)
	pp.close(hPM)
	pp.release(hPM)

def calculate(q1,q2):

	L = np.zeros((1, int(len(pole))))
	p2Count=0
	sw=2
	cZ_right=np.zeros((int(creTime/div[1]),int(len(usefreq))))
	cZ_left = np.zeros((int(creTime / div[1]), int(len(usefreq))))
	mZ_right = np.zeros((ave_num))
	mZ_left = np.zeros((ave_num))


	while True:
		l = q1.get()
		p2Count+=int(len(l))
		#print("p2",p2Count)	#遅延確認用
		L = np.vstack((L, l))

		if (len(L) >= seg*2):
			RC = [0, 0]
			"右手"
			f, t, z = FP.stft(L[:, usepole[0]], sampling, seg, 0)
			z = abs(z[:, 1])  # ゼロパディングを含む振幅スペクトルの破棄
			f, z = FP.fcut(f, z, usefreq)
			cZ_right = np.append(cZ_right, z)
			cZ_right = np.delete(cZ_right, 0)
			zM = FP.SAA(cZ_right)
			mZ_right = np.append(mZ_right, FP.SAA(((z - zM) / zM)))
			mZ_right = np.delete(mZ_right, 0)
			RC[0] = np.average(mZ_right)

			"左手"
			f, t, z = FP.stft(L[:, usepole[1]], sampling, seg, 0)
			z = abs(z[:, 1])  # ゼロパディングを含む振幅スペクトルの破棄
			f, z = FP.fcut(f, z, usefreq)
			cZ_left = np.append(cZ_left, z)
			cZ_left = np.delete(cZ_left, 0)
			zM = FP.SAA(cZ_left)
			mZ_left = np.append(mZ_left, FP.SAA(((z - zM) / zM)))
			mZ_left = np.delete(mZ_left, 0)
			RC[1] = np.average(mZ_left)

			if (q2.empty()):
				q2.put(RC, block=False)
			L = L[hop:, :]  # オーバーラップ処理

def monitor(q2):
	###pygame画面設定###
	###pygame画面設定###
	pg.init()  # Pygameの初期化
	screen = pg.display.set_mode((1500, 800))  # 1500 800の画面
	pg.display.set_caption("measurement")  # タイトルバーに表示する文字
	font = pg.font.Font("ipaexm.ttf", 100)  # フォントの設定(55px)
	Rimg = []
	Limg = []
	for i in range(5):
		img = pg.image.load("C:./画像/右手_Moment" + str(i + 1) + ".jpg").convert()
		Rimg.append(pg.transform.scale(img, (500, 500)))
		img = pg.image.load("C:./画像/左手_Moment" + str(i + 1) + ".jpg").convert()
		Limg.append(pg.transform.scale(img, (500, 500)))
	screen.blit(Rimg[0], (900, 300))
	screen.blit(Limg[0], (130, 300))
	figtext = font.render("+", True, (255, 255, 0))
	screen.blit(figtext, [735, 240])

	movienum = [0,1,2,3,4,4,3,2,1,0]*actnum
	vis_sw=0
	v_m=0
	TransK=0 #過渡現象用変数
	RC=[0,0]
	t=time.time()
	debugT=time.time()
	pg.display.update()  # 描画処理を実行


	while True:
		#print(time.time()-debugT)
		debugT=time.time()
		sw=2
		if (q2.empty()):
			pass
		else:
			RC=q2.get()
			TransK=0
		T=time.time()-t

		"指示"
		if (T>actinterval):
			if (vis_sw == 0):#右手
				pg.draw.circle(screen, (255, 0, 0), (1200, 200), 50)

			elif (vis_sw == 1):#左手
				pg.draw.circle(screen, (255, 0, 0), (380, 200), 50)

			else:#両手
				pg.draw.circle(screen, (255, 0, 0), (1200, 200), 50)
				pg.draw.circle(screen, (255, 0, 0), (380, 200), 50)

			v_m+=1

			if (v_m==int(len(movienum))):
				t=time.time()
				v_m=0
				vis_sw=(vis_sw+1)%3

		else:
			pg.draw.circle(screen, (0, 0, 0), (1200, 200), 50)
			pg.draw.circle(screen, (0, 0, 0), (380, 200), 50)


		"ERD-Hand"
		m = (np.array(RC)*(-100))//abs(np.array(RCth)*(-10))-TransK
		m = np.where(m < 0, 0, m)
		m = np.where(m > max(movienum), max(movienum), m)

		screen.blit(Rimg[int(m[0])], (900, 300))
		screen.blit(Limg[int(m[1])], (130, 300))


		pg.display.update()
		TransK+=1
		time.sleep(1/fps)

"おまじない"
if __name__=="__main__":
	q1 = multiprocessing.Queue()
	q2 = multiprocessing.Queue()
	p1 = multiprocessing.Process(name="p1", target=measure,args=(nCount,q1,))
	p2 = multiprocessing.Process(name="p2", target=calculate, args=(q1,q2))
	p2.daemon = True
	p3 = multiprocessing.Process(name="p3", target=monitor, args=(q2,))
	p3.daemon = True
	p1.start()
	p2.start()
	p3.start()
	p1.join()
	exit()