#
# * フリーソフトのため、弊社でのお問い合わせ等の対応は致しかねます。ご了承ください。
#
# 本サンプルで必要なパッケージ
#
# numpy			1.18.1
#
# pip install numpy
#
#
import time
import numpy as np
import polymate.mini as pp
# 情報の表示
print('-------------------------------')
print(pp.__name__)
print(pp.__version__)
print(pp.__date__)
print(pp.__author__)
print('-------------------------------')

hPM = pp.create(500, 10, 500 * 10)
#サンプリング周波数
#-
# 電極の設定
#-
pp.setup_ele(hPM,  1, 'ELE', 1, 1000)			# nGain : 1000, 100
pp.setup_ele(hPM,  2, 'ELE', 2, 1000)			# nGain : 1000, 100
pp.setup_ele(hPM,  3, 'ELE', 3, 1000)			# nGain : 1000, 100
pp.setup_ele(hPM,  4, 'ELE', 4, 1000)			# nGain : 1000, 100
pp.setup_ele(hPM,  5, 'ELE', 5, 1000)			# nGain : 1000, 100
pp.setup_ele(hPM,  6, 'ELE', 6, 1000)			# nGain : 1000, 100
pp.setup_ele(hPM,  7, 'ELE', 7, 1000)			# nGain : 1000, 100
pp.setup_ele(hPM,  8, 'ELE', 8, 1000)			# nGain : 1000, 100
pp.setup_ele(hPM,  9, 'EXT', 1,    1, 'ON')		# nGain : 1              nPullUp : 'ON', 'OF'
pp.setup_ele(hPM, 10, 'EXT', 2,    1, 'OF')		# nGain : 1              nPullUp : 'ON', 'OF'
#9,10は脳波以外で使う,ELE…?,EXT…?
#チャンネル番号、電極の種類、電極番号、ゲイン

#抵抗値用測定
pp.setup_unit(hPM,  1, 'uV')
pp.setup_unit(hPM,  2, 'uV')
pp.setup_unit(hPM,  3, 'uV')
pp.setup_unit(hPM,  4, 'uV')
pp.setup_unit(hPM,  5, 'uV')
pp.setup_unit(hPM,  6, 'uV')
pp.setup_unit(hPM,  7, 'uV')
pp.setup_unit(hPM,  8, 'uV')
pp.setup_unit(hPM,  9, 'mV')
pp.setup_unit(hPM, 10, 'mV')

nComPort = 'COM4'		# 「デバイスとプリンター」でシリアルポートの番号を確認する

nRET = pp.open(hPM, nComPort, '19200')
#ボーレート19200

if( nRET == False ):
	print("FALSE")


#-
# 抵抗測定
#-
print( '抵抗測定' )

pp.start_impd(hPM)
nIMPD, nResult = pp.data_impd(hPM)
print(nIMPD)
print("REF,CH1,CH2,…")
pp.stop_impd(hPM)
pp.stop(hPM)
pp.close(hPM)
pp.release(hPM)



#データ同期、被験タイミング
#Bluetooth接続
#ミユキ技研