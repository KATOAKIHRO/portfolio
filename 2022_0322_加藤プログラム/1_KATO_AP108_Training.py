# coding: UTF-8
import random
import pygame as pg
import time

interval=4 #指示インターバル[s]
exetime=300#プログラム起動時間[s]
exetime=int(exetime/interval)
tlist=[i%3 for i in range(exetime)]#指示リスト配列
random.shuffle(tlist)

"おまじない"
if __name__=="__main__":
	###pygame画面設定###
	pg.init()  # Pygameの初期化
	pg.mixer.quit()  # サウンドの無効化用
	screen = pg.display.set_mode((1500, 800))  # 1500 800の画面
	pg.display.set_caption("measurement")  # タイトルバーに表示する文字
	font = pg.font.Font("ipaexm.ttf", 100)  # フォントの設定(55px)
	Rimg=[]
	Limg=[]
	for i in range(5):#画像読み込み
		img = pg.image.load("C:./画像/右手_Moment" + str(i+1) + ".jpg")
		Rimg.append(pg.transform.scale(img, (500, 500)))
		img = pg.image.load("C:./画像/左手_Moment" + str(i+1) + ".jpg")
		Limg.append(pg.transform.scale(img, (500, 500)))
	screen.blit(Rimg[0], (900, 300))
	screen.blit(Limg[0], (130, 300))
	figtext = font.render("+", True, (255, 255, 0))
	screen.blit(figtext, [735, 240])
	pg.display.update()  # 描画処理を実行

	#プログラム内容#
	movienum=[0,1,2,3,4,3,2,1,0]#アニメデータ生成
	time.sleep(2)
	n=0
	#アニメーション実施
	for t in tlist:
		if t == 0:
			time.sleep(4)
		elif t == 1:
			for i in range(2):
				for m in movienum:
					screen.blit(Rimg[m], (900, 300))
					pg.display.update()  # 描画処理を実行
					time.sleep(0.1)
			time.sleep(2)
		elif t == 2:
			for i in range(2):
				for m in movienum:
					screen.blit(Limg[m], (130, 300))
					pg.display.update()  # 描画処理を実行
					time.sleep(0.1)
			time.sleep(2)
		else:
			for i in range(2):
				for m in movienum:
					screen.blit(Rimg[m], (900, 300))
					screen.blit(Limg[m], (130, 300))
					pg.display.update()  # 描画処理を実行
					time.sleep(0.1)
			time.sleep(2)
		n+=1
		if (n%15==0):
			print("1分経過")