# -*- coding: utf-8 -*-
import numpy as np
from PIL import Image, ImageDraw
from mana544Lib import createcolor, listprint, heightLayer, objectPoint
import matplotlib.pyplot as plt

'''
正距円筒図法に則って、正円を計算します。
【注意】
このプログラムはそもそも展開用に書いたものではないので、ドキュメント等
はありません(書く予定もありません)。従って、備忘録的に書いた各関数の
docstringを頼りに、Pythonコードを解析できる人のみ利用してください。
利用の際は、製作者は一切の責任(サポート等)を負わないものとします。
ソース(構造含む)が汚いのはご容赦を。オリジナルの再頒布は禁止しますが、
改造および改造後の公開などは自由です。その際も、製作者は一切の責任を負
わないものとします。誰か抽象化してクラスで書いてくれないかな…
説明文の中の用語とかは「全天球イラストの描き方講座」と連動していますの
で、そちらも併せて参照してください。
【動作環境(使用モジュール)】
Python(Anaconda) 3.6.4(5.1.0)
numpy 1.14.0
pillow 5.0.0

★★★★★★★
★ 設定値 ★
★★★★★★★
sphR : float
    全天球の半径 [m](1000かけて[mm]にする)
point_theta : list(int, ...)
    円を描画するときの“点”を角度で指定
circleR : float
    円の半径 [mm]
centerPoint : objectPoint
    円の中心座標を[Az, Ev]で指定
    .Az = 180
    .Ev = -80

'''
# ▼▼▼ 設定値ココカラ ▼▼▼
sphR = 1.5 * 1000
circleR = 5
centerPoint = objectPoint()
centerPoint.Az = 180
centerPoint.Ev = 0
# ▲▲▲ 設定値ココマデ ▲▲▲


def DHW2AzEv(rect):
    """
    objectPointオブジェクトのリストを
    直交座標→球面座標に一括変換して、
    Az, Evのそれぞれのリストを生成

    Parameters
    ----------
    rect : list[objectPoint, ...]
        objectPointのリスト。

    Returns
    -------
    Az : list(float)
        水平角のリスト。
    Ev : list(float)
        仰角のリスト。
    """
    Az = []
    Ev = []
    for rct in rect:
        rct.rect2sph()
        Az.append(rct.Az)
        Ev.append(rct.Ev)
    
    return Az,Ev


def createImage(CP_list, drawAzEvGrid, color):
    """
    OPを描画してPNGファイルに保存する。

    Parameters
    ----------
    wLine_Az : list(float)
        ヨコ線用水平角のリスト
    wLine_Ev : list(float)
        ヨコ線用仰角のリスト
    hLine_Az : list(float)
        タテ線用水平角のリスト
    hLine_Ev : list(float)
        タテ線用仰角のリスト
    widthCount : int
        ヨコの個数
    heightCount : int
        タテの個数
    l_heightCount : int
        ライン描画用タテ個数
    l_widthCount : int
        ライン描画用ヨコ個数

    Returns
    -------
    なし
    """
    # 画像のサイズ(width, height)
    imageSize = (5376, 2688)
    gridDivision = imageSize[0]/4
    grid = [[gridDivision, 0, gridDivision, gridDivision*2],
            [gridDivision*2, 0, gridDivision*2, gridDivision*2],
            [gridDivision*3, 0, gridDivision*3, gridDivision*2],
            [0, gridDivision, gridDivision*4, gridDivision]]
    # ベース画像(RGBモード)
    im = Image.new('RGB', imageSize, (255, 255, 255))
    draw = ImageDraw.Draw(im)
    # アルファチャンネル用画像(グレースケールモード)
    im_a = Image.new('L', imageSize, 0)
    draw_a = ImageDraw.Draw(im_a)

    if drawAzEvGrid:
        for g in grid:
            draw.line(g, fill=(200, 200, 200), width=2)
            draw_a.line(g, fill=255, width=2)

    # Az→x[px]変換係数
    x_a = (gridDivision*2) / 180
    # Ev→y[px]変換係数
    y_a = -gridDivision / 90
    y_b = gridDivision

    # ★★★★★★★★
    # ★ 線の描画 ★
    # ★★★★★★★★

    # CP_listの個数だけループ(描画する“点”の個数)
    for i in range(len(CP_list)):
        # ライン描画用ポイント初期化
        P=[]
        # 点(円)の描画ポイント個数
        for j in range(len(CP_list[i])):
            P.append(((x_a * CP_list[i][j].Az), (y_a * CP_list[i][j].Ev + y_b)))

        # draw.polygon(P, fill=color)
        # draw_a.polygon(P, fill=255)
        draw.line(P, fill=color, width=2)
        draw_a.line(P, fill=255, width=2)

    # アルファチャンネル埋め込み
    im.putalpha(im_a)

    # filename = ("vertPersGuide(%g).png" % bseObjPoint[0])
    filename = ("vertPersGuide.png")
    im.save(filename)
    print("%s 生成完了" % filename)



def calc_circlePoint(centerPoint, circleR):
    """
    円のポイント(D, H, W)を計算して返す

    Parameters
    ----------
    centerPoint : objectPoint
        円の中心ポイント
    circleR : float
        円の半径

    Returns
    -------
    circlePoint_list : (objectPoint, ...)
        円を描画するポイントリスト
    """
    point_theta = range(0, 361, 10)
    vert_circlePoint = []
    rel_circlePoint = []
    circlePoint = []
    for i in range(0,len(point_theta)):
        # vert面[W, H]に円を割り付け
        vert_circlePoint.append(objectPoint())
        vert_circlePoint[i].W = circleR * np.cos(np.deg2rad(point_theta[i]))
        vert_circlePoint[i].H = circleR * np.sin(np.deg2rad(point_theta[i]))
        # print("vert_Point[%u]: [%f, %f, %f]" % (i, vert_circlePoint[i].D, vert_circlePoint[i].H, vert_circlePoint[i].W))

        # vert面の円をEv分傾ける
        rel_circlePoint.append(objectPoint())
        rel_circlePoint[i].W = vert_circlePoint[i].W
        rel_circlePoint[i].H = vert_circlePoint[i].H * np.cos(np.deg2rad(centerPoint.Ev))
        rel_circlePoint[i].D = - vert_circlePoint[i].H * np.sin(np.deg2rad(centerPoint.Ev))
        # print("rel_Point[%u]: [%f, %f, %f]" % (i, rel_circlePoint[i].D, rel_circlePoint[i].H, rel_circlePoint[i].W))

        # 円の座標[D, H, W]を求める
        circlePoint.append(objectPoint())
        circlePoint[i].W = centerPoint.W + rel_circlePoint[i].W
        circlePoint[i].D = centerPoint.D + rel_circlePoint[i].D
        circlePoint[i].H = centerPoint.H + rel_circlePoint[i].H
        circlePoint[i].baseAz = centerPoint.baseAz
        print("circlePoint[%u]: [%f, %f, %f]" % (i, circlePoint[i].D, circlePoint[i].H, circlePoint[i].W))
    
    return circlePoint





'''
★★★★★★
★ main ★
★★★★★★
'''
# centerPoint.AzをbaseAzとして[D, H, W]を計算
centerPoint.baseAz = centerPoint.Az
centerPoint.D = sphR * np.cos(np.deg2rad(centerPoint.Ev))
centerPoint.H = sphR * np.sin(np.deg2rad(centerPoint.Ev))
centerPoint.W = 0.0
print("centerPoint: [%.2f, %.2f, %.2f]" % (centerPoint.D, centerPoint.H, centerPoint.W))


circleR = (50, 100, 250, 500, 800)
CP_list = []
for i in range(len(circleR)):
    CP_list.append(calc_circlePoint(centerPoint, circleR[i]))
    # 座標変換とリストの作成
    p_Az, p_Ev = DHW2AzEv(CP_list[i])

    print("p_Az: ", end="")
    listprint(p_Az, ".1f")
    print("")   # 改行
    print("p_Ev: ", end="")
    listprint(p_Ev, ".1f")
    print("")   # 改行
'''
CP_list : ((objectPoint, ...), ...)
    円のリスト。


'''

# createImage(CP_list, drawAzEvGrid, color)
createImage(CP_list, True, (0,0,0))

# 計算結果をささっと確認用(matplotlib使用)
# plt.plot(p_Az,p_Ev,'-')
# plt.ylim(-90, 90)
# plt.yticks(range(-90,100,30))
# plt.xlim(0, 360)
# plt.xticks(range(0,361,90))
# plt.show()


