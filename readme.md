# text to slack gif

把一段文字轉成會捲動的 GIF，直接上傳當 Slack 自訂 emoji。

不用再到好幾個線上服務之間轉檔、裁切、壓縮，一個指令（或在 GitHub 上點幾下）就完成。

![臣亮言 範例](src/%E8%87%A3%E4%BA%AE%E8%A8%80%20in%20f%205%20d%20100.gif)

## 三種用法

| 用法 | 適合 | 需要什麼 |
| --- | --- | --- |
| [在 GitHub Actions 上跑](#在-github-actions-上跑免安裝) | 不想在電腦上裝 Python | GitHub 帳號 |
| [網頁版](#網頁版) | 想邊調參數邊看預覽 | 瀏覽器 |
| [在自己電腦上跑](#在自己電腦上跑) | 常常要產生、想寫成腳本 | Python 3.9 以上 |

## 在 GitHub Actions 上跑（免安裝）

GIF 會在 GitHub 的機器上產生，跑完再下載回來就好。因為 workflow 只能在你自己有權限的 repo 執行，所以**要先 fork 一份到自己的帳號**。

### 1. Fork 這個 repo

1. 登入 GitHub，打開 <https://github.com/PttCodingMan/text_to_slack_gif>。
2. 點右上角的 **Fork**，再按 **Create fork**。
3. 完成後會跳到 `https://github.com/<你的帳號>/text_to_slack_gif`，接下來的步驟都在這個 fork 裡做。

### 2. 啟用 Actions（只需要做一次）

GitHub 預設會關閉 fork 出來的 repo 的 workflow。

1. 在你的 fork 點上方的 **Actions** 分頁。
2. 看到 *Workflows aren't being run on this forked repository* 時，按 **I understand my workflows, go ahead and enable them**。

### 3. 執行 `build gif`

1. 在 Actions 分頁左側選 **build gif**。
2. 點右邊的 **Run workflow** 下拉選單，分支保持 `master`。
3. 填入文字，其他選項可以照預設，也可以調整（見下方 [選項說明](#選項說明)）。
4. 按綠色的 **Run workflow**。

### 4. 下載 GIF

1. 等一下下（通常不到一分鐘），列表最上面會出現一筆新的執行紀錄，點進去。
2. 出現綠色勾勾後，在 **Summary** 頁面可以看到這次用的參數。
3. 往下捲到 **Artifacts**，點檔名（預設是 `slack-gif`）下載。
4. 下載下來是 zip 檔，解壓縮就會拿到 `.gif`。

> Artifact 預設保留 90 天，過期就要重跑一次。

### 之後要更新

原作者更新後，在你的 fork 首頁點 **Sync fork** → **Update branch**，就能拿到新功能。

## 網頁版

`docs/index.html` 是純前端的版本，全部在瀏覽器裡跑，可以即時預覽、直接下載。字型用的是瀏覽器內建字型，所以結果可能跟 Python 版略有差異。

想放到線上，可以在你的 fork 開 GitHub Pages：

1. 到 fork 的 **Settings** → **Pages**。
2. **Source** 選 **Deploy from a branch**，Branch 選 `master`、資料夾選 `/docs`，按 **Save**。
3. 等一兩分鐘後就能在 `https://<你的帳號>.github.io/text_to_slack_gif/` 打開。

只想在本機用的話，直接用瀏覽器開 `docs/index.html` 也可以（需要連網載入 GIF 編碼套件）。

## 在自己電腦上跑

需要 Python 3.9 以上。

```bash
git clone https://github.com/PttCodingMan/text_to_slack_gif.git
```

```bash
cd text_to_slack_gif
```

```bash
pip install -r requirements.txt
```

```bash
python3 src/app.py -t "臣亮言：先帝創業未半，而中道崩殂"
```

產生的檔案是目前目錄下的 `output.gif`。

## 選項說明

| GitHub Actions 欄位 | 指令參數 | 說明 | 預設值 |
| --- | --- | --- | --- |
| Text | `-t`, `--text` | 要轉成 GIF 的文字（必填） | — |
| Theme | `--theme` | `dark` 黑底白字、`light` 白底黑字 | `dark` |
| Flashing background | `--flash` | `none` 不閃、`blink` 背景和文字顏色每格互換、`rainbow` 背景輪流換成彩虹七色 | `none` |
| Flash interval | `--flash-delay` | 閃背景時每隔幾毫秒換一次顏色，越小閃越快；和 `-d` 互相獨立 | `50` |
| Text color | `-c`, `--color` | 文字顏色，HTML/CSS 色名或 hex（如 `red`、`#ff8800`），會蓋過主題顏色 | 依主題 |
| Frames per character | `-f`, `--frame` | 每個字捲動幾格；`1` 是逐字跳出，數字越大捲動越平滑 | `5` |
| Delay | `-d`, `--delay` | 每格停留幾毫秒，越小越快 | `100` |
| Width | `-w`, `--width` | 畫面寬度，以「字」為單位；`1` 是 50×50 的正方形 emoji | `1` |
| File name | — | 下載檔名（不含 `.gif`），只有 Actions 版有 | `slack-gif` |

## 範例

調整 `-f`（每字格數）和 `-d`（每格毫秒數）可以做出不同節奏的效果。

預設：平滑捲動

```bash
python3 src/app.py -t "臣亮言..."
```

![f 5 d 100](src/%E8%87%A3%E4%BA%AE%E8%A8%80%20in%20f%205%20d%20100.gif)

逐字跳出，每個字停 0.5 秒

```bash
python3 src/app.py -f 1 -d 500 -t "臣亮言..."
```

![f 1 d 500](src/%E8%87%A3%E4%BA%AE%E8%A8%80%20in%20f%201%20d%20500.gif)

快速捲動

```bash
python3 src/app.py -d 30 -t "臣亮言..."
```

![f 5 d 30](src/%E8%87%A3%E4%BA%AE%E8%A8%80%20in%20f%205%20d%2030.gif)

其他組合：

```bash
# 白底黑字
python3 src/app.py --theme light -t "臣亮言..."

# 紫色字、5 個字寬的橫幅
python3 src/app.py -c blueviolet -w 5 -t "臣亮言..."

# 單一個字，黑白快速閃爍
python3 src/app.py -f 1 --flash blink -t "急"

# 彩虹背景
python3 src/app.py --flash rainbow -t "臣亮言..."
```

## 上傳到 Slack

在 Slack 的訊息輸入框點 emoji 圖示 → **Add Emoji**（新增表情符號），上傳 GIF 並取個名字即可。

Slack 自訂 emoji 的檔案上限是 128 KB。如果太大，可以縮短文字、把 `-f` 調小，或把 `-d` 調大以減少張數。

## License

[MIT](LICENSE)
