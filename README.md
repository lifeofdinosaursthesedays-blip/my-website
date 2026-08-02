# 5度圏ルーレット（PWA）

スマホのホーム画面に置いて、アイコンから全画面で起動できるようにしたものです。
インストール後はオフラインでも動きます。ストア審査も費用も不要です。

## ファイル

| ファイル | 役割 |
|---|---|
| `index.html` | アプリ本体（1ファイル完結） |
| `manifest.webmanifest` | アプリ名・アイコン・全画面表示の設定 |
| `sw.js` | オフライン用サービスワーカー |
| `icon-*.png` / `apple-touch-icon.png` | ホーム画面アイコン |
| `make_icons.py` | アイコン生成スクリプト（再生成したいとき用） |
| `.nojekyll` | GitHub Pages の余計な変換を止める空ファイル（隠しファイル） |

## 公開する（どれか1つ）

**サービスワーカーは HTTPS（または localhost）でしか動きません。** 下記はどれも HTTPS です。

### A. GitHub Pages（無料・おすすめ）

ブラウザだけで完結します。コマンドもトークンも不要です。

**1. リポジトリを作る**

https://github.com/new を開き、

- Repository name: `circle-of-fifths`（好きな名前でOK）
- **Public を選ぶ**（無料アカウントでは Private だと Pages が使えません）
- 「Add a README file」などのチェックは**すべて外す**
- 「Create repository」

**2. ファイルを上げる**

作成直後の画面にある **「uploading an existing file」** のリンクを押し、
このフォルダの中身を**ファイルごと全部**（フォルダごとではなく中身を）ドラッグ＆ドロップ。
`.nojekyll` は隠しファイルなので、Finder で `command + shift + .` を押すと見えるようになります。

下の「Commit changes」を押す。

**3. Pages を有効にする**

リポジトリの **Settings** → 左メニューの **Pages** →
Build and deployment の Source を **Deploy from a branch**、
Branch を **main** / **/(root)** にして **Save**。

1〜2分待ってページを再読み込みすると、上部に URL が出ます。

```
https://<ユーザー名>.github.io/circle-of-fifths/
```

**4. スマホで開いてホーム画面に追加**（下の手順へ）

#### コマンドラインで行う場合

`git config` の名前・メール設定と、パスワードの代わりの
Personal Access Token（または SSH 鍵）が別途必要です。上のブラウザ手順の方が簡単です。

```bash
cd circle-of-fifths-pwa
git init && git add -A
git -c user.name="あなたの名前" -c user.email="you@example.com" commit -m "5度圏ルーレット"
git branch -M main
git remote add origin https://github.com/<ユーザー名>/<リポジトリ名>.git
git push -u origin main
```

### B. Netlify Drop（アカウント不要・最速）

https://app.netlify.com/drop にフォルダごとドラッグ＆ドロップするだけ。すぐ URL が発行されます。

### C. Cloudflare Pages

ダッシュボードの Workers & Pages → Create → Pages → Upload assets からフォルダをアップロード。

## ホーム画面に追加する

**iPhone（Safari で開く）**
共有ボタン → 「ホーム画面に追加」 → 追加

Safari 以外のブラウザだと項目が出ないことがあります。Safari で開いてください。

**Android（Chrome）**
メニュー（⋮） → 「アプリをインストール」 または 「ホーム画面に追加」

追加後はアイコンから全画面で起動し、機内モードでも遊べます。

## 遊び方

「回す」で輪が回転して止まり、ポインタが指した1マスだけが表示されます。
その隣接5マスのどれかが金色に光るので、そこに入る調を答えます。

- スマホ: ♮/♯/♭ を選んでから音名をタップ（1〜2タップで解答）
- PC: そのままキーボードで入力して Enter（`F#` `Bb` `Am` いずれの書き方でも可）
- 短調のマスは音名だけで正解になります（`Gm` は `G` でも可）
- 異名同音も正解扱い（G♭の位置に `F#`、Bの位置に `Cb` など）

レベルとテーマの設定は端末に保存され、次回起動時も引き継がれます。

## アプリを更新したとき

**`sw.js` の `CACHE` の版数を必ず上げてください。**

```js
const CACHE = "cof-v2";   // v1 → v2 のように
```

サービスワーカーはキャッシュ優先で配信するため、版数を変えないと
インストール済みの端末が古い画面を表示し続けます。
版数を上げると、次回起動時に新しいキャッシュへ入れ替わります。

## ローカルで確認する

```bash
cd circle-of-fifths-pwa && python3 -m http.server 8000
```

`http://localhost:8000/` を開きます（localhost はサービスワーカーが動く例外扱いです）。
