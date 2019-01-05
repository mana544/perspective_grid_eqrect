# -*- coding: utf-8 -*-
import numpy as np
import colorsys
import copy
import json


def saveSetting(section, setting):
    '''
    設定ファイル(setting.json)に内容を保存する。
    
    Parameters
    ----------
    section : str
        何のセクションを読み取るか？
        水平パースガイド生成 : 'horz_plane_pers_grid'
        垂直パースガイド生成 : 'vert_plane_pers_grid'

    setting : dict
        設定情報。
        キーや内容はセクションによって異なります。

    Returns
    -------
    None
    '''
    with open('setting.json') as f:
        json_setting = json.load(f)

    json_setting[section] = setting

    with open('setting.json', 'w') as f:
        json.dump(json_setting, f, indent=4)


def loadSetting(section):
    '''
    設定ファイル(setting.json)から読み取って、内容を返す。
    
    Parameters
    ----------
    section : str
        何のセクションを読み取るか？
        水平パースガイド生成 : 'horz_plane_pers_grid'
        垂直パースガイド生成 : 'vert_plane_pers_grid'

    Returns
    -------
    setting : dict
        設定情報。
        キーや内容はセクションによって異なります。
    '''
    with open('setting.json') as f:
        setting = json.load(f)

    # print(type(setting))

    return setting[section]


def createcolor(num:int, s=1.0, v=1.0):
    '''
    黄金角で位相(h)を変えて、バラバラの色を生成します。
    返り値はrgbのタプルです。
    
    Parameters
    ----------
    num : int
        正の整数を指定。正の値*黄金角でhを決定します。
    s : float
        彩度。0.0～1.0を指定。デフォルトは1.0
    v : float
        明度。0.0～1.0を指定。デフォルトは1.0

    Returns
    -------
    rgb_color : (int, int, int)
        RGB値。0～255の値。
    
    '''

    golden_ang = 360*(1-1/((1 + np.sqrt(5)) / 2))    # 黄金角[deg]
    h = np.mod(golden_ang * num, 360) / 360

    a = colorsys.hsv_to_rgb(h, s, v)
    rgb = []
    for i in range(0,3):
        rgb.append(int(a[i]*255))

    return tuple(rgb)


def jdgAzRange(center_Az, range_Az, cmp_Az):
    '''
    cmp_Azが[center_Az - range_Az, center_Az + range_Az]間に入っているかどうかを判定する。

    Parameters
    ----------
    center_Az : float
        中心Az
        0 <= center_Az < 360
    range_Az : float
        範囲Az
        range_Az > 0
    cmp_Az : float
        比較対象のAz
        0 <= cmp_Az < 360

    Returns
    -------
    judge : boolean
        範囲内ならTrue。

    '''

    ps_az = center_Az + range_Az
    if ps_az > 360:
        ps_sub_az = np.mod(ps_az, 360)
        ps_az = 360
    else:
        ps_sub_az = 0

    mn_az = center_Az - range_Az
    if mn_az < 0:
        mn_sub_az = np.mod(mn_az, 360)
        mn_az = 0
    else:
        mn_sub_az = 360

    hikaku = cmp_Az
    x1 = (ps_az > hikaku)and(mn_az <= hikaku)
    x2 = (ps_sub_az >= hikaku)and(0 < ps_sub_az)
    x3 = (mn_sub_az <= hikaku)and(360 > mn_sub_az)

    if x1 or x2 or x3:
        xJDG = True
    else:
        xJDG = False
    return xJDG


    

def listprint(l, fmt):
    '''
    リストをフォーマットに従って画面出力

    Parameters
    ----------
    l : list
        リスト
    fmt : str
        フォーマット指定子文字列

    Returns
    -------
    なし
    '''
    print_fmt = "{0:" + fmt + "}"
    print("[", end="")
    for i, item in enumerate(l):
        if i!=0:
            print(", ", end="")
        print(print_fmt.format(item), end="")
    print("]", end="")

class heightLayer:
    """
    heightLayer型構造体

    Attributes
    ----------
    height : float
        高さを表す数値。
    color : (int,int,int)
        色をタプル(r, g, b)で指定。(各値は0～255)
    """
    def __init__(self,height,color):
        self.height = float(height)
        self.color = color

class objectPoint:
    """
    objectPointクラス
    OPの座標「(Az, Ev)&(D, H, W)」の管理、及び変換メソッドの提供。

    Attributes
    ----------
    Az : float
        方位角
    Ev : float
        仰角
    D : float
        奥行
    H : float
        高さ
    W : float
        横幅
    baseAz : float
        [D, H, W]座標計算の起点となる方位角
    """



    def __init__(self):
        self.Az = np.nan
        self.Ev = np.nan
        self.D = np.nan
        self.H = np.nan
        self.W = np.nan
        self.baseAz = np.nan


    def rotateDW(self, rotAz):
        '''
        指定したrotAz=[90, 180, 270]でD, Wを再計算(入れ替え)

        '''
        if rotAz==90:
            D = self.W
            W = -1 * self.D
            bseAz = np.mod(self.baseAz + 90.0, 360)
        elif rotAz==180:
            D = -1 * self.D
            W = -1 * self.W
            bseAz = np.mod(self.baseAz + 180.0, 360)
        elif rotAz==270:
            D = -1 * self.W
            W = self.D
            bseAz = np.mod(self.baseAz + 270.0, 360)
        else:
            D = self.D
            W = self.W
            bseAz = self.baseAz

        self.D = D
        self.W = W
        self.baseAz = bseAz


    def rect2sph(self):
        '''
        インスタンスの直交座標系(D, H, W)&baseAzから
        球面座標系(Az, Ev)への変換をして、インスタンスメンバーAz, Evを更新します

        Parameters
        ----------
        なし

        Returns
        -------
        '''        

        # DとWがマイナスだったら、baseAzを90度回転させて、D, Wを再計算(プラスにする)
        # if self.D<0:
        #     if self.W<0:
        #         # 3象限
        #         D = -1 * self.D
        #         W = -1 * self.W
        #         bseAz = np.mod(self.baseAz + 180.0, 360)
        #     else:
        #         # 4象限
        #         D = self.W
        #         W = -1 * self.D
        #         bseAz = np.mod(self.baseAz + 90.0, 360)
        # else:
        #     if self.W<0:
        #         # 2象限
        #         D = -1 * self.W
        #         W = self.D
        #         bseAz = np.mod(self.baseAz + 270.0, 360)
        #     else:
        #         # 1象限
        #         D = self.D
        #         W = self.W
        #         bseAz = self.baseAz
        # H = self.H

        self.convertDW()
        D = self.D
        H = self.H
        W = self.W
        bseAz =self.baseAz

        # 相対方位角 + ベース方位角
        az = np.rad2deg(np.arctan(W/D)) + bseAz

        # 斜辺
        hyp = np.sqrt(D**2 + W**2)

        # 仰角
        ev = np.rad2deg(np.arctan(H/hyp))

        self.Az = az
        self.Ev = ev



    def convertDW(self):
        '''
        DとWがマイナスだったら、baseAzを回転させて、D, Wを再計算(プラスにする)


        Parameters
        ----------
        なし

        Returns
        -------
        rotAz : int
            回転させたAz[0, 90, 180, 270]

        '''
        if self.D<0:
            if self.W<0:
                # 3象限(180°回転)
                rotAz = 180
            else:
                # 4象限(90°回転)
                rotAz = 90
        else:
            if self.W<0:
                # 2象限(270°回転)
                rotAz = 270
            else:
                # 1象限(何もしない)
                rotAz = 0
        self.rotateDW(rotAz)
        return rotAz


    def DHW2DHW(self, bseAz):
        '''
        指定されたbaseAzでDHWを再計算して
        インスタンスメンバー(D, H, W)&baseAzを更新します。
        '''
        # 元と元2をディープコピー
        moto2 = copy.deepcopy(self)
        
        # DとWをプラスに回転
        moto2.convertDW()
        
        Az_R = np.rad2deg(np.arctan(moto2.W/moto2.D))
        moto2.Az = moto2.baseAz + Az_R
        
        # 元2のAz2±90°の範囲にbseAzがない場合、180°反転させる
        xROT = not jdgAzRange(moto2.Az, 90, bseAz)
        if xROT:
            tgtAz = np.mod(bseAz+180, 360)
        else:
            tgtAz = bseAz
        
        Az_sa = moto2.Az - tgtAz
        hyp = np.sqrt(moto2.D**2 + moto2.W**2)
        D_new = hyp * np.cos(np.deg2rad(Az_sa))
        W_new = hyp * np.sin(np.deg2rad(Az_sa))

        if xROT:
            D_new = -1 * D_new
            W_new = -1* W_new

        # インスタンスの内容書き換え
        self.D = D_new
        self.W = W_new
        self.baseAz = bseAz
        
        




if __name__ == '__main__':

    point = objectPoint()
    point.D = -304.338085
    point.H = -210.000000
    point.W = 22.358118
    point.baseAz = 355.0
    point2 = copy.deepcopy(point)

    rotAz = point.convertDW()

    print("point[D, H, W] = [%f, %f, %f]" % (point.D, point.H, point.W))
    print("point.baseAz = %f" % (point.baseAz,))
    print("point2[D, H, W] = [%f, %f, %f]" % (point2.D, point2.H, point2.W))
    print("point2.baseAz = %f" % (point2.baseAz,))
    print("rotAz: %d"%rotAz)



