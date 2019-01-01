# -*- coding: utf-8 -*-
import sys
import tkinter
from tkinter import colorchooser
import numpy as np
import colorsys
import pers_grid_exec
from mana544Lib import loadSetting, saveSetting

# メインウインドウ生成
root = tkinter.Tk()
root.title(u"水平パースガイド生成")
root.geometry("300x400")
root.resizable(False,False)     #ウィンドウサイズ変更の禁止　(x,y)・・・False：禁止　True：許可

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
                   'chkVal_drawObjPoint': chkVal_drawObjPoint.get(),    # Boolean
                   'chkVal_drawAzEvGrid': chkVal_drawAzEvGrid.get(),    # Boolean
                   'chkVal_guideColor': chkVal_guideColor.get(),        # Boolean
                   'btn_color': btn_color.cget('foreground')}           # String
        saveSetting(section, setting)
        print("設定値を保存しました。")

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

        # チェックボックスモノは
        # BooleanVarオブジェクトからgetして
        # Boolean型に変換
        drawObjPoint = chkVal_drawObjPoint.get()
        drawAzEvGrid = chkVal_drawAzEvGrid.get()

        # 「パースガイドの色」チェックボックスの選択有無に応じて
        # guideColorに突っ込む値を変える
        if chkVal_guideColor.get():
                # 16進カラーコードを取得
                c = btn_color.cget('foreground')
                # カラーコードをRGB(タプル)に変換
                guideColor = (int(c[1:3],16),int(c[3:5],16),int(c[5:7],16))
        else:
                # 空のタプル
                guideColor = ()
        
        pers_grid_exec.horz_plane_pers_grid(bseAz, bseObjPoint, widthDivision, widthCount, depthDivision, depthCount, heightList, drawObjPoint, drawAzEvGrid, guideColor)
        # print(guideColor)
        # print(heightList)
        # print(type(heightList))


# 「パースガイドの色」チェックボックス
def chk_guideColor_action():
        btn_color_reDraw()

# 色選択ボタン
def btn_color_action():
    c = btn_color.cget('foreground')
    a = tkinter.colorchooser.askcolor(initialcolor=c)
    # キャンセルされたら、色のセットはなし
    if a[1] is not None:
        btn_color.configure(foreground=a[1])

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

# ★★★★★★★★★★★★★★★
# ★ スタティックテキスト ★
# ★★★★★★★★★★★★★★★
Static01 = tkinter.Label(text=u'水平パースガイド生成', justify='left', font=('',14))
Static02 = tkinter.Label(text=u'ベースAz', justify='left')
Static03 = tkinter.Label(text=u'ベースObject Point', justify='left')
Static04 = tkinter.Label(text=u'D', justify='left')
Static05 = tkinter.Label(text=u'W', justify='left')
Static06 = tkinter.Label(text=u'H', justify='left')
Static07 = tkinter.Label(text=u'Width Division', justify='left')
Static08 = tkinter.Label(text=u'Width Count', justify='left')
Static09 = tkinter.Label(text=u'Depth Division', justify='left')
Static10 = tkinter.Label(text=u'Depth Count', justify='left')

# ★★★★★★★★★★★★★★
# ★ インプットテキスト ★
# ★★★★★★★★★★★★★★
txtVal_baseAz = tkinter.StringVar()
txtVal_D = tkinter.StringVar()
txtVal_W = tkinter.StringVar()
txtVal_H = tkinter.StringVar()
txtVal_widthDiv = tkinter.StringVar()
txtVal_widthCnt = tkinter.StringVar()
txtVal_depthDiv = tkinter.StringVar()
txtVal_depthCnt = tkinter.StringVar()
txtVal_baseAz.set(setting['txt_baseAz'])
txtVal_D.set(setting['txt_D'])
txtVal_W.set(setting['txt_W'])
txtVal_H.set(setting['txt_H'])
txtVal_widthDiv.set(setting['txt_widthDiv'])
txtVal_widthCnt.set(setting['txt_widthCnt'])
txtVal_depthDiv.set(setting['txt_depthDiv'])
txtVal_depthCnt.set(setting['txt_depthCnt'])

txt_baseAz = tkinter.Entry(width=10, justify='left', textvariable=txtVal_baseAz)
txt_D = tkinter.Entry(width=5, justify='left', textvariable=txtVal_D)
txt_W = tkinter.Entry(width=5, justify='left', textvariable=txtVal_W)
txt_H = tkinter.Entry(width=18, justify='left', textvariable=txtVal_H)
txt_widthDiv = tkinter.Entry(width=10, justify='left', textvariable=txtVal_widthDiv)
txt_widthCnt = tkinter.Entry(width=5, justify='left', textvariable=txtVal_widthCnt)
txt_depthDiv = tkinter.Entry(width=10, justify='left', textvariable=txtVal_depthDiv)
txt_depthCnt = tkinter.Entry(width=5, justify='left', textvariable=txtVal_depthCnt)

# ★★★★★★★★★★★★★
# ★ チェックボックス ★
# ★★★★★★★★★★★★★
# チェックボックス用変数
chkVal_drawObjPoint = tkinter.BooleanVar()
chkVal_drawObjPoint.set(setting['chkVal_drawObjPoint'])
chkVal_drawAzEvGrid = tkinter.BooleanVar()
chkVal_drawAzEvGrid.set(setting['chkVal_drawAzEvGrid'])
chkVal_guideColor = tkinter.BooleanVar()
chkVal_guideColor.set(setting['chkVal_guideColor'])
# chk_drawObjPoint = tkinter.Checkbutton(text=u"OPの“点”を描画する" , variable=Val1, state='disabled')
chk_drawObjPoint = tkinter.Checkbutton(text=u"OPの“点”を描画する" , variable=chkVal_drawObjPoint)
chk_drawAzEvGrid = tkinter.Checkbutton(text=u"正方グリッドを描画する" , variable=chkVal_drawAzEvGrid)
chk_guideColor = tkinter.Checkbutton(text=u"パースガイドの色" , variable=chkVal_guideColor, command=chk_guideColor_action)

# ★★★★★★★
# ★ ボタン ★
# ★★★★★★★
btn_color = tkinter.Button(text=u'━━━', justify='left', foreground=setting['btn_color'], command=btn_color_action)
btn_execute = tkinter.Button(text=u'パースガイド画像生成', justify='left')
btn_saveSetting = tkinter.Button(text=u'設定値保存', command=btn_saveSetting_action)

# ★★★★★★★★
# ★ イベント ★
# ★★★★★★★★
btn_execute.bind("<ButtonRelease-1>", btn_execute_action) 
# chk_guideColor.bind("<ButtonRelease-1>", chk_guideColor_action)

# ★★★★★★★★★
# ★ レイアウト ★
# ★★★★★★★★★
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
btn_execute.grid(row=13, column=0, columnspan=5, sticky='E')
btn_saveSetting.grid(row=12, column=0, columnspan=5, sticky='W')


# ★★★★★★★
# ★ 再描画 ★
# ★★★★★★★
btn_color_reDraw()


root.mainloop()

