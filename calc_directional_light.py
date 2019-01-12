# -*- coding: utf-8 -*-
import numpy as np
from PIL import Image, ImageDraw
from mana544Lib import createcolor, listprint, heightLayer, objectPoint, jdgAzRange
import matplotlib.pyplot as plt
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
pillow 5.0.0

★★★★★★★
★ 設定値 ★
★★★★★★★
sunPoint : objectPoint
    太陽の座標を[Az, Ev]で指定
    .Az
    .Ev
OP : objectPoint
    影の計算の起点となるポイントを[D, H, W]&baseAzで指定
    OP.D
    OP.H
    OP.W
    OP.baseAz
groundH : float
    SP～地面の高さ
'''
# ▼▼▼ 設定値ココカラ ▼▼▼
sunPoint = objectPoint(Az=342, Ev=80)
OP = objectPoint(D=100, H=-60, W=0, baseAz=0)
groundH = -210
# ▲▲▲ 設定値ココマデ ▲▲▲

'''
★★★★★★
★ main ★
★★★★★★
'''
print("OP: [%f, %f, %f]" % (OP.D, OP.H, OP.W))
print("OP.baseAz: %f" % (OP.baseAz,))


# 仮baseAz
# 太陽のAzから+90°(太陽を左側に)
kari_baseAz = np.mod((sunPoint.Az + 90),360)
print("仮baseAz: %f" % (kari_baseAz))

# 仮baseAzで考える(OPのほうは書き換えない)
kari_OP = copy.deepcopy(OP)
kari_OP.DHW2DHW(kari_baseAz)
print("仮OP: [%f, %f, %f]" % (kari_OP.D, kari_OP.H, kari_OP.W))
print("仮OP.baseAz: %f" % (kari_OP.baseAz,))


kagePoint = objectPoint()
kagePoint.baseAz = kari_baseAz
# 影PointのHはgroundと同じ
kagePoint.H = groundH
# 影PointのDはkari_OP.Dと同じ
kagePoint.D = kari_OP.D
OP_groundH = np.abs(groundH - kari_OP.H)
print("OP-地面 距離: %f" % (OP_groundH,))

kagePoint.W = OP_groundH / np.tan(np.deg2rad(sunPoint.Ev)) + kari_OP.W
print("影Point: [%f, %f, %f]" % (kagePoint.D, kagePoint.H, kagePoint.W))
print("影Point.baseAz: %f" % (kagePoint.baseAz,))

kagePoint.DHW2DHW(OP.baseAz)
print("影Point: [%f, %f, %f]" % (kagePoint.D, kagePoint.H, kagePoint.W))
print("影Point.baseAz: %f" % (kagePoint.baseAz,))
kagePoint.rect2sph()
print("影Point[Az, Ev]: [%f, %f]" % (kagePoint.Az, kagePoint.Ev))

# 計算結果をささっと確認用(matplotlib使用)
# plt.plot(p_Az,p_Ev,'-')
# plt.ylim(-90, 90)
# plt.yticks(range(-90,100,30))
# plt.xlim(0, 360)
# plt.xticks(range(0,361,90))
# plt.show()
