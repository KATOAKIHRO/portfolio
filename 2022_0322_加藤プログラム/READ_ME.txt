【ファイル説明】
・使用する順番で番号を振っています．その流れで実験で使うと楽だと思います．
・基本的にソースコード上部にある変数をいじれば動作します．

(0).時間に対して3つの指示を，タイムチャートで表現し，脳波記録します．テストにおすすめ．
(0).抵抗値確認だけを行うファイルです．電極設置時に使用．
(1).ただ動画が流れるだけのファイルです．テストに使用．
(2).実験指示動画(手の掌握)を流し，脳波記録します.

(3).解析用ファイル．周波数解析をしてプロットします(活性化している周波数帯を選択するために使っていました)．
(4).解析用ファイル．時間軸で変化率をプロットします(多分)．いっぱい書き換えてください．

(5).ニューロフィードバック用のファイル．BARはERDバー．HANDは，脳波解析による操作．
マルチプロセス3つ使っているので，CPUコア3つないと動かないから注意．

(F_A).解析やプロットのメソッドを集めたファイルです．頻繁に使うものはここに入れてます．
(F_P).前処理系のメソッドを集めたファイルです．頻繁に使うものはここに入れてます．


【拡張】
・classは使っていません．コード綺麗にできそうならお掃除お願いします．
・配列がかなり厄介です．ごめんなさい，手元で整理して考えるなどして扱ってください．
・瞬目除去も必要であれば導入してください！(試行回数50回設定の場合，瞬目なし50回取れるまで
実施する等．その際，除去ファイルもデバッグ用に取っておくと吉．)
・卒論付近で後先考えずコードをいじったので，バグが多いかもしれません．