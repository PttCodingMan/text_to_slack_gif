# text to slack gif

This is a simple Python script that can convert text to gif in slack format.  
This script solves the problem that you need to use several online services to do this.  
And the more important thing is it saves your time!

## Basic usage

### Run on GitHub Actions

1. Fork this repository.
2. Go to the Actions tab and enable workflows.
3. Select `build gif` workflow.
4. Click `Run workflow` button.
5. Input the text you want to convert, and adjust the other options if you like:

   | Option | Description | Default |
   | --- | --- | --- |
   | Text | The text to convert | 臣亮言… |
   | Theme | `dark` (white text on black) or `light` (black text on white) | `dark` |
   | Flashing background | `none`, `blink` (background and text colors swap every frame) or `rainbow` (background cycles through colors) | `none` |
   | Text color | HTML/CSS color name or hex (e.g. `red`, `#ff8800`); leave blank to use the theme color | blank |
   | Frames per character | `1` shows one character at a time; larger values scroll more smoothly | `5` |
   | Delay | Milliseconds per frame; smaller is faster | `100` |
   | Width | Image width in characters; `1` is a square emoji | `1` |
   | File name | Name of the downloaded gif (without `.gif`) | `slack-gif` |

6. Download the gif from the Artifacts. The run summary also lists the options that were used.

### Run on your local machine

1. Clone this repository.
2. Install the required packages.
3. Run the script.

```bash
python3 src/app.py -t "臣亮言..."
```

## Advanced usage

However, you can get different type gif by adjusting frame and delay.  
The default values for frame and delay are 5 and 100 respectively.

```bash
python3 src/app.py -t "臣亮言..."
```
![image](https://raw.githubusercontent.com/PttCodingMan/text_to_slack_gif/master/src/%E8%87%A3%E4%BA%AE%E8%A8%80%20in%20f%205%20d%20100.gif)

```bash
python3 src/app.py -f 1 -d 500 -t "臣亮言..."
```
![image](https://raw.githubusercontent.com/PttCodingMan/text_to_slack_gif/master/src/%E8%87%A3%E4%BA%AE%E8%A8%80%20in%20f%201%20d%20500.gif)

```bash
python3 src/app.py -d 30 -t "臣亮言..."
```
![image](https://raw.githubusercontent.com/PttCodingMan/text_to_slack_gif/master/src/%E8%87%A3%E4%BA%AE%E8%A8%80%20in%20f%205%20d%2030.gif)

## Theme

Add `--theme <dark/light>` argument to change the theme of the gif. Default is `dark`.

- `dark`: Black background with white text.
- `light`: White background with black text.

```bash
python3 src/app.py --theme light -t "臣亮言..."
```

## Flashing background

Add `--flash <none/blink/rainbow>` argument to make the background flash. Default is `none`.

- `none`: No flashing.
- `blink`: The background and text colors swap every frame, e.g. white on black ↔ black on white.
- `rainbow`: The background cycles through rainbow colors; the text keeps its color.

```bash
python3 src/app.py -f 1 --flash blink -t "急"
python3 src/app.py --flash rainbow -t "臣亮言..."
```

## Font color

Add `-c <HTML/CSS Color Name>` or `--color=<HTML/CSS Color Name>` argument to change font color; type=str. This will override the default color of the selected theme.

```bash
python3 src/app.py -c blueviolet -t "臣亮言..."
```
![image](https://github.com/PersonalComputerRetailer/text_to_slack_gif/blob/dev/src/%E8%87%A3%E4%BA%AE%E8%A8%80%EF%BC%9A%E5%85%88%20in%20f%205%20d%20100_violet.gif)

## Width of image

Add `-w <int>` or `--width=<int>` argument to change width of image; type=int. Default is 1. 

```bash
python3 src/app.py -c blueviolet -w 5 -t "臣亮言..."
```
![image](https://github.com/PersonalComputerRetailer/text_to_slack_gif/blob/dev/src/%E8%87%A3%E4%BA%AE%E8%A8%80%EF%BC%9A%E5%85%88%20in%20f%205%20d%20100_violet_w5.gif)

