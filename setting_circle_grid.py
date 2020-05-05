# -*- coding: utf-8 -*-
import sys
import tkinter
from tkinter import ttk
from tkinter import colorchooser
from tkinter import messagebox
import numpy as np
import colorsys
from circle_grid_exec import circle_grid
from mana544Lib import loadSetting, saveSetting, objectPoint
from fractions import Fraction

# ★★★★★★★★★
# ★ アクション ★
# ★★★★★★★★★
# 「設定値保存」ボタン
def btn_saveSetting_action():
        # 保存するjsonセクションと設定値dictを定義
        section="circle_grid"
        setting = {'txt_sphR': txt_sphR.get(),          # String
                   'txt_cirCtrAz': txt_cirCtrAz.get(),  # String
                   'txt_cirCtrEv': txt_cirCtrEv.get(),  # String
                   'txt_cirR': txt_cirR.get(),          # String
                   'txt_imgSizW': txt_imgSizW.get(),          # String
                   'txt_imgSizH': txt_imgSizH.get(),          # String
                   'chkVal_drawAzEvGrid': chkVal_drawAzEvGrid.get(),    # Boolean
                   'chkVal_guideColor': chkVal_guideColor.get(),        # Boolean
                   'btn_color': style.configure("btn_color.TButton")['foreground']}           # String
        saveSetting(section, setting)
        print("設定値を保存しました。")
        messagebox.showinfo('設定値保存','設定値を保存しました。')

# パースガイド画像生成 実行
def btn_execute_action(event):
        # GUIインプット情報から数値変換
        # 全天球半径
        sphR = float(txt_sphR.get())
        # 円中心ポイントAz, Evを使って
        # ObjectPointオブジェクト生成
        centerPoint = objectPoint(
                Az=float(txt_cirCtrAz.get()),
                Ev=float(txt_cirCtrEv.get())
        )
        imageSize = (int(txtVal_imgSizW.get()), int(txtVal_imgSizH.get()))

        # カンマ区切りをスプリットする
        # 組み込みリスト型にはそのまま数値変換できないので
        # いったんnp.array型で一気にfloat変換
        # その後組み込みリストに変換
        ans1 = np.array(txt_cirR.get().split(","), dtype ='float64')
        circleR = ans1.tolist()

        # チェックボックスモノは
        # BooleanVarオブジェクトからgetして
        # Boolean型に変換
        drawAzEvGrid = chkVal_drawAzEvGrid.get()

        # 「パースガイドの色」チェックボックスの選択有無に応じて
        # guideColorに突っ込む値を変える
        if chkVal_guideColor.get():
                # 16進カラーコードを取得
                c = style.configure("btn_color.TButton")['foreground']
                # カラーコードをRGB(タプル)に変換
                guideColor = (int(c[1:3],16),int(c[3:5],16),int(c[5:7],16))
        else:
                # 空のタプル
                guideColor = ()

        # imageSizeのタテヨコ比を検証
        rto = Fraction(imageSize[0] , imageSize[1])
        print('出力画像サイズ(W, H)={}, Ratio={}:{}'.format(imageSize, rto.numerator, rto.denominator))
        if (rto.numerator != 2) or (rto.denominator != 1):
                messagebox.showerror('縦横比エラー','出力画像サイズの縦横比が{}:{}になっています。縦横比は必ず「W:H = 2:1」になるように数値設定してください。'.format(rto.numerator, rto.denominator))
                return
        
        # 円ガイド生成実行
        circle_grid(sphR, centerPoint, circleR, drawAzEvGrid, guideColor, imageSize)


# 「パースガイドの色」チェックボックス
def chk_guideColor_action():
        btn_color_reDraw()

# 色選択ボタン
def btn_color_action():
    c = style.configure("btn_color.TButton")['foreground']
    a = tkinter.colorchooser.askcolor(initialcolor=c)
    # キャンセルされたら、色のセットはなし
    if a[1] is not None:
        style.configure("btn_color.TButton", foreground=a[1])

# 「パースガイドの色」チェックボックスに応じて
# 「色」ボタンの表示描画を変える
def btn_color_reDraw():
    if chkVal_guideColor.get():
        # print("チェックが入ってます")
        btn_color.config(state='normal')
    else:
        # print("チェックが切れてます")
        btn_color.config(state='disable')


# メインウインドウ生成
root = tkinter.Tk()
root.title(u"円ガイド生成")
# root.geometry("300x400")
root.resizable(False,False)     #ウィンドウサイズ変更の禁止　(x,y)・・・False：禁止　True：許可
frm = ttk.Frame(root)
frm.grid(column=0, row=0, sticky=tkinter.N+tkinter.S+tkinter.E+tkinter.W)

# 初期設定値をsetting.jsonから読み込む
setting = loadSetting('circle_grid')

#######################
# ttkスタイル設定
#######################
style = ttk.Style()
style.configure("btn_color.TButton", foreground=setting['btn_color'])

#######################
# インプットテキスト格納用オブジェクト
#######################
txtVal_sphR = tkinter.StringVar()
txtVal_cirCtrAz = tkinter.StringVar()
txtVal_cirCtrEv = tkinter.StringVar()
txtVal_cirR = tkinter.StringVar()
txtVal_imgSizW = tkinter.StringVar()
txtVal_imgSizH = tkinter.StringVar()

txtVal_sphR.set(setting['txt_sphR'])
txtVal_cirCtrAz.set(setting['txt_cirCtrAz'])
txtVal_cirCtrEv.set(setting['txt_cirCtrEv'])
txtVal_cirR.set(setting['txt_cirR'])
txtVal_imgSizW.set(setting['txt_imgSizW'])
txtVal_imgSizH.set(setting['txt_imgSizH'])

#######################
# チェックボックス格納用オブジェクト
#######################
chkVal_drawAzEvGrid = tkinter.BooleanVar()
chkVal_guideColor = tkinter.BooleanVar()

chkVal_drawAzEvGrid.set(setting['chkVal_drawAzEvGrid'])
chkVal_guideColor.set(setting['chkVal_guideColor'])

#######################
# GUIコンポーネントの定義
# ココでの定義順でTabフォーカスの順序が決定される
#######################
# タイトル
Static01 = ttk.Label(frm, text=u'円ガイド生成', justify='left', padding='2')
# 全天球半径 text
Static02 = ttk.Label(frm, text=u'全天球半径', justify='left', padding='2')
# 全天球半径 インプット
txt_sphR = ttk.Entry(frm, width=7, justify='left', textvariable=txtVal_sphR)
# 円の中心 text
Static03 = ttk.Label(frm, text=u'円の中心', justify='left', padding='2')
# 円の中心(Az, Ev)
cirCtrFrm = ttk.Frame(frm)
Static04 = ttk.Label(cirCtrFrm, text=u'Az', justify='left', padding='2')
txt_cirCtrAz = ttk.Entry(cirCtrFrm, width=7, justify='left', textvariable=txtVal_cirCtrAz)
Static05 = ttk.Label(cirCtrFrm, text=u'Ev', justify='left', padding='2')
txt_cirCtrEv = ttk.Entry(cirCtrFrm, width=7, justify='left', textvariable=txtVal_cirCtrEv)
# 円半径 text
Static06 = ttk.Label(frm, text=u'円半径', justify='left', padding='2')
# 円半径 インプット
txt_cirR = ttk.Entry(frm, width=18, justify='left', textvariable=txtVal_cirR)
# 正方グリッドを描画する チェックボックス
chk_drawAzEvGrid = ttk.Checkbutton(frm, text=u"正方グリッドを描画する" , variable=chkVal_drawAzEvGrid)
# パースガイドの色 チェックボックス
chk_guideColor = ttk.Checkbutton(frm, text=u"パースガイドの色" , variable=chkVal_guideColor, command=chk_guideColor_action)
# パースガイド色設定ボタン
btn_color = ttk.Button(frm, text=u'━━━', style='btn_color.TButton', command=btn_color_action)
# 出力画像サイズ(W, H) インプット
Static07 = ttk.Label(frm, text=u'出力画像サイズ(Pixcel)', justify='left')
imgSzFrm = ttk.Frame(frm)
Static08 = ttk.Label(imgSzFrm, text=u'W', justify='left')
txt_imgSizW = ttk.Entry(imgSzFrm, width=7, justify='left', textvariable=txtVal_imgSizW)
Static09 = ttk.Label(imgSzFrm, text=u'H', justify='left')
txt_imgSizH = ttk.Entry(imgSzFrm, width=7, justify='left', textvariable=txtVal_imgSizH)
# 設定値保存ボタン
btn_saveSetting = ttk.Button(frm, text=u'設定値保存', command=btn_saveSetting_action)
# パースガイド画像生成ボタン
btn_execute = ttk.Button(frm, text=u'パースガイド画像生成')

#################
# イベントバインド
#################
btn_execute.bind("<ButtonRelease-1>", btn_execute_action) 

##################
# グリッドレイアウト
##################
Static01.grid(row=0, column=0, columnspan=2, sticky='W')
Static02.grid(row=1, column=0, sticky='W')
txt_sphR.grid(row=1, column=1, sticky='W')

Static03.grid(row=2, column=0, sticky='W')
# 円の中心小フレーム
cirCtrFrm.grid(row=2, column=1, sticky='W')
Static04.grid(row=0, column=0, sticky='W')
txt_cirCtrAz.grid(row=0, column=1, sticky='W')
Static05.grid(row=0, column=2, sticky='W')
txt_cirCtrEv.grid(row=0, column=3, sticky='W')

Static06.grid(row=3, column=0, sticky='W')
txt_cirR.grid(row=3, column=1, sticky='W')
chk_drawAzEvGrid.grid(row=4, column=0, columnspan=2, sticky='W')
chk_guideColor.grid(row=5, column=0, sticky='W')
btn_color.grid(row=5, column=1, sticky='W')

Static07.grid(row=6, column=0, columnspan=2, sticky='W')
# 出力画像サイズ小フレーム
imgSzFrm.grid(row=7, column=1, sticky='W')
Static08.grid(row=0, column=0, sticky='W')
txt_imgSizW.grid(row=0, column=1, sticky='W')
Static09.grid(row=0, column=2, sticky='W')
txt_imgSizH.grid(row=0, column=3, sticky='W')

btn_saveSetting.grid(row=8, column=0, columnspan=2, sticky='W')
btn_execute.grid(row=9, column=0, columnspan=2, sticky='E')

#########
# 再描画
#########
btn_color_reDraw()


root.mainloop()

