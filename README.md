# YouTubeの動画からQuestionAnsweringのデータセットを作成する

## 概要
YouTubeの動画からQuestionAnsweringのデータセットを作成するためのWebアプリケーションです。  
動画から自動で音声認識を行い、その結果を元に質問と回答のペアを作成します。  
質問と回答のペアは、動画の再生時間とともに表示されるので、簡単に確認することができます。  
下記２つのページから構成されています。
- YouTubeの動画を読み取り、音声ファイルを作成、文字起こしを行うページ
- 文字起こしした結果を元に質問に対する回答を作成するページ

YouTubeのロードにはPyTube、音声認識にはOpenAIのWhisperを使用しています。  
WhisperのモデルにはSmallを使用しています。  
テキストの分解、ベクトル化、QAの作成にはLangChainを使用しています。  


## 使い方
### パッケージのインストール
```shell
pip install -r requirements.txt
```
### ffmpegのインストール（Whisperで使用）
```shell
brew install ffmpeg
* mac環境の場合
* それぞれの環境にあったインストールを行ってください。
```

### envファイルの作成
[参考](https://platform.openai.com/account/api-keys)
```shell
.env.templateをコピーして.envを作成する。
.envの`OPENAI_API_KEY=`に自身が登録しているOpenAI APIで作成したAPIキーを記載する。
```

### frontendの起動
```shell
streamlit run app.py
```

### backendの起動
```shell
uvicorn main:app
```

### ブラウザで開く
```shell
http://localhost:8501/
```
1. サイドバーの「Transcription」を選択
2. YouTubeの動画URLを入力して「モデル作成」ボタンを押す
3. 「モデルを作成しました」が表示されるまで待つ（しばらーく待つ必要があります）
4. サイドバーの「Question」を選択
5. 質問したい動画を選択
6. 質問を入力して「回答を作成」ボタンを押す
7. 回答が表示されるので、確認する
