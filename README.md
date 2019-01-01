# perspective_grid_eqrect
正距円筒図法(Equirectangular)に則ったグリッド状の
“パースガイド”を計算して、画像生成します。

---
## 概要
全天球イラストを描く際に、
正距円筒図法に則ったパースガイド計算が必要になりますが、
このスクリプトは水平グリッド状のパースガイドを計算して、
PNG画像を生成・描画します。
PNG画像はパースガイド面以外は透過して生成しますので、
Photoshop等のペイントソフトにレイヤーとしてすぐに読み込めて
作画作業に入ることができます。  
いちおう「水平パースガイド生成」「垂直パースガイド生成(垂直面の傾斜角も指定可能)」
「円ガイド生成」「太陽光によってできる影(平行光源)計算」の4つの機能をスクリプトとして提供しますが、このうち
**「水平パースガイドの生成」のみGUI対応しています。**
以下の使い方は「水平パースガイド生成」についてのみ対象としたものです。


---
## 動作環境(使用モジュール)
* Python(Anaconda) 3.6.4(5.1.0)
* tkinter 8.6
* numpy 1.14.0
* pillow 5.0.0

---
## 簡単な使い方
※拙著[「全天球イラストの描き方」](https://www.pixiv.net/user/810920/series/41910)
をまずはご覧頂き、用語や概念を理解した上で以下の使い方をお読みください。

### "setting_horz_plane_pers_grid.py"を呼び出す
"setting_horz_plane_pers_grid.py"を呼び出すと、
以下のようなGUI設定画面が立ち上がります。
![水平パースガイド生成](img/setting_horz_plane_pers_grid.png)

### 設定値の入力
設定値については、以下の概念図も併せてご覧下さい。  
![水平パースガイド概念図](img/abstract.png)

説明で頻繁に出てくる“ベースObject Point(Base OP)”とは、
パース面生成の基点となるOPのことで、図中の黒塗り潰しの点のことを指します。  

| 名前 | format| 初期値 |概要|
|:---|:---|:---|:---|
|ベースAz |float |155.0 |Base OPが向いている方位角。0 <= ベースAz < 360[度]で指定。|
|D(ベースObject Point) |float |16.0 |SPからBase OPまでの前進距離。前進方向がプラス。D > 0 で指定のこと。|
|W(ベースObject Point) |float |-30.0 |SPからBase OPまでの、垂直面からの横方向の距離。右方向がプラス。左方向がマイナス。|
|H(ベースObject Point) |float(,　float...) |-180,　-120,　-60,　3.3,　6.6|SPからBase OPまでの、水平面からの縦方向の距離。上方向がプラス。下方向がマイナス。この項目だけは複数の数値を入力することができて、カンマで区切って数値を指定すると、その数だけ水平面パースガイド(画像)が生成されます。ひとつだけパース面を生成したい場合は、ひとつの数値(高さ)を指定してください。|
|Width Division|float |10.0 |Base OPから横方向の格子点間隔。プラスだとSPから見て右方向に、マイナスだと左方向に生成。|
|Width Count|int|7 |横方向の格子点の数。正の整数で指定。必ず1以上を指定のこと。|
|Depth Division|float |10.0 |Base OPから奥行き方向の格子点間隔。プラスだとSPから見て奥方向に、マイナスだと手前方向に生成。だけど、D=0があると(SPと重なると)正接の計算ができないので基本はプラスに指定した方が無難です。|
|Depth Count|int|4|奥行き方向の格子点の数。正の整数で指定。必ず1以上を指定のこと。|

| 名前  |概要|
|:---|:---|
|OPの“点”を描画する|OPの“点”を描画するかどうか。通常はなくてもいい気がする。|
|正方グリッドを描画する|PNG画像内に正距円筒図法の正方グリッドを描画するかどうか。チェックをいれると、Az=(0, 90, 180, 270, 360), Ev=(-90, 0, 90) の位置にグレーのラインが描画されます。|
|パースガイドの色|パースガイドを任意の色にしたい場合、チェックを入れて右のボタンで色を指定してください。複数の水平パース面を生成する際も、パースガイドの色はこの1色で書き出されます。このチェックを入れない場合、パースガイドの色は自動で決定します。複数の水平パースを生成するときは、いろんな色で出力されるため、作画時の視認性が良いかと。|

### 画像生成
設定値を入力したら「パースガイド画像生成」ボタンを押下すると、水平パース面を計算してPNG画像を生成します。  
保存場所はスクリプト実行時のカレントディレクトリ。保存ファイル名は「horzPersGuide(00.0).png」で決め打ち(“00.0”はH(ベースObject Point)で設定した数値)。同名ファイルが既にある場合は上書きしてしまうため、生成後は待避させましょう。

### 設定値の保存
「設定値保存」ボタンを押下すると、現在の設定値を保存することができます。
保存した設定値はGUI(設定画面)を閉じても保持され、次回起動時に自動的にロード・反映されます。  
設定値は「setting.json」に記録しています。設定値を初期化したい場合は、このリポジトリの「setting.json」を、ご自身のワーキングツリーに対して`fetch`した後に`checkout`すれば初期値にリセットされます。(別にローカルリポジトリ全体を`reset`してもいいけど)  

---

## 今後やること(確定はしていない)
### いろんな画像サイズ対応
今のところ5376 X 2688のみ対応です。

### 機能を整理して実装し直し
概要にも書きましたが、現在まともにインターフェイスをもっているのは
「水平パースガイド生成」のみです。
* 垂直パースガイド生成(vert_plane_pers_grid.py)
* 円ガイド生成(circle_plane_pers_grid.py)
* 太陽光によってできる影(平行光源)計算(calc_directional_light.py)

上記は個別スクリプトとして実装してありますが、どれも設定値を入力するためのインターフェイスは無く、スクリプト内の数値(定数)を直接書き換えて実行するというスタイルです。  
このため、機能を整理して「水平パースガイド生成(pers_grid_exec.py)」に統合することを企んでいます。

### 機能整理するときに、中途半端なクラス実装をもうちっとなんとかする…
いかんせん、イラスト制作の時に必要に迫られてだだーっと作ったモノたちばかりなので、
プログラムの抽象化がほとんどなされていません。
後から作った「円ガイド生成」あたりになると、「これオブジェクトでまとめた方がラクじゃね？」という事に気付きクラス実装を始めてみましたが、最初に作った「水平&垂直パースガイド生成」のほうは置いてけぼりのままで、なんとも中途半端なことになってます・・・

---

## 免責事項
このプログラムはそもそも展開用に書いたものではないので、ドキュメント等はありません(書く予定もありません)。従って、このREADMEおよび備忘録的に書いたソース内のコメントを頼りに、Pythonコードを解析できる人のみ利用してください。  
ライセンスはGPLに準拠します。利用の際は、作者は一切の責任(サポート等)を負わないものとします。  
もともと作者(わたなべ:mana544)が全天球イラスト制作用に個人的に描いた汎用性のないスクリプトなので、ソース(構造含む)が汚いのはご容赦を。合間見てちょぼちょぼ修正入れていきます。Fork大歓迎(誰か抽象化してクラスで書いてくれないかな…)

