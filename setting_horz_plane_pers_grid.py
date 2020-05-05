# -*- coding: utf-8 -*-
import sys
import tkinter
from tkinter import ttk
from tkinter import colorchooser
from tkinter import messagebox
import numpy as np
import colorsys
import pers_grid_exec
from mana544Lib import loadSetting, saveSetting
from fractions import Fraction

# メインウインドウ生成
root = tkinter.Tk()
root.title(u"水平パースガイド生成")
# root.geometry("300x400")
root.resizable(False,False)     #ウィンドウサイズ変更の禁止　(x,y)・・・False：禁止　True：許可
frm = ttk.Frame(root)
frm.grid(column=0, row=0, sticky=tkinter.N+tkinter.S+tkinter.E+tkinter.W)

# ★★★★★★★★★
# ★ アクション ★
# ★★★★★★★★★
# 「設定値保存」ボタン
def btn_saveSetting_action():
        # 保存するjsonセクションと設定値dictを定義
        section="horz_plane_pers_grid"
        setting = {'txt_baseAz': txt_baseAz.get(),      # String
                   'txt_D': txt_D.get(),                # String
                   'txt_W': txt_W.get(),                # String
                   'txt_H': txt_H.get(),                # String
                   'txt_widthDiv': txt_widthDiv.get(),  # String
                   'txt_widthCnt': txt_widthCnt.get(),  # String
                   'txt_depthDiv': txt_depthDiv.get(),  # String
                   'txt_depthCnt': txt_depthCnt.get(),  # String
                   'txt_imgSizH': txt_imgSizH.get(),  # String
                   'txt_imgSizW': txt_imgSizW.get(),  # String
                   'chkVal_drawObjPoint': chkVal_drawObjPoint.get(),    # Boolean
                   'chkVal_drawAzEvGrid': chkVal_drawAzEvGrid.get(),    # Boolean
                   'chkVal_guideColor': chkVal_guideColor.get(),        # Boolean
                   'btn_color': style.configure("btn_color.TButton")['foreground']}           # String
        saveSetting(section, setting)
        print("設定値を保存しました。")
        messagebox.showinfo('設定値保存','設定値を保存しました。')

# パースガイド画像生成 実行
def btn_execute_action(event):
        # GUIインプット情報から数値変換
        bseAz = float(txt_baseAz.get())
        D = float(txt_D.get())
        W = float(txt_W.get())
        bseObjPoint = [D, 0.0, W]

        # カンマ区切りをスプリットする
        # 組み込みリスト型にはそのまま数値変換できないので
        # いったんnp.array型で一気にfloat変換
        # その後組み込みリストに変換
        ans1 = np.array(txt_H.get().split(","), dtype ='float64')
        heightList = ans1.tolist()

        # テキストインプットモノは
        # 数値変換(float, int)
        widthDivision = float(txt_widthDiv.get())
        widthCount = int(txt_widthCnt.get())
        depthDivision = float(txt_depthDiv.get())
        depthCount = int(txt_depthCnt.get())
        imageSize = (int(txtVal_imgSizW.get()), int(txtVal_imgSizH.get()))

        # チェックボックスモノは
        # BooleanVarオブジェクトからgetして
        # Boolean型に変換
        drawObjPoint = chkVal_drawObjPoint.get()
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

        pers_grid_exec.horz_plane_pers_grid(bseAz, bseObjPoint, widthDivision, widthCount, depthDivision, depthCount, heightList, drawObjPoint, drawAzEvGrid, guideColor, imageSize)
        # print(guideColor)
        # print(heightList)
        # print(type(heightList))


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

# 初期設定値をsetting.jsonから読み込む
setting = loadSetting('horz_plane_pers_grid')

#######################
# ttkスタイル設定
#######################
style = ttk.Style()
style.configure("btn_color.TButton", foreground=setting['btn_color'])

#######################
# スタティックテキスト
#######################
Static01 = ttk.Label(frm, text=u'水平パースガイド生成', justify='left', font=('',14))
Static02 = ttk.Label(frm, text=u'ベースAz', justify='left')
Static03 = ttk.Label(frm, text=u'ベースObject Point', justify='left')
Static04 = ttk.Label(frm, text=u'D', justify='left')
Static05 = ttk.Label(frm, text=u'W', justify='left')
Static06 = ttk.Label(frm, text=u'H', justify='left')
Static07 = ttk.Label(frm, text=u'Width Division', justify='left')
Static08 = ttk.Label(frm, text=u'Width Count', justify='left')
Static09 = ttk.Label(frm, text=u'Depth Division', justify='left')
Static10 = ttk.Label(frm, text=u'Depth Count', justify='left')
Static11 = ttk.Label(frm, text=u'出力画像サイズ(Pixcel)', justify='left')
Static12 = ttk.Label(frm, text=u'W', justify='left')
Static13 = ttk.Label(frm, text=u'H', justify='left')

#######################
# インプットテキスト格納用オブジェクト
#######################
txtVal_baseAz = tkinter.StringVar()
txtVal_D = tkinter.StringVar()
txtVal_W = tkinter.StringVar()
txtVal_H = tkinter.StringVar()
txtVal_widthDiv = tkinter.StringVar()
txtVal_widthCnt = tkinter.StringVar()
txtVal_depthDiv = tkinter.StringVar()
txtVal_depthCnt = tkinter.StringVar()
txtVal_imgSizW = tkinter.StringVar()
txtVal_imgSizH = tkinter.StringVar()

txtVal_baseAz.set(setting['txt_baseAz'])
txtVal_D.set(setting['txt_D'])
txtVal_W.set(setting['txt_W'])
txtVal_H.set(setting['txt_H'])
txtVal_widthDiv.set(setting['txt_widthDiv'])
txtVal_widthCnt.set(setting['txt_widthCnt'])
txtVal_depthDiv.set(setting['txt_depthDiv'])
txtVal_depthCnt.set(setting['txt_depthCnt'])
txtVal_imgSizW.set(setting['txt_imgSizW'])
txtVal_imgSizH.set(setting['txt_imgSizH'])

#######################
# チェックボックス格納用オブジェクト
#######################
chkVal_drawObjPoint = tkinter.BooleanVar()
chkVal_drawAzEvGrid = tkinter.BooleanVar()
chkVal_guideColor = tkinter.BooleanVar()

chkVal_drawObjPoint.set(setting['chkVal_drawObjPoint'])
chkVal_drawAzEvGrid.set(setting['chkVal_drawAzEvGrid'])
chkVal_guideColor.set(setting['chkVal_guideColor'])

#######################
# GUIコンポーネントの定義
# ココでの定義順でTabフォーカスの順序が決定される
#######################
# ベースAz インプット
txt_baseAz = ttk.Entry(frm, width=10, justify='left', textvariable=txtVal_baseAz)
# Base OP(D, W, H) インプット
txt_D = ttk.Entry(frm, width=5, justify='left', textvariable=txtVal_D)
txt_W = ttk.Entry(frm, width=5, justify='left', textvariable=txtVal_W)
txt_H = ttk.Entry(frm, width=18, justify='left', textvariable=txtVal_H)
# Width Division インプット
txt_widthDiv = ttk.Entry(frm, width=10, justify='left', textvariable=txtVal_widthDiv)
# Width Count インプット
txt_widthCnt = ttk.Entry(frm, width=5, justify='left', textvariable=txtVal_widthCnt)
# Depth Division インプット
txt_depthDiv = ttk.Entry(frm, width=10, justify='left', textvariable=txtVal_depthDiv)
# Depth Count インプット
txt_depthCnt = ttk.Entry(frm, width=5, justify='left', textvariable=txtVal_depthCnt)
# OPの“点”を描画する チェックボックス
chk_drawObjPoint = ttk.Checkbutton(frm, text=u"OPの“点”を描画する" , variable=chkVal_drawObjPoint)
# 正方グリッドを描画する チェックボックス
chk_drawAzEvGrid = ttk.Checkbutton(frm, text=u"正方グリッドを描画する" , variable=chkVal_drawAzEvGrid)
# パースガイドの色 チェックボックス
chk_guideColor = ttk.Checkbutton(frm, text=u"パースガイドの色" , variable=chkVal_guideColor, command=chk_guideColor_action)
# パースガイド色指定ボタン
btn_color = ttk.Button(frm, text=u'━━━', style='btn_color.TButton', command=btn_color_action)
# 出力画像サイズ(W, H) インプット
txt_imgSizW = ttk.Entry(frm, width=7, justify='left', textvariable=txtVal_imgSizW)
txt_imgSizH = ttk.Entry(frm, width=7, justify='left', textvariable=txtVal_imgSizH)
# 設定値保存ボタン
btn_saveSetting = ttk.Button(frm, text=u'設定値保存', command=btn_saveSetting_action)
# パースガイド画像生成ボタン
btn_execute = ttk.Button(frm, text=u'パースガイド画像生成')

################
# イベントバインド
################
btn_execute.bind("<ButtonRelease-1>", btn_execute_action) 
# chk_guideColor.bind("<ButtonRelease-1>", chk_guideColor_action)

##################
# グリッドレイアウト
##################
Static01.grid(row=0, column=0, columnspan=5, sticky='W')
Static02.grid(row=1, column=0, sticky='W')
Static03.grid(row=2, column=0, columnspan=5, sticky='W')
Static04.grid(row=3, column=1, sticky='W')
Static05.grid(row=3, column=3, sticky='W')
Static06.grid(row=4, column=1, sticky='W')
Static07.grid(row=5, column=0, sticky='W')
Static08.grid(row=6, column=0, sticky='W')
Static09.grid(row=7, column=0, sticky='W')
Static10.grid(row=8, column=0, sticky='W')
txt_baseAz.grid(row=1, column=1, columnspan=4, sticky='W')
txt_D.grid(row=3, column=2, sticky='W')
txt_W.grid(row=3, column=4, sticky='W')
txt_H.grid(row=4, column=2, columnspan=3, sticky='W')
txt_widthDiv.grid(row=5, column=1, columnspan=4, sticky='W')
txt_widthCnt.grid(row=6, column=1, columnspan=4, sticky='W')
txt_depthDiv.grid(row=7, column=1, columnspan=4, sticky='W')
txt_depthCnt.grid(row=8, column=1, columnspan=4, sticky='W')
chk_drawObjPoint.grid(row=9, column=0, columnspan=5, sticky='W')
chk_drawAzEvGrid.grid(row=10, column=0, columnspan=5, sticky='W')
chk_guideColor.grid(row=11, column=0, columnspan=4, sticky='W')
btn_color.grid(row=11, column=4, sticky='W')
Static11.grid(row=12, column=0, columnspan=5, sticky='W')
Static12.grid(row=13, column=1, sticky='W')
txt_imgSizW.grid(row=13, column=2, sticky='W')
Static13.grid(row=13, column=3, sticky='W')
txt_imgSizH.grid(row=13, column=4, sticky='W')
btn_execute.grid(row=15, column=0, columnspan=5, sticky='E')
btn_saveSetting.grid(row=14, column=0, columnspan=5, sticky='W')


#########
# 再描画
#########
btn_color_reDraw()


root.mainloop()

