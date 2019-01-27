# -*- coding: utf-8 -*-
from mana544Lib import objectPoint

D = 411.5568
H = -150
W = 21.5688
baseAz = 232.0
# 回転させるbaseAz角度
new_baseAz = 90

point = objectPoint(D=D,H=H,W=W,baseAz=baseAz)
print("point[D, H, W] = [%f, %f, %f]" % (point.D, point.H, point.W))
print("point.baseAz = %f" % (point.baseAz,))
point.rect2sph()
print("point[Az, Ev] = [%f, %f]" % (point.Az, point.Ev))
print("*************************")

point.DHW2DHW(new_baseAz)
print("new_baseAz = %f" % (new_baseAz,))
print("point[D, H, W] = [%f, %f, %f]" % (point.D, point.H, point.W))
print("point.baseAz = %f" % (point.baseAz,))

point.rect2sph()
print("point[Az, Ev] = [%f, %f]" % (point.Az, point.Ev))

