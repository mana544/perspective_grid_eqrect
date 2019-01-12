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
        # 円ガイド生成実行
        circle_grid(sphR, centerPoint, circleR, drawAzEvGrid, guideColor)


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

# ★★★★★★★★★★★★
# ★ ttkスタイル設定 ★
# ★★★★★★★★★★★★
style = ttk.Style()
style.configure("btn_color.TButton", foreground=setting['btn_color'])

# ★★★★★★★★★
# ★ 子フレーム ★
# ★★★★★★★★★
# 円中心Point(Az, Ev)用コンテナ
cirCtrFrm = ttk.Frame(frm)

# ★★★★★★★★★★★★★★★
# ★ スタティックテキスト ★
# ★★★★★★★★★★★★★★★
Static01 = ttk.Label(frm, text=u'円ガイド生成', justify='left', padding='2')
Static02 = ttk.Label(frm, text=u'全天球半径', justify='left', padding='2')
Static03 = ttk.Label(frm, text=u'円の中心', justify='left', padding='2')
Static04 = ttk.Label(cirCtrFrm, text=u'Az', justify='left', padding='2')
Static05 = ttk.Label(cirCtrFrm, text=u'Ev', justify='left', padding='2')
Static06 = ttk.Label(frm, text=u'円半径', justify='left', padding='2')

# ★★★★★★★★★★★★★★
# ★ インプットテキスト ★
# ★★★★★★★★★★★★★★
txtVal_sphR = tkinter.StringVar()
txtVal_cirCtrAz = tkinter.StringVar()
txtVal_cirCtrEv = tkinter.StringVar()
txtVal_cirR = tkinter.StringVar()

txtVal_sphR.set(setting['txt_sphR'])
txtVal_cirCtrAz.set(setting['txt_cirCtrAz'])
txtVal_cirCtrEv.set(setting['txt_cirCtrEv'])
txtVal_cirR.set(setting['txt_cirR'])

txt_sphR = ttk.Entry(frm, width=10, justify='left', textvariable=txtVal_sphR)
txt_cirCtrAz = ttk.Entry(cirCtrFrm, width=5, justify='left', textvariable=txtVal_cirCtrAz)
txt_cirCtrEv = ttk.Entry(cirCtrFrm, width=5, justify='left', textvariable=txtVal_cirCtrEv)
txt_cirR = ttk.Entry(frm, width=18, justify='left', textvariable=txtVal_cirR)

# ★★★★★★★★★★★★★
# ★ チェックボックス ★
# ★★★★★★★★★★★★★
# チェックボックス用変数
chkVal_drawAzEvGrid = tkinter.BooleanVar()
chkVal_guideColor = tkinter.BooleanVar()

chkVal_drawAzEvGrid.set(setting['chkVal_drawAzEvGrid'])
chkVal_guideColor.set(setting['chkVal_guideColor'])

chk_drawAzEvGrid = ttk.Checkbutton(frm, text=u"正方グリッドを描画する" , variable=chkVal_drawAzEvGrid)
chk_guideColor = ttk.Checkbutton(frm, text=u"パースガイドの色" , variable=chkVal_guideColor, command=chk_guideColor_action)

# ★★★★★★★
# ★ ボタン ★
# ★★★★★★★
btn_color = ttk.Button(frm, text=u'━━━', style='btn_color.TButton', command=btn_color_action)
btn_execute = ttk.Button(frm, text=u'パースガイド画像生成')
btn_saveSetting = ttk.Button(frm, text=u'設定値保存', command=btn_saveSetting_action)

# ★★★★★★★★
# ★ イベント ★
# ★★★★★★★★
btn_execute.bind("<ButtonRelease-1>", btn_execute_action) 

# ★★★★★★★★★
# ★ レイアウト ★
# ★★★★★★★★★
cirCtrFrm.grid(row=2, column=1, sticky='W')

Static01.grid(row=0, column=0, columnspan=2, sticky='W')
Static02.grid(row=1, column=0, sticky='W')
Static03.grid(row=2, column=0, sticky='W')
Static06.grid(row=3, column=0, sticky='W')
Static04.grid(row=0, column=0, sticky='W')
Static05.grid(row=0, column=2, sticky='W')
txt_sphR.grid(row=1, column=1, sticky='W')
txt_cirCtrAz.grid(row=0, column=1, sticky='W')
txt_cirCtrEv.grid(row=0, column=3, sticky='W')
txt_cirR.grid(row=3, column=1, sticky='W')
chk_drawAzEvGrid.grid(row=4, column=0, columnspan=2, sticky='W')
chk_guideColor.grid(row=5, column=0, sticky='W')
btn_color.grid(row=5, column=1, sticky='W')
btn_execute.grid(row=7, column=0, columnspan=2, sticky='E')
btn_saveSetting.grid(row=6, column=0, columnspan=2, sticky='W')

# ★★★★★★★
# ★ 再描画 ★
# ★★★★★★★
btn_color_reDraw()


root.mainloop()

