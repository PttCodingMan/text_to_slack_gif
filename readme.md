# text to slack gif

把一段文字轉成會捲動、會閃的 GIF，直接上傳當 Slack 自訂 emoji。

**線上直接用：<https://pttcodingman.github.io/text_to_slack_gif/>**（免安裝，打開瀏覽器就能產生、預覽、下載）

| 黑底白字 | 白底黑字 | 自訂背景 | 閃字 | 紅黃閃字 | 彩虹換色 | 自訂換色 |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| <img src="examples/dark.gif" width="100" alt="黑底白字"> | <img src="examples/light.gif" width="104" alt="白底黑字"> | <img src="examples/background.gif" width="100" alt="深藍底金字"> | <img src="examples/blink.gif" width="100" alt="閃字"> | <img src="examples/alert.gif" width="100" alt="紅黃閃字"> | <img src="examples/rainbow.gif" width="100" alt="彩虹換色"> | <img src="examples/rainbow-custom.gif" width="100" alt="自訂換色"> |

範例圖都是 50×50 的原尺寸放大兩倍顯示，每個選項的更多範例見 [選項說明](#選項說明)。白底範例外圍的灰框是為了在白色頁面上看得清楚另外加的，實際產生的 GIF 沒有框。

## 兩種用法

| 用法 | 適合 | 需要什麼 |
| --- | --- | --- |
| [網頁版](#網頁版) | 想邊調參數邊看預覽，最快上手 | 瀏覽器就好 |
| [指令版](#指令版) | 常常要產生、想寫成腳本 | Python 3.9 以上 |

## 網頁版

打開 <https://pttcodingman.github.io/text_to_slack_gif/> 就能用，不需要 GitHub 帳號。

1. **挑一個風格**：最上面的「風格範例」會用你輸入的文字預覽各種效果，點一下就套用那組設定。
2. **輸入文字**，需要的話再微調下面的參數，每個欄位下面都有簡短說明。
3. 確認預覽沒問題，按 **下載 output.gif**。

幾個小提醒：

- 全部在瀏覽器裡跑，文字不會上傳到任何地方。
- 顏色打錯時欄位會變紅，畫面會先用預設的顏色。
- 檔案超過 Slack 的 128 KB 上限時，檔案大小會變紅。
- 字型用的是瀏覽器內建字型，所以結果可能跟指令版略有差異。

網頁版的原始碼是 [`docs/index.html`](docs/index.html)，一個檔案就是全部。想架一份自己的（例如改了程式想自己用），可以 fork 之後開 GitHub Pages：

1. 到 fork 的 **Settings** → **Pages**。
2. **Source** 選 **Deploy from a branch**，Branch 選 `master`、資料夾選 `/docs`，按 **Save**。
3. 等一兩分鐘後就能在 `https://<你的帳號>.github.io/text_to_slack_gif/` 打開。

只想在本機用的話，直接用瀏覽器開 `docs/index.html` 也可以（需要連網載入 GIF 編碼套件）。

## 指令版

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

網頁版的欄位和指令版的參數一一對應：

| 網頁版欄位 | 指令參數 | 說明 | 預設值 |
| --- | --- | --- | --- |
| 文字 | `-t`, `--text` | 要轉成 GIF 的文字（必填） | — |
| 主題 | `--theme` | `dark` 黑底白字、`light` 白底黑字 | `dark` |
| 文字顏色 | `-c`, `--color` | 蓋過主題的文字顏色 | 依主題 |
| 背景顏色 | `-b`, `--background` | 蓋過主題的背景顏色 | 依主題 |
| 每字格數 | `-f`, `--frame` | 每個字捲動幾格；`1` 是逐字跳出，數字越大捲動越平滑 | `5` |
| 每格毫秒 | `-d`, `--delay` | 每格停留幾毫秒，越小越快 | `100` |
| 寬度 | `-w`, `--width` | 畫面寬度，以「字」為單位；`1` 是 50×50 的正方形 emoji | `1` |
| 閃爍效果 | `--flash` | `none` 不閃、`blink` 閃字（背景和文字顏色互換）、`rainbow` 背景換色（背景在幾個顏色之間輪流閃） | `none` |
| 閃爍間隔 | `--flash-delay` | 每隔幾毫秒換一次顏色，越小閃越快；和每格毫秒分開算 | `50` |
| 背景輪流的顏色 | `--flash-colors` | 背景換色時輪流的顏色，至少兩個，用逗號分隔 | 彩虹七色 |

下面逐一說明每個選項的效果，以及怎麼搭配使用。

### 文字 `-t`

要顯示的內容，中英文和標點符號都可以（字型不支援彩色 emoji，會顯示不出來）。

- 連續的空白和換行會被合併成一個空格。
- 逐字模式（`-f 1`）會跳過空白，英文字母會置中，中文字則靠左對齊並填滿畫面。
- 文字越長，GIF 張數越多、檔案越大。

### 主題 `--theme`

決定預設的背景色和文字顏色：

| 值 | 背景 | 文字 |
| --- | --- | --- |
| `dark` | 黑 | 白 |
| `light` | 白 | 黑 |

| `--theme dark`（預設） | `--theme light` |
| :---: | :---: |
| <img src="examples/dark.gif" width="100" alt="黑底白字"> | <img src="examples/light.gif" width="104" alt="白底黑字"> |

主題只決定「預設」顏色，可以再用文字顏色、背景顏色個別蓋過。

### 文字顏色 `-c`、背景顏色 `-b`

分別蓋過主題的文字顏色和背景顏色，可以只設其中一個。顏色支援這些寫法：

- 色名：`red`、`gold`、`navy`、`blueviolet`（[CSS 色名列表](https://developer.mozilla.org/en-US/docs/Web/CSS/named-color)）
- 16 進位：`#f80`、`#ff8800`
- 函式：`rgb(255, 136, 0)`、`hsl(32, 100%, 50%)`

| `-c gold` | `-b navy -c gold` |
| :---: | :---: |
| <img src="examples/color.gif" width="100" alt="黑底金字"> | <img src="examples/background.gif" width="100" alt="深藍底金字"> |

顏色寫錯時，指令版會直接報錯並說明是哪個參數；網頁版則會把欄位標紅，先用預設的顏色。

### 捲動方式 `-f`

決定文字「怎麼動」：

- **`-f 1`：逐字跳出。** 一格顯示一個字，像跑馬燈一樣一個字一個字換。適合短詞，或搭配閃爍做「急」、「讚」這類單字 emoji。
- **`-f 2` 以上：平滑捲動。** 整串文字從右往左滑過畫面，每個字要滑 `f` 格才會完全移過去。數字越大越平滑，但張數也越多（大約是「字數 × f」張）。

| `-f 1 -d 500`：逐字跳出 | `-f 5`（預設）：平滑捲動 |
| :---: | :---: |
| <img src="examples/step.gif" width="100" alt="逐字跳出"> | <img src="examples/dark.gif" width="100" alt="平滑捲動"> |

可以填 `1`～`50`，建議用 `1`～`10`。畫面只有 50 px 寬，每格至少要移動 1 px，所以上限是 `50`：指令版填超過會直接報錯，網頁版則會自動當成 `50`。

### 速度 `-d`

每一格停留幾毫秒，數字越小越快。

- 逐字模式下就是每個字停多久，例如 `-f 1 -d 500` 是每個字停 0.5 秒。
- 捲動模式下，一個字滑過去的時間大約是 `f × d` 毫秒，例如預設 `-f 5 -d 100` 是每個字 0.5 秒。想要同樣捲動速度但更平滑，可以把 `f` 加倍、`d` 減半。
- GIF 的時間單位是 10 毫秒，數值會被四捨五入到 10 的倍數。
- 很多瀏覽器和 App 會把 20 毫秒以下的格子放慢成 100 毫秒，所以 `-d` 不要低於 `20`。

| `-d 100`（預設） | `-d 30`：快速捲動 |
| :---: | :---: |
| <img src="examples/dark.gif" width="100" alt="預設速度"> | <img src="examples/fast.gif" width="100" alt="快速捲動"> |

### 寬度 `-w`

畫面寬度，以「字」為單位，高度固定 50 px：

- `-w 1`：50×50 正方形，最適合當 emoji。
- `-w 4`：200×50 的橫幅，一次能看到好幾個字，適合搭配捲動模式。

逐字模式（`-f 1`）的字只會出現在最左邊那格，所以寬度大於 1 時建議用捲動模式。

`-w 4`：

<img src="examples/wide.gif" width="400" alt="200×50 橫幅">

### 閃爍效果 `--flash`

讓背景閃爍，做出「警告」、「慶祝」之類很吵的 emoji。有三種模式：

| 值 | 效果 |
| --- | --- |
| `none` | 不閃（預設） |
| `blink` | **閃字：背景和文字顏色互換。** 預設是黑底白字 ↔ 白底黑字輪流切換，看起來字和背景一起在閃。 |
| `rainbow` | **背景換色：背景在幾個顏色之間輪流閃**，文字顏色不變。預設是彩虹七色（紅、橙、黃、綠、青、藍、紫），可以換成自己挑的顏色（見下方）。 |

| `--flash blink` | `--flash rainbow` | `--flash rainbow -c black` | `-f 1 -d 500 --flash blink` | `-f 1 -d 500 --flash rainbow` |
| :---: | :---: | :---: | :---: | :---: |
| <img src="examples/blink.gif" width="100" alt="閃字"> | <img src="examples/rainbow.gif" width="100" alt="彩虹換色"> | <img src="examples/rainbow-black.gif" width="100" alt="彩虹換色黑字"> | <img src="examples/blink-char.gif" width="100" alt="急 閃爍"> | <img src="examples/rainbow-char.gif" width="100" alt="讚 彩虹換色"> |

後兩個是單一個字（「急」、「讚」）配逐字模式，最常拿來當 emoji。白字在彩虹的亮色背景上比較不明顯，可以用 `-c black` 之類的深色字。

#### 自訂閃爍的顏色組合

- **閃字**：互換的兩個顏色就是文字顏色和背景顏色，所以用 `-c`、`-b` 就能自訂。例如 `-c yellow -b red` 是紅底黃字 ↔ 黃底紅字。
- **背景換色**：想讓背景在自己挑的幾個顏色之間閃，就選背景換色，再到網頁版的「背景輪流的顏色」填顏色（指令版用 `--flash-colors`）。至少兩個，用逗號分隔，例如 `red, yellow, blue`。這個欄位只在背景換色時有作用，指令版搭配其他模式會報錯。

| `--flash blink -b red -c yellow` | `-f 1 -d 500 --flash blink -b red -c yellow` | `-f 1 -d 500 --flash rainbow --flash-colors "#ff4fa3,#ffd400,#00d1ff" -c black` |
| :---: | :---: | :---: |
| <img src="examples/blink-custom.gif" width="100" alt="紅黃閃字"> | <img src="examples/alert.gif" width="100" alt="急 紅黃閃字"> | <img src="examples/rainbow-custom.gif" width="100" alt="讚 自訂換色"> |

#### 閃爍速度 `--flash-delay`

每隔幾毫秒換一次背景色，預設 `50`，數字越小閃越快。它和 `-d` 是分開的：文字的移動節奏照 `-d`，背景在這段時間內另外閃好幾下。例如：

```bash
# 每個字停 0.5 秒，這段時間內背景每 0.05 秒換一次色（閃 10 下）
python3 src/app.py -f 1 -d 500 --flash blink --flash-delay 50 -t "急"
```

幾個要注意的地方：

- 實際的閃爍間隔是「把 `-d` 平均切成幾段」算出來的，所以會是接近、但不一定剛好等於你填的數字。
- 每段最短 20 毫秒（理由同上，太短會被瀏覽器放慢），填更小的值也只會閃到 20 毫秒。
- 如果 `--flash-delay` 比 `-d` 還大，就是每格換一次色，閃爍速度等於文字移動速度。
- 閃爍會讓張數變成好幾倍，檔案也會跟著變大。為了讓循環播放時不會斷拍，`blink` 會讓總張數維持偶數；很短的 `rainbow` 動畫會重複到每個顏色都輪過一次。

## 範例指令

上面的範例圖都放在 [`examples/`](examples)，用下面的指令產生（產生的檔案都叫 `output.gif`）：

```bash
# 黑底白字（預設）
python3 src/app.py -t "臣亮言：先帝創業未半"

# 白底黑字
python3 src/app.py --theme light -t "臣亮言：先帝創業未半"

# 自訂背景：深藍底金字
python3 src/app.py -b navy -c gold -t "臣亮言：先帝創業未半"

# 閃字：黑底白字 ↔ 白底黑字互換
python3 src/app.py --flash blink -t "臣亮言：先帝創業未半"

# 紅黃閃字：紅底黃字 ↔ 黃底紅字
python3 src/app.py --flash blink -b red -c yellow -t "臣亮言：先帝創業未半"

# 單一個字，每 0.5 秒一輪，紅黃快速閃爍
python3 src/app.py -f 1 -d 500 --flash blink -b red -c yellow -t "急"

# 背景換色（彩虹七色），黑字
python3 src/app.py --flash rainbow -c black -t "臣亮言：先帝創業未半"

# 背景換色，自己挑顏色
python3 src/app.py -f 1 -d 500 --flash rainbow --flash-colors "#ff4fa3,#ffd400,#00d1ff" -c black -t "讚"

# 逐字跳出
python3 src/app.py -f 1 -d 500 -t "臣亮言：先帝創業未半"

# 4 個字寬的橫幅
python3 src/app.py -w 4 -t "臣亮言：先帝創業未半"
```

## 上傳到 Slack

在 Slack 的訊息輸入框點 emoji 圖示 → **Add Emoji**（新增表情符號），上傳 GIF 並取個名字即可。

Slack 自訂 emoji 的檔案上限是 128 KB。如果太大，可以縮短文字、把 `-f` 調小、關掉閃爍，或把 `--flash-delay` 調大以減少張數。

## License

[MIT](LICENSE)
