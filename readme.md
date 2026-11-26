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

下面逐一說明每個選項的效果，以及怎麼搭配使用。

### 文字 `-t` / Text

要顯示的內容，中英文和標點符號都可以（字型不支援彩色 emoji，會顯示不出來）。

- 連續的空白和換行會被合併成一個空格。
- 逐字模式（`-f 1`）會跳過空白，英文字母會置中，中文字則靠左對齊並填滿畫面。
- 文字越長，GIF 張數越多、檔案越大。

### 主題 `--theme` / Theme

決定預設的背景色和文字顏色：

| 值 | 背景 | 文字 |
| --- | --- | --- |
| `dark` | 黑 | 白 |
| `light` | 白 | 黑 |

主題只決定「預設」顏色；用 `-c` 指定文字顏色後，背景仍然照主題。

### 文字顏色 `-c` / Text color

覆蓋主題的文字顏色，支援這些寫法：

- 色名：`red`、`gold`、`blueviolet`（[CSS 色名列表](https://developer.mozilla.org/en-US/docs/Web/CSS/named-color)）
- 16 進位：`#f80`、`#ff8800`
- 函式：`rgb(255, 136, 0)`、`hsl(32, 100%, 50%)`

寫錯色名會直接報錯（`unknown color specifier`），在 Actions 上會看到執行失敗的紅叉。

### 捲動方式 `-f` / Frames per character

決定文字「怎麼動」：

- **`-f 1`：逐字跳出。** 一格顯示一個字，像跑馬燈一樣一個字一個字換。適合短詞，或搭配閃爍做「急」、「讚」這類單字 emoji。
- **`-f 2` 以上：平滑捲動。** 整串文字從右往左滑過畫面，每個字要滑 `f` 格才會完全移過去。數字越大越平滑，但張數也越多（大約是「字數 × f」張）。

建議用 `1`～`10`，**不要超過 `50`**：畫面只有 50 px 寬，超過 50 時每格移動量會變成 0，程式會卡住跑不完。

### 速度 `-d` / Delay

每一格停留幾毫秒，數字越小越快。

- 逐字模式下就是每個字停多久，例如 `-f 1 -d 500` 是每個字停 0.5 秒。
- 捲動模式下，一個字滑過去的時間大約是 `f × d` 毫秒，例如預設 `-f 5 -d 100` 是每個字 0.5 秒。想要同樣捲動速度但更平滑，可以把 `f` 加倍、`d` 減半。
- GIF 的時間單位是 10 毫秒，數值會被四捨五入到 10 的倍數。
- 很多瀏覽器和 App 會把 20 毫秒以下的格子放慢成 100 毫秒，所以 `-d` 不要低於 `20`。

### 寬度 `-w` / Width

畫面寬度，以「字」為單位，高度固定 50 px：

- `-w 1`：50×50 正方形，最適合當 emoji。
- `-w 5`：250×50 的橫幅，一次能看到好幾個字，適合搭配捲動模式。

逐字模式（`-f 1`）的字只會出現在最左邊那格，所以寬度大於 1 時建議用捲動模式。

### 閃爍效果 `--flash` / Flashing background

讓背景閃爍，做出「警告」、「慶祝」之類很吵的 emoji。有三種模式：

| 值 | 效果 |
| --- | --- |
| `none` | 不閃（預設） |
| `blink` | **背景和文字顏色互換**：黑底白字 ↔ 白底黑字輪流切換，看起來字和背景一起在閃。有設 `-c` 的話就是兩個顏色互換，例如 `-c red` 會變成黑底紅字 ↔ 紅底黑字。 |
| `rainbow` | **背景輪流換成彩虹七色**（紅、橙、黃、綠、青、藍、紫），文字顏色不變。白字在亮色背景上比較不明顯，可以用 `-c black` 之類的深色字試試。 |

**閃爍速度 `--flash-delay` / Flash interval**

每隔幾毫秒換一次背景色，預設 `50`，數字越小閃越快。它和 `-d` 是分開的：文字的移動節奏照 `-d`，背景在這段時間內另外閃好幾下。例如：

```bash
# 每個字停 0.5 秒，這段時間內背景每 0.05 秒換一次色（閃 10 下）
python3 src/app.py -f 1 -d 500 --flash blink --flash-delay 50 -t "急"
```

幾個要注意的地方：

- 實際的閃爍間隔是「把 `-d` 平均切成幾段」算出來的，所以會是接近、但不一定剛好等於你填的數字。
- 每段最短 20 毫秒（理由同上，太短會被瀏覽器放慢），填更小的值也只會閃到 20 毫秒。
- 如果 `--flash-delay` 比 `-d` 還大，就是每格換一次色，閃爍速度等於文字移動速度。
- 閃爍會讓張數變成好幾倍，檔案也會跟著變大。為了讓循環播放時不會斷拍，`blink` 會讓總張數維持偶數；很短的 `rainbow` 動畫會重複到七個顏色都輪過一次。

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

Slack 自訂 emoji 的檔案上限是 128 KB。如果太大，可以縮短文字、把 `-f` 調小、關掉閃爍，或把 `--flash-delay` 調大以減少張數。

## License

[MIT](LICENSE)
