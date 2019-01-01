# -*- coding: utf-8 -*-
import numpy as np
from PIL import Image, ImageDraw
from mana544Lib import createcolor, listprint, heightLayer
# import matplotlib.pyplot as plt

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

def makeHorzGridPoint(bseObjPoint, widthDivision, widthCount, depthDivision, depthCount):
    '''
    SPに対して水平な格子点を作成

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
    depthDivision : float
        bseObjPointから奥行き方向の格子点間隔。
        プラスだとSPから見て奥方向に、マイナスだと手前方向に生成。
        だけど、depthがSPと重なると正接の計算ができないので
        基本はプラスに指定した方が無難です。
    depthCount : int
        奥行き方向の格子点の数。正の整数で指定。

    Returns
    -------
    rectList : list
        [[D1,H1,W1], ... ,[Dn,Hn,Wn]]
        n = widthCount x depthCount
        格子点の座標を上記フォーマットで返します。
    '''

    rectList = []

    for iDepth in range(depthCount):
        for iWidth in range(widthCount):
            D = bseObjPoint[0]+iDepth*depthDivision
            W = bseObjPoint[2]+iWidth*widthDivision
            H = bseObjPoint[1]

            if D == 0:
                print("D=0の検出: D=0は正接の計算ができないので、[%g, %g, %g]のOPはとばします。" % (D,H,W))
            else:
                rectList.append([D,H,W])
    return rectList

def createImage(Az, Ev, wLine_Az, wLine_Ev, hLine_Az, hLine_Ev, widthCount, depthCount, l_depthCount, l_widthCount, drawObjPoint, drawAzEvGrid, color, bseObjPoint):
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
    depthCount : int
        奥行きの個数
    l_depthCount : int
        ライン描画用奥行き個数
    l_widthCount : int
        ライン描画用ヨコ個数

    Returns
    -------
    なし
    """
    # 画像のサイズ(width, height)
    imageSize = (5376, 2688)
    # 90°のピクセル数
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
    for i in range(depthCount):
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
        for j in range(l_depthCount):
            k = i  + j * widthCount
            P.append(((x_a*hLine_Az[k]), (y_a*hLine_Ev[k]+y_b)))

        draw.line(P, fill=color, width=3)
        draw_a.line(P, fill=255, width=3)

    # アルファチャンネル埋め込み
    im.putalpha(im_a)

    filename = ("horzPersGuide(%g).png" % bseObjPoint[1])
    im.save(filename)
    print("%s 生成完了" % filename)

def DHW2AzEv(rect,bseAz=0.0):
    """
    直交座標リストを球面座標に一括変換

    Parameters
    ----------
    rect : list
        [[D1,H1,W1], ... ,[Dn,Hn,Wn]]
        n = widthCount x depthCount
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

def horz_plane(bseAz, bseObjPoint, widthDivision, widthCount, depthDivision, depthCount, drawObjPoint, drawAzEvGrid, color):
    """
    水平面のパースガイド生成

    Parameters
    ----------

    Returns
    -------

    """

    # Az = 2°間隔で widthDivision を仮計算して
    # 「ヨコ線」描画のためのwidthCountを計算
    kariDivision = bseObjPoint[0] * np.tan(np.deg2rad(2))
    l_widthCount = int(widthDivision * (widthCount-1) / kariDivision)
    l_widthDivision = widthDivision * (widthCount-1) / l_widthCount
    l_widthCount = 1 + l_widthCount
    print("l_widthCount {0}".format(l_widthCount))
    print("l_widthDivision {0}".format(l_widthDivision))


    # 「タテ線」描画のためのdepthCountを計算
    l_depthCount = int(depthDivision * (depthCount-1) / kariDivision)
    if l_depthCount <= depthCount:
        print("depthCountを元に戻します。")
        l_depthCount = depthCount

    l_depthDivision = depthDivision * (depthCount-1) / l_depthCount
    l_depthCount = 1 + l_depthCount
    print("l_depthCount {0}".format(l_depthCount))
    print("l_depthDivision {0}".format(l_depthDivision))


    # 「点」のリスト
    p_rectList = makeHorzGridPoint(bseObjPoint, widthDivision, widthCount, depthDivision, depthCount)
    # 座標変換
    p_Az, p_Ev = DHW2AzEv(p_rectList,bseAz)

    print("p_Az: ", end="")
    listprint(p_Az, ".1f")
    print("")   # 改行
    print("p_Ev: ", end="")
    listprint(p_Ev, ".1f")
    print("")   # 改行

    # 「ヨコ線」のリスト
    wl_rectList = makeHorzGridPoint(bseObjPoint, l_widthDivision, l_widthCount, depthDivision, depthCount)
    # print("{0}".format(wl_rectList))
    # 座標変換
    wl_Az, wl_Ev = DHW2AzEv(wl_rectList,bseAz)
    # print("p_Az {0}".format(wl_Az))

    # 「タテ線」のリスト
    hl_rectList = makeHorzGridPoint(bseObjPoint, widthDivision, widthCount, l_depthDivision, l_depthCount)
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
    createImage(p_Az, p_Ev, wl_Az, wl_Ev, hl_Az, hl_Ev, widthCount, depthCount, l_depthCount, l_widthCount, drawObjPoint, drawAzEvGrid, color, bseObjPoint)

def horz_plane_pers_grid(bseAz, bseObjPoint, widthDivision, widthCount, depthDivision, depthCount, heightList, drawObjPoint, drawAzEvGrid, guideColor):
    '''
    ★★★★★★★★★★★★★★
    ★ 水平パース面生成の ★
    ★ エントリーポイント ★
    ★★★★★★★★★★★★★★

    Parameters
    ----------
    bseAz : float
        ベースの方位角。0 <= bseAz < 360[度]で指定。
    bseObjPoint : list[D, 0.0, W]
        ベースObject Point
        D: float
            SPからOPまでの前進距離。前進方向がプラス。D > 0 で指定のこと。
        W: float
            SPの垂直面からの横方向の距離。右方向がプラス。左方向がマイナス。
    widthDivision : float
        ベースObject Pointから横方向の格子点間隔。プラスだとSPから見て右方向に、マイナスだと左方向に生成。
    widthCount : int
        横方向の格子点の数。正の整数で指定。必ず1以上を指定のこと。
    depthDivision : float
        ベースObject Pointから奥行き方向の格子点間隔。
        プラスだとSPから見て奥方向に、マイナスだと手前方向に生成。
        だけど、D=0があると(SPと重なると)正接の計算ができないので基本はプラスに指定した方が無難です。
    depthCount : int
        奥行き方向の格子点の数。正の整数で指定。必ず1以上を指定のこと。
    heightList : list[float(, float...)]
        基点のOPの位置(距離)。SPの水平面からの縦方向の距離。
        上方向がプラス。下方向がマイナス。
    drawObjPoint : Boolean
        OPの“点”を描画するかどうか。通常はなくてもいい気がする。
    drawAzEvGrid : Boolean
        PNG画像内に正距円筒図法の正方グリッドを描画するかどうか。
        TrueでAz=(0, 90, 180, 270, 360), Ev=(-90, 0, 90) の位置にグレーのラインが描画されます。
    guideColor : tuple(int, int, int)
        パースガイドの色をRGB値で指定。
        空tupleを指定すると、パースガイドの色を自動で決定します。

    Returns
    -------
    None

    '''

    # ▼▼▼ 設定値ココカラ ▼▼▼
    # bseAz = 255.0
    # bseObjPoint = [117.0, 0.0, -30.0]
    # widthDivision = 10.0
    # widthCount = 7
    # depthDivision = 10.0
    # depthCount = 4
    # heightList = (-150,)
    # drawObjPoint = False
    # drawAzEvGrid = False
    # guideColor = (0, 0, 0)
    # ▲▲▲ 設定値ココマデ ▲▲▲

    layer_list = []

    # heightListの存在チェック
    # try:
    #     heightList
    # except NameError:
    #     # なかった場合、bseObjPoint[1]を突っ込んでおく
    #     heightList = (bseObjPoint[1],)

    for i in range(len(heightList)):
        # guideColorの空チェック
        # なかった場合、createcolorで自動で色を決定
        if not guideColor:
            # リスト番号(i)を使って色相環(h)をぐるぐる回して自動で決定
            # 明度(v)を0.5～1に振る(徐々に明るくなる)
            vRange = 0.5 / len(heightList)
            meido = 0.5 + i*vRange
            color = createcolor(i, 1, meido)
        else:
            color = guideColor

        # layer_listにheightLayerオブジェクトのインスタンスを突っ込む
        layer_list.append(heightLayer(heightList[i], color))

        print("***********************************************")
        print("layer_list[%d]: height=%g, color=" % (i, layer_list[i].height), end="")
        print(layer_list[i].color)

        # baseOPのHeightをオーバーライド
        bseObjPoint[1] = layer_list[i].height
        # パースガイド生成
        horz_plane(bseAz, bseObjPoint, widthDivision, widthCount, depthDivision, depthCount, drawObjPoint, drawAzEvGrid, layer_list[i].color)

    print("処理が全部終わりました。")
