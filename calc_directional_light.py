# -*- coding: utf-8 -*-
import numpy as np
from mana544Lib import objectPoint, loadSetting, saveSetting
import copy
import tkinter
from tkinter import ttk
from tkinter import messagebox

'''
太陽光(平行光源)によってできる、OPから地面に落ちる影の点を計算します。
SUN PositionよりもOPのEvが上にあると、地面に影が落ちないのでエラーとなります。
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
tkinter

'''

def calc_shadow_point(sunPoint, OP, groundH):
    '''
    影のできるポイントを計算して返す
    
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

# ★★★★★★★★★
# ★ アクション ★
# ★★★★★★★★★
# 「設定値保存」ボタン
def btn_saveSetting_action():
        # 保存するjsonセクションと設定値dictを定義
        section="calc_directional_light"
        setting = {'txt_sunPtAz': txt_sunPtAz.get(),        # String
                   'txt_sunPtEv': txt_sunPtEv.get(),        # String
                   'txt_objPtBseAz': txt_objPtBseAz.get(),  # String
                   'txt_objPtD': txt_objPtD.get(),          # String
                   'txt_objPtH': txt_objPtH.get(),          # String
                   'txt_objPtW': txt_objPtW.get(),          # String
                   'txt_groundH': txt_groundH.get()}        # String
        saveSetting(section, setting)
        print("設定値を保存しました。")
        messagebox.showinfo('設定値保存','設定値を保存しました。')

# 影の計算 実行
def btn_execute_action(event):
        # GUIインプット情報から数値変換
        # SUN Point(Az, Ev)
        sunPoint = objectPoint(
            Az=float(txt_sunPtAz.get()), 
            Ev=float(txt_sunPtEv.get())
            )
        # Object Point(BaseAz, D, H, W)
        OP = objectPoint(
            D=float(txt_objPtD.get()), 
            H=float(txt_objPtH.get()), 
            W=float(txt_objPtW.get()), 
            baseAz=float(txt_objPtBseAz.get())
            )
        # Ground H
        groundH = float(txt_groundH.get())

        # 影Pointの計算
        SP = calc_shadow_point(sunPoint, OP, groundH)

        # 影Pointの値からフォーマット幅を決定
        # 最大の整数ケタ数 + 3(ドット + 小数点以下1ケタ + 符号)
        b = np.max(np.ceil(np.log10(np.abs(
            [SP.baseAz, SP.D, SP.H, SP.W, SP.Az, SP.Ev]
            )))) + 3
        strfmt = '%% %.0f.1f' % (b, )

        print("***** Shadow Point *****")
        stg = 'baseAz    =  %s' % (strfmt, )
        print(stg % (SP.baseAz,))
        stg = '[D, H, W] = [%s %s %s]' % (strfmt, strfmt, strfmt, )
        print(stg % (SP.D, SP.H, SP.W))
        stg = '[Az, Ev]  = [%s %s]\n' % (strfmt, strfmt, )
        print(stg % (SP.Az, SP.Ev))


if __name__ == '__main__':

    # メインウインドウ生成
    root = tkinter.Tk()
    root.title(u"太陽光(平行光源)の影計算")
    # root.geometry("300x400")
    root.resizable(False,False)     #ウィンドウサイズ変更の禁止　(x,y)・・・False：禁止　True：許可
    frm = ttk.Frame(root)
    frm.grid(column=0, row=0, sticky=tkinter.N+tkinter.S+tkinter.E+tkinter.W)

    # 初期設定値をsetting.jsonから読み込む
    setting = loadSetting('calc_directional_light')

    # ★★★★★★★★★
    # ★ 子フレーム ★
    # ★★★★★★★★★
    # SUN Point(Az, Ev)用コンテナ
    sunPtFrm = ttk.Frame(frm)
    # Object Point(Base Az)用コンテナ
    objPtFrm1 = ttk.Frame(frm)
    # Object Point(D, H, W)用コンテナ
    objPtFrm2 = ttk.Frame(frm)

    # ★★★★★★★★★★★★★★★
    # ★ スタティックテキスト ★
    # ★★★★★★★★★★★★★★★
    Static01 = ttk.Label(frm, text=u'太陽光(平行光源)の影計算', justify='left', padding='2')

    Static02 = ttk.Label(frm, text=u'SUN Position :', justify='left', padding='2')
    Static03 = ttk.Label(sunPtFrm, text=u'Az', justify='left', padding='2')
    Static04 = ttk.Label(sunPtFrm, text=u'Ev', justify='left', padding='2')

    Static05 = ttk.Label(frm, text=u'Object Point :', justify='left', padding='2')
    Static06 = ttk.Label(objPtFrm1, text=u'BaseAz', justify='left', padding='2')
    Static07 = ttk.Label(objPtFrm2, text=u'D', justify='left', padding='2')
    Static08 = ttk.Label(objPtFrm2, text=u'H', justify='left', padding='2')
    Static09 = ttk.Label(objPtFrm2, text=u'W', justify='left', padding='2')

    Static10 = ttk.Label(frm, text=u'Ground H :', justify='left', padding='2')

    # ★★★★★★★★★★★★★★
    # ★ インプットテキスト ★
    # ★★★★★★★★★★★★★★
    txtVal_sunPtAz = tkinter.StringVar()
    txtVal_sunPtEv = tkinter.StringVar()
    txtVal_objPtBseAz = tkinter.StringVar()
    txtVal_objPtD = tkinter.StringVar()
    txtVal_objPtH = tkinter.StringVar()
    txtVal_objPtW = tkinter.StringVar()
    txtVal_groundH = tkinter.StringVar()

    txtVal_sunPtAz.set(setting['txt_sunPtAz'])
    txtVal_sunPtEv.set(setting['txt_sunPtEv'])
    txtVal_objPtBseAz.set(setting['txt_objPtBseAz'])
    txtVal_objPtD.set(setting['txt_objPtD'])
    txtVal_objPtH.set(setting['txt_objPtH'])
    txtVal_objPtW.set(setting['txt_objPtW'])
    txtVal_groundH.set(setting['txt_groundH'])

    txt_sunPtAz = ttk.Entry(sunPtFrm, width=6, justify='left', textvariable=txtVal_sunPtAz)
    txt_sunPtEv = ttk.Entry(sunPtFrm, width=6, justify='left', textvariable=txtVal_sunPtEv)

    txt_objPtBseAz = ttk.Entry(objPtFrm1, width=10, justify='left', textvariable=txtVal_objPtBseAz)
    txt_objPtD = ttk.Entry(objPtFrm2, width=6, justify='left', textvariable=txtVal_objPtD)
    txt_objPtH = ttk.Entry(objPtFrm2, width=6, justify='left', textvariable=txtVal_objPtH)
    txt_objPtW = ttk.Entry(objPtFrm2, width=6, justify='left', textvariable=txtVal_objPtW)

    txt_groundH = ttk.Entry(frm, width=10, justify='left', textvariable=txtVal_groundH)

    # ★★★★★★★
    # ★ ボタン ★
    # ★★★★★★★
    btn_execute = ttk.Button(frm, text=u'影の計算')
    btn_saveSetting = ttk.Button(frm, text=u'設定値保存', command=btn_saveSetting_action)

    # ★★★★★★★★
    # ★ イベント ★
    # ★★★★★★★★
    btn_execute.bind("<ButtonRelease-1>", btn_execute_action) 

    # ★★★★★★★★★
    # ★ レイアウト ★
    # ★★★★★★★★★
    sunPtFrm.grid(row=1, column=1, sticky='W')
    objPtFrm1.grid(row=2, column=1, sticky='W')
    objPtFrm2.grid(row=3, column=1, sticky='W')

    Static01.grid(row=0, column=0, columnspan=2, sticky='W')
    Static02.grid(row=1, column=0, sticky='W')
    Static03.grid(row=0, column=0, sticky='W')
    Static04.grid(row=0, column=2, sticky='W')
    Static05.grid(row=2, column=0, sticky='W')
    Static06.grid(row=0, column=0, sticky='W')
    Static07.grid(row=0, column=0, sticky='W')
    Static08.grid(row=0, column=2, sticky='W')
    Static09.grid(row=0, column=4, sticky='W')
    Static10.grid(row=4, column=0, sticky='W')

    txt_sunPtAz.grid(row=0, column=1, sticky='W')
    txt_sunPtEv.grid(row=0, column=3, sticky='W')
    txt_objPtBseAz.grid(row=0, column=1, sticky='W')
    txt_objPtD.grid(row=0, column=1, sticky='W')
    txt_objPtH.grid(row=0, column=3, sticky='W')
    txt_objPtW.grid(row=0, column=5, sticky='W')
    txt_groundH.grid(row=4, column=1, sticky='W')

    btn_execute.grid(row=6, column=0, columnspan=2, sticky='E')
    btn_saveSetting.grid(row=5, column=0, columnspan=2, sticky='W')

    root.mainloop()
    