# OpenAIとラズパイで動かす鉄道模型

## 概要
ラズパイとOpenAI(GPT)を使ってNゲージ鉄道模型を制御します。ずいぶん昔に声で動かせるプラレールがありましたが、同じ気分で鉄道模型も制御できたらいいなと思って作りました。

## ハードウェア構成
- Raspberry Pi 4 (4GB)
  - 特にRaspberry Pi 4である必要も、4GBモデルである必要もありません。2ch分のPWM出力ができればOKです。
- 12V DC電源
  - Nゲージは12VのDC電源で動作するため、その電源です。
- モータードライバー等の回路
  - ラズパイから直接Nゲージ用のDC電源を出力することはできないため、モータードライバーが必要です。参考までに今回使用したモータードライバーICと部品を紹介します。
    - モータードライバー TB6643KQ
    - 積層セラミックコンデンサ 0.1μF (電源電圧(12V)とGNDの間に配置)
    - 電解コンデンサ 100μF (電源電圧VM(12V)とGNDの間に配置)


## ソフトウェア構成
ラズパイのOSとしてはRaspberry Pi OS (32-bit)を使用しています。
<br>
ラズパイのGPIOの制御にはpigpioライブラリを使用しています。

プログラムについてはPythonを使用します。インストールが必要なパッケージについてはrequirements.txtに記載しています。今回の目玉であるopenaiもインストールします。

また、OpenAIのAPIを使用するので、OpenAIの有料クレジットを購入する必要があります。GPT3.5を使用しているため、比較的安価ではありますが、ユーザープロンプトを受け付けるたびに課金されることは留意してください。


## セットアップ＆実行
特に記載がない限りこれらのコマンドはラズパイ上で実行します。
<br>
また、環境変数にOpenAIのAPI Keyが登録されている前提となっていますので、OpenAIのAPI Keyを発行し、環境変数として登録しておいてください。

まず最初にpigpioライブラリをインストールします。
```
sudo apt install pigpio
```

pigpioのインストールが終わったら、pigpioのdaemonを実行しておきます。
```
sudo pigpiod
```

Gitリポジトリのクローン後、Pythonの仮想環境を作成する場合は以下のコマンドを実行して仮想環境を作ります。

```
python -m venv .venv
```

requirements.txtのパッケージをインストールします。

```
pip install -r requirements.txt
```

次にアプリケーションコード(main.py)を実行します。

```
python main.py
```

ユーザープロンプトを入力するように言われるので、日本語で命令を入力してください。

```
Insert user prompt (in Japanese):走れ
```

以下のようなレスポンスが表示され、鉄道模型が動き始めます。
<br>
モーターへの負荷軽減のため、突然スピードが増減しないよう、徐々にスピードが増減するようなコードとなっています。PWMのデューティー比を増減させることでスピードの制御をしています。

```
{
  "role": "assistant",
  "content": null,
  "function_call": {
    "name": "operate_vehicle",
    "arguments": "{\n  \"direction\": \"forward\",\n  \"speed\": 100\n}"
  }
}
command accepted, direction: forward, speed: 100
self.direction forward, self.speed 0
self.direction forward, self.speed 1
self.direction forward, self.speed 2
self.direction forward, self.speed 3

...

```

止まらせたい時は「止まれ」という命令などが実行可能です。

```
Insert user prompt (in Japanese):止まれ
```

また、反対方向に車両を走らせることや、ゆっくり走らせることなども可能です。ぜひ色々なプロンプトを使ってみてください。

```
Insert user prompt (in Japanese):逆方向に走れ
```

```
Insert user prompt (in Japanese):ゆっくり走れ
```


最後に、プログラムを終了させるときは、何も入力せずEnterを押してください。この時、まだ車両が動いている場合は停止させる処理が走ったのちにプログラムは停止します。
```
Insert user prompt (in Japanese):
```
