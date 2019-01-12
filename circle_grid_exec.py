# -*- coding: utf-8 -*-
import numpy as np
from PIL import Image, ImageDraw
from operator import attrgetter
from mana544Lib import createcolor, objectPoint

'''
正距円筒図法に則って、正円(同心円)を計算します。
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

'''

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


def createImage(line_point, drawAzEvGrid, guideColor):
    """
    OPを描画してPNGファイルに保存する。

    Parameters
    ----------
    line_point : list[(ObjectPoint, ...), ...]
        円を形成するポイントのリスト
    drawAzEvGrid : Boolean
        PNG画像内に正距円筒図法の正方グリッドを描画するかどうか。
        TrueでAz=(0, 90, 180, 270, 360), Ev=(-90, 0, 90) の位置にグレーのラインが描画されます。
    guideColor : tuple(int, int, int)
        描画する色

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
    for i in range(len(line_point)):
        if not guideColor:
            # リスト番号(i)を使って色相環(h)をぐるぐる回して自動で決定
            # 明度(v)を0.5～1に振る(徐々に明るくなる)
            vRange = 0.5 / len(line_point)
            meido = 0.5 + i*vRange
            color = createcolor(i, 1, meido)
        else:
            color = guideColor

        # ライン描画用ポイント初期化
        P=[]
        for j in range(len(line_point[i])):
            # 点(円)の描画ポイント個数
            P.append(((x_a * line_point[i][j].Az), (y_a * line_point[i][j].Ev + y_b)))

        draw.line(P, fill=color, width=2)
        draw_a.line(P, fill=255, width=2)

    # アルファチャンネル埋め込み
    im.putalpha(im_a)

    # filename = ("vertPersGuide(%g).png" % bseObjPoint[0])
    filename = ("circlePersGuide.png")
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
    # 円を形成する点の数(角度)
    circlePoint_deg = 1.0
    point_theta = np.arange(0.0, 360.0+circlePoint_deg, circlePoint_deg)

    # vert面[W, H]に円を割り付け
    W = circleR * np.cos(np.deg2rad(point_theta))
    H = circleR * np.sin(np.deg2rad(point_theta))

    # vert面の円をEv分傾ける
    cntPoint_sin = np.sin(np.deg2rad(centerPoint.Ev))
    cntPoint_cos = np.cos(np.deg2rad(centerPoint.Ev))
    D = -1 * H * cntPoint_sin
    H = H * cntPoint_cos

    # 円の座標[D, H, W]を求める
    W = centerPoint.W + W
    D = centerPoint.D + D
    H = centerPoint.H + H

    # point_thetaの数だけcirclePoint(objectPointクラスのリスト)を作る
    circlePoint = []
    for i in range(0,len(point_theta)):
        circlePoint.append(
            objectPoint(
                W=W[i], 
                D=D[i],
                H=H[i],
                baseAz=centerPoint.baseAz))
        circlePoint[i].rect2sph()
        # print("circlePoint[%u]: [%f, %f,%f]" % (i, circlePoint[i].W, circlePoint[i].D, circlePoint[i].H))
    
    # もし Dにマイナスの値が入っていたら、
    # circlePointリストを'Az'プロパティ昇順ソート
    # (線描画対策)
    if D.min() < 0:
        circlePoint = sorted(circlePoint, key=attrgetter('Az'))

    return circlePoint

def circle_grid(sphR, centerPoint, circleR, drawAzEvGrid, guideColor):
    '''
    ★★★★★★★★★★★★★★
    ★ 円ガイド生成の     ★
    ★ エントリーポイント ★
    ★★★★★★★★★★★★★★

    sphR : float
        全天球の半径 [mm]([m]にしたほうがいいよ。1000かける)
    centerPoint : objectPoint
        円の中心座標を[Az, Ev]で指定
        .Az = 180
        .Ev = -80
    circleR : tuple(float, float...)
        円の半径 [mm]
        タプルで複数の半径を指定すると、同心円を描画します。
    drawAzEvGrid : Boolean
        PNG画像内に正距円筒図法の正方グリッドを描画するかどうか。
        TrueでAz=(0, 90, 180, 270, 360), Ev=(-90, 0, 90) の位置にグレーのラインが描画されます。
    guideColor : tuple(int, int, int)
        パースガイドの色をRGB値で指定。
        空tupleを指定すると、パースガイドの色を自動で決定します。
    '''
    # ▼▼▼ 設定値ココカラ ▼▼▼
    # sphR = 1.5 * 1000
    # centerPoint = objectPoint()
    # centerPoint.Az = 180
    # centerPoint.Ev = -80.0
    # circleR = (264, 266,)
    # drawAzEvGrid = True
    # guideColor = (0, 0, 0)
    # ▲▲▲ 設定値ココマデ ▲▲▲

    # centerPoint.AzをbaseAzとして[D, H, W]を計算
    centerPoint.baseAz = centerPoint.Az
    centerPoint.D = sphR * np.cos(np.deg2rad(centerPoint.Ev))
    centerPoint.H = sphR * np.sin(np.deg2rad(centerPoint.Ev))
    centerPoint.W = 0.0
    print("centerPoint: [%.2f, %.2f, %.2f]" % (centerPoint.D, centerPoint.H, centerPoint.W))

    '''
    line_point =[ (objPoint, objPoint, ...), ... ]
                   ~~~~~~~~    ← [j]
                  ~~~~~~~~~~~~~~~~~~~~~~~~~ ← [i]
                  ↑一本の線を定義 : line_point[i]
    '''
    line_point =[]
    for i in range(len(circleR)):
        CP = tuple(calc_circlePoint(centerPoint, circleR[i]))

        # 円のポイント計算した結果を
        # リストに追加
        line_point.append(CP)

        print("circle_R: %.f" % (circleR[i]))

    # 円を描画
    createImage(line_point, drawAzEvGrid, guideColor)
    print("処理が全部終わりました。")

