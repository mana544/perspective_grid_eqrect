# -*- coding: utf-8 -*-
import numpy as np
from PIL import Image, ImageDraw
from mana544Lib import createcolor, listprint, heightLayer
# import matplotlib.pyplot as plt


'''
正距円筒図法に則った垂直面のパースガイド(グリッド)を計算して、PNG画像を
生成・描画します。
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

bseAz : float
    ベースの方位角。基点のOPが向いている方向
    0 <= bseAz < 360[度]で指定。
bseEv : float
    垂直面の傾斜角。-90.0 < bseEv < 90.0[度]で指定。
    水平面と垂直にしたければ、0.0を指定。
    プラスだと上端が手前に、マイナスだと上端が奥側に傾いた面を生成します。
bseObjPoint : list
    基点のOPの位置(距離)。
    [D,H,W]で指定。
    D : float
        SPからOPまでの前進距離。前進方向がプラス。D > 0 で指定のこと！
    H : float
        SPの水平面からの高さ。上方向がプラス。下方向がマイナス。
    W : float
        SPの垂直面からの横方向の距離。右方向がプラス。左方向がマイナス。
widthDivision : float
    bseObjPointから横方向の格子点間隔。
    プラスだとSPから見て右方向に、マイナスだと左方向に生成。
widthCount : int
    横方向の格子点の数。正の整数で指定。
heightDivision : float
    bseObjPointから縦方向の格子点間隔。
    プラスだとSPから見て上方向に、マイナスだと下方向に生成。
heightCount : int
    縦方向の格子点の数。正の整数で指定。
'''
# ▼▼▼ 設定値ココカラ ▼▼▼
bseAz = 165.0
bseEv = 30.0
bseObjPoint = [10.0, 5.7735026918962576450914878050196, 0.0]
widthDivision = 1.0
widthCount = 4
heightDivision = -1.0
heightCount = 7
drawObjPoint = False
drawAzEvGrid = False
guideColor = (0, 0, 0)
# ▲▲▲ 設定値ココマデ ▲▲▲

def rect2sph(rect,bseAz=0.0):
    '''
    直交座標系(D, H, W)から球面座標系(Az, Ev)への変換

    Parameters
    ----------
    rect : list
        直交座標系のオブジェクトポイント。[D,H,W]で指定。
        D:float   SPから見た奥行き。前進方向が＋。D > 0 で指定のこと！
        H:float   SPのアイレベルからの垂直距離。上方向が＋
        W:float   SPの垂線からの水平距離。右方向が＋
    bseAz : float
        ベース方位角。指定しない場合は0.0。

    Returns
    -------
    sph : list
        球面座標。[Az, Ev]で返る。
        Az:float   方位角。相対方位角にbseAzが足されます。
        Ev:float   仰角
    '''
    D=rect[0]
    H=rect[1]
    W=rect[2]

    # 相対方位角 + ベース方位角
    az = np.rad2deg(np.arctan(W/D)) + bseAz

    # 斜辺
    hyp = np.sqrt(D**2 + W**2)

    # 仰角
    ev = np.rad2deg(np.arctan(H/hyp))

    sph = [az,ev]
    return sph

def makeVertGridPoint(bseObjPoint, widthDivision, widthCount, heightDivision, heightCount, bseEv=0.0):
    '''
    SPに相対する垂直な格子点を作成

    Parameters
    ----------
    bseObjPoint : list(float)
        基点のオブジェクトポイント(OP)。
        [D,H,W]で指定。
        D > 0 で指定のこと！
    widthDivision : float
        bseObjPointから横方向の格子点間隔。
        プラスだとSPから見て右方向に、マイナスだと左方向に生成。
    widthCount : int
        横方向の格子点の数。正の整数で指定。
    heightDivision : float
        bseObjPointから縦方向の格子点間隔。
        プラスだとSPから見て上方向に、マイナスだと下方向に生成。
    heightCount : int
        縦方向の格子点の数。正の整数で指定。
    bseEv : float
        垂直面の傾斜角を[度]で指定。
        水平面と垂直にしたければ、0.0を指定。
        プラスだと上端が手前に、マイナスだと上端が奥側に傾いた垂直面を生成します。
    
    Returns
    -------
    rectList : list
        [[D1,H1,W1], ... ,[Dn,Hn,Wn]]
        n = widthCount x heightCount
        格子点の座標を上記フォーマットで返します。
    '''

    rectList = []

    for iHeight in range(heightCount):
        for iWidth in range(widthCount):
            D = bseObjPoint[0] - iHeight * heightDivision * np.sin(np.deg2rad(bseEv))
            W = bseObjPoint[2] + iWidth * widthDivision
            H = bseObjPoint[1] + iHeight * heightDivision * np.cos(np.deg2rad(bseEv))
            
            rectList.append([D,H,W])
    return rectList


def createImage(Az, Ev, wLine_Az, wLine_Ev, hLine_Az, hLine_Ev, widthCount, heightCount, l_heightCount, l_widthCount, drawObjPoint, drawAzEvGrid, color):
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
    # ★ 点の描画 ★
    # ★★★★★★★★
    if drawObjPoint:
        # 点の大きさ
        size = 20
        for i in range(len(Az)):
            P = ((x_a*Az[i])-size/2,
                (y_a*Ev[i]+y_b)-size/2,
                (x_a*Az[i])+size/2,
                (y_a*Ev[i]+y_b)+size/2)

            draw.ellipse(P, fill=color)
            draw_a.ellipse(P, fill=255)

    # ★★★★★★★★★★
    # ★ ヨコ線の描画 ★
    # ★★★★★★★★★★
    # 線の本数
    for i in range(heightCount):
        # ライン描画用ポイント初期化
        # [[x1,x2],[x1,x2],...,[xn,xn]]
        P=[]

        # 1本あたりのポイントの数
        for j in range(l_widthCount):
            k = i * l_widthCount + j
            P.append(((x_a*wLine_Az[k]), (y_a*wLine_Ev[k]+y_b)))

        draw.line(P, fill=color, width=3)
        draw_a.line(P, fill=255, width=3)

    # ★★★★★★★★★★
    # ★ タテ線の描画 ★
    # ★★★★★★★★★★
    # 線の本数
    for i in range(widthCount):
        # ライン描画用ポイント初期化
        # [[x1,x2],[x1,x2],...,[xn,xn]]
        P=[]

        # 1本あたりのポイントの数
        for j in range(l_heightCount):
            k = i  + j * widthCount
            P.append(((x_a*hLine_Az[k]), (y_a*hLine_Ev[k]+y_b)))

        draw.line(P, fill=color, width=3)
        draw_a.line(P, fill=255, width=3)

    # アルファチャンネル埋め込み
    im.putalpha(im_a)

    filename = ("vertPersGuide(%g).png" % bseObjPoint[0])
    im.save(filename)
    print("%s 生成完了" % filename)

def DHW2AzEv(rect,bseAz=0.0):
    """
    直交座標リストを球面座標に一括変換

    Parameters
    ----------
    rect : list
        [[D1,H1,W1], ... ,[Dn,Hn,Wn]]
        n = widthCount x heightCount
        直交座標のリスト。
    bseAz : float
        ベース方位角

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
        a = rect2sph(rct,bseAz)
        Az.append(a[0])
        Ev.append(a[1])
    
    return Az,Ev

def vert_plane():
    '''

    '''
    # Az = 2°間隔で widthDivision を仮計算して
    # 「ヨコ線」描画のためのwidthCountを計算
    kariDivision = bseObjPoint[0] * np.tan(np.deg2rad(2))
    l_widthCount = int(widthDivision * (widthCount-1) / kariDivision)
    l_widthDivision = widthDivision * (widthCount-1) / l_widthCount
    l_widthCount = 1 + l_widthCount
    print("l_widthCount {0}".format(l_widthCount))
    print("l_widthDivision {0}".format(l_widthDivision))


    # 「タテ線」描画のためのheightCountを計算
    l_heightCount = int(heightDivision * (heightCount-1) / kariDivision)
    if l_heightCount < heightCount:
        print("heightCountを元に戻します。")
        l_heightCount = heightCount

    l_heightDivision = heightDivision * (heightCount-1) / l_heightCount
    l_heightCount = 1 + l_heightCount
    print("l_heightCount {0}".format(l_heightCount))
    print("l_heightDivision {0}".format(l_heightDivision))


    # 「点」のリスト
    p_rectList = makeVertGridPoint(bseObjPoint, widthDivision, widthCount, heightDivision, heightCount, bseEv)
    print("点の座標[D, H, W]: ", end="")
    for i, item in enumerate(p_rectList):
        if i!=0:
            print(", ", end="")
        listprint(item, ".1f")
    print("")   # 改行
    
    # 座標変換
    p_Az, p_Ev = DHW2AzEv(p_rectList,bseAz)

    print("p_Az: ", end="")
    listprint(p_Az, ".1f")
    print("")   # 改行
    print("p_Ev: ", end="")
    listprint(p_Ev, ".1f")
    print("")   # 改行


    # 「ヨコ線」のリスト
    wl_rectList = makeVertGridPoint(bseObjPoint, l_widthDivision, l_widthCount, heightDivision, heightCount, bseEv)
    # print("ヨコ線の座標: ", end="")
    # print(wl_rectList)
    # 座標変換
    wl_Az, wl_Ev = DHW2AzEv(wl_rectList,bseAz)

    # 「タテ線」のリスト
    hl_rectList = makeVertGridPoint(bseObjPoint, widthDivision, widthCount, l_heightDivision, l_heightCount, bseEv)
    # print("タテ線の座標: ", end="")
    # print(hl_rectList)
    # 座標変換
    hl_Az, hl_Ev = DHW2AzEv(hl_rectList,bseAz)


    # 計算結果をささっと確認用(matplotlib使用)
    '''
    plt.plot(Az,Ev,linestyle='None',marker='.')
    plt.ylim(-90, 90)
    plt.yticks(range(-90,100,30))
    plt.xlim(0, 360)
    plt.xticks(range(0,361,90))
    plt.show()
    '''

    # 座標変換の結果をプロットして画像保存(pillow使用)
    createImage(p_Az, p_Ev, wl_Az, wl_Ev, hl_Az, hl_Ev, widthCount, heightCount, l_heightCount, l_widthCount, drawObjPoint, drawAzEvGrid, guideColor)


# ★★★★★★
# ★ main ★
# ★★★★★★
print("Vertical Plane パースガイド生成")
print("***********************************************")
print("depth=%g, color=" % (bseObjPoint[0]), end="")
print(guideColor)
vert_plane()
print("処理が全部終わりました。")
