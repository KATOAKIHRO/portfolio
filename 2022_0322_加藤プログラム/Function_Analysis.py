import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


"method"
#dim2PLT-2次元プロット
#dim3PLT-3次元プロット
#dim4PLT-4次元プロット

"dim2PLT"
def dim2PLT(hor_axis,z_data,label,mode,zRange):
    fig = plt.figure()
    fig.subplots_adjust(wspace=0.4, hspace=0.4)
    fig.suptitle(label[0], fontsize=15)
    if (mode=="plot"):
        plt.ylim(zRange)
        fig.text(0.5, 0.05, label[1], ha='center', va='center', fontsize=10)
        fig.text(0.05, 0.5, label[2], ha='center', va='center', rotation='vertical', fontsize=10)
        plt.plot(hor_axis,z_data)
        plt.show()

"dim3PLT"
#lavel=["graph_title","hor_label","ver_label","Z_label"]
#mode =["mesh","multiline","multiscat","3D","sub"]
def dim3PLT(hor_axis,ver_axis,z_data,label,mode,zRange,xSpan,zMark):
    fig = plt.figure()
    fig.subplots_adjust(wspace=0.4, hspace=0.8)
    cm = plt.get_cmap("hsv")
    if (mode=="mesh"):#メッシュマップを作成します#
        ax = fig.add_subplot(1, 2, 1)
        ax.set_ylim(zRange)
        plt.suptitle(label[0], fontsize=15)
        plt.imshow(z_data, interpolation='nearest', cmap='magma',aspect=len(hor_axis)/len(ver_axis))
        ys, xs = np.meshgrid(range(z_data.shape[0]), range(z_data.shape[1]), indexing='ij')
        plt.xticks(xs[0, ::10], hor_axis[::10])
        plt.yticks(ys[::10, 0], ver_axis[::10])
        plt.colorbar()
        plt.show()
    elif (mode=="multiline" or mode=="multiscat"):#マルチライン(ドット)で描写します#
        ax = fig.add_subplot(1, 2, 1)
        plt.suptitle(label[0], fontsize=15)
        ax.set_ylim(zRange)
        ax.axvspan(xSpan[0], xSpan[1], color='0.8')
        for h in zMark:
           ax.hlines(y=h, xmin=np.amin(hor_axis), xmax=np.amax(hor_axis),linestyles="dashed")
        fig.text(0.5, 0.05, label[1], ha='center', va='center', fontsize=10)
        fig.text(0.05, 0.5, label[3], ha='center', va='center', rotation='vertical', fontsize=10)
        for i in range(int(len(ver_axis))):
            ax.plot(hor_axis, z_data[i], color=cm(i/int(len(ver_axis))), label=str(ver_axis[i])+label[2])
        ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0, fontsize=20)
        plt.show()
    elif (mode=="3D"):#立体グラフで描写します#
        X, Y = np.meshgrid(hor_axis, ver_axis)  # x軸とy軸からグリッドデータを作成
        # ここからグラフ描画
        # フォントの種類とサイズを設定する。
        plt.rcParams['font.size'] = 14
        plt.rcParams['font.family'] = 'Times New Roman'
        plt.suptitle(label[0], fontsize=15)
        ax1 = Axes3D(fig)
        # 軸のラベルを設定する。
        ax1.set_xlabel(label[1])
        ax1.set_ylabel(label[2])
        ax1.set_zlabel(label[3])
        ax1.set_zlim(zRange[0],zRange[1])
        # データプロットする。
        ax1.plot_surface(X, Y, z_data, cmap='coolwarm')
        plt.legend()
        # グラフを表示する。
        plt.show()
    elif (mode=="sub"):#複数グラフで描写します#
        Graph=[]
        for d in range(int(len(ver_axis))):
            ax = fig.add_subplot(3, 3, d + 1)
            ax.set_ylim(zRange)
            ax.axvspan(xSpan[0], xSpan[1], color='0.8')
            for h in zMark:
                ax.hlines(y=h, xmin=np.amin(hor_axis), xmax=np.amax(hor_axis), linestyles="dashed")
            ax.set_xlabel(label[1])
            ax.set_ylabel(label[2])
            ax.set_title(ver_axis[d], fontsize=16)
            Graph.append(ax)
            Graph[d].plot(hor_axis,z_data[d])
        plt.show()
    else:
        print("正しいプロットモードを選択してください！")
        exit()

"dim4PLT"
#lavel=["graph_title","hor_label","ver_label","dep_label","Z_label"]
#mode =["mesh","multiline"] (全てグラフ複数表示スタイル)
def dim4PLT(hor_axis, ver_axis, dep_axis, z_data, label, mode, zRange,xSpan,zMark):
    fig = plt.figure()
    plt.subplots_adjust(wspace=0.4, hspace=0.6)
    plt.suptitle(label[0], fontsize=15)
    cm = plt.get_cmap("hsv")
    Graph = []
    for d in range(int(len(dep_axis))):
        ax = fig.add_subplot(int(np.sqrt(int(len(dep_axis)))+1), int(np.sqrt(int(len(dep_axis)))+1), d + 1)
        ax.set_xlabel(label[1])
        ax.set_ylabel(label[3])
        ax.set_title(dep_axis[d], fontsize=16)
        Graph.append(ax)
    if (mode == "multiline"):  # マルチライン(ドット)で描写します#
        for d in range(int(len(dep_axis))):
            Graph[d].grid(color="gray", linestyle="--")
            Graph[d].set_ylim(zRange)
            Graph[d].axvspan(xSpan[0], xSpan[1], color='0.8')
            for h in zMark:
                Graph[d].hlines(y=h, xmin=np.amin(hor_axis), xmax=np.amax(hor_axis), linestyles="dashed")
            for i in range(int(len(ver_axis))):
                Graph[d].plot(hor_axis, z_data[d][i], color=cm(i / int(len(ver_axis))), label=str(ver_axis[i]) + label[2])
        Graph[int(len(dep_axis))-1].legend(bbox_to_anchor=(1.5, 1), loc='upper left', borderaxespad=0, fontsize=20)
        plt.show()
    elif (mode == "mesh"):  #メッシュで描写します
        for d in range(int(len(dep_axis))):
            Graph[d].imshow(z_data[d], origin='lower', aspect='equal')
        plt.show()

    else:
        print("正しいプロットモードを選択してください！")
        exit()
