# text to slack gif

這是一個簡單的 Python 腳本，可以把文字轉成 slack 格式的 gif，解決你需要開好幾個線上服務一直轉換的問題。  
做出師表 gif 只需要一瞬間！  

This is a simple python script that can automatically convert text into slack gif.

Test on MacBook ok!  

## Basic usage

Download app.zip from [Releases](https://github.com/PttCodingMan/text_to_slack_gif/releases).
```bash
./app -t "臣亮言：先帝創業未半，而中道崩殂。今天下三分，益州疲弊，此誠危急存亡之秋也。"
```
or run python script.
```bash
python3 app.py -t "臣亮言：先帝創業未半，而中道崩殂。今天下三分，益州疲弊，此誠危急存亡之秋也。"
```
## Advanced usage
However, you can get different type gif by adjusting frame and delay.
The default values for frame and delay are 4 and 100 respectively.
```bash
python3 app.py -t "臣亮言：先帝創業未半，而中道崩殂。今天下三分，益州疲弊，此 誠危急存亡之秋也。"
```
![image](https://raw.githubusercontent.com/PttCodingMan/text_to_slack_gif/dev/src/%E8%87%A3%E4%BA%AE%E8%A8%80%20in%20f%205%20d%20100.gif)

```bash
python3 app.py -t "臣亮言：先帝創業未半，而中道崩殂。今天下三分，益州疲弊，此 誠危急存亡之秋也。" -f 1 -d 500
```
![image](https://raw.githubusercontent.com/PttCodingMan/text_to_slack_gif/dev/src/%E8%87%A3%E4%BA%AE%E8%A8%80%20in%20f%201%20d%20500.gif)

```bash
python3 app.py -t "臣亮言：先帝創業未半，而中道崩殂。今天下三分，益州疲弊，此 誠危急存亡之秋也。" -d 30
```
![image](https://raw.githubusercontent.com/PttCodingMan/text_to_slack_gif/dev/src/%E8%87%A3%E4%BA%AE%E8%A8%80%20in%20f%205%20d%2030.gif)

## Build
```bash
sh make.sh
```
