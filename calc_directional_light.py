# -*- coding: utf-8 -*-
import numpy as np
from mana544Lib import objectPoint
import copy

'''
太陽光によってできる影(平行光源)を計算します。
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

'''

def calc_shadow_point(sunPoint, OP, groundH):
    '''
    影のできるポイントを返す
    
    Parameters
    ----------
    sunPoint : ObjectPoint
        太陽の位置を sunPoint.Az, sunPoint.Ev で指定

    OP : ObjectPoint
        影計算の対象となるオブジェクトポイントを
        OP.D, OP.H, OP.W, OP.baseAz で指定。
    groundH : float
        SP～地面の高さ。
        SPより地面が下にある場合(普通はこの場合が多い)はマイナスで指定。

    Returns
    -------
    shadowPoint : ObjectPoint
        sunPointとOPによって、groundHにできる影のポイント。
        .D
        .H  groundHと同じ
        .W
        .baseAz  OP.baseAzと同じ
        .Az
        .Ev
    '''
    # print("OP: [%f, %f, %f]" % (OP.D, OP.H, OP.W))
    # print("OP.baseAz: %f" % (OP.baseAz,))

    # 仮baseAz
    # 太陽のAzから+90°(太陽を左側に)
    kari_baseAz = np.mod((sunPoint.Az + 90),360)
    # print("仮baseAz: %f" % (kari_baseAz))

    # 仮baseAzで考える(OPのほうは書き換えない)
    kari_OP = copy.deepcopy(OP)
    kari_OP.DHW2DHW(kari_baseAz)
    # print("仮OP: [%f, %f, %f]" % (kari_OP.D, kari_OP.H, kari_OP.W))
    # print("仮OP.baseAz: %f" % (kari_OP.baseAz,))

    kagePoint = objectPoint()
    kagePoint.baseAz = kari_baseAz
    # 影PointのHはgroundと同じ
    kagePoint.H = groundH
    # 影PointのDはkari_OP.Dと同じ
    kagePoint.D = kari_OP.D
    OP_groundH = np.abs(groundH - kari_OP.H)
    # print("OP-地面 距離: %f" % (OP_groundH,))

    kagePoint.W = OP_groundH / np.tan(np.deg2rad(sunPoint.Ev)) + kari_OP.W
    # print("影Point: [%f, %f, %f]" % (kagePoint.D, kagePoint.H, kagePoint.W))
    # print("影Point.baseAz: %f" % (kagePoint.baseAz,))

    kagePoint.DHW2DHW(OP.baseAz)
    kagePoint.rect2sph()
    # print("影Point: [%f, %f, %f]" % (kagePoint.D, kagePoint.H, kagePoint.W))
    # print("影Point.baseAz: %f" % (kagePoint.baseAz,))
    # print("影Point[Az, Ev]: [%f, %f]" % (kagePoint.Az, kagePoint.Ev))
    return kagePoint


if __name__ == '__main__':
    # ▼▼▼ 設定値ココカラ ▼▼▼
    sunPoint = objectPoint(Az=342, Ev=80)
    OP = objectPoint(D=100, H=-60, W=0, baseAz=0)
    groundH = -210
    # ▲▲▲ 設定値ココマデ ▲▲▲

    SP = calc_shadow_point(sunPoint, OP, groundH)

    print("影Point")
    print("[D, H, W] = [%f, %f, %f]" % (SP.D, SP.H, SP.W))
    print("baseAz    =  %f" % (SP.baseAz,))
    print("[Az, Ev]  = [%f, %f]" % (SP.Az, SP.Ev))

