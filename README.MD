# 偷鸡摸鱼工具包
## 1. 介绍
本工具包集成了部分自动化工具，用于提高工作效率，减少重复劳动。

## 2. 使用说明
### 2.1. 依赖
- Python 3.8+
- Flask
- Flask-Cors
- pystray
- pillow
- PyAutoGUI

### 2.2. 使用方法
1. 安装依赖
```pip install -r requirements.txt```
2. 运行
```python main.py```
3. 在系统托盘中找到图标，点击选择需要的功能即可

## 3. 功能
### 3.1. 保持Teams在线
- 功能：自动模拟鼠标移动，每10秒随机移动0~1px，保持屏幕唤醒状态，防止Teams自动离线
- 使用：点击系统托盘图标，选择“保持Teams在线”
- 注意：使用过程中出现鼠标自动偏移1px的情况，是正常现象，不影响使用
- 关闭：点击系统托盘图标，取消选择“保持Teams在线”

### 3.2. Dingtalk自动签到脚本生成器
- 功能：生成钉钉自动签到脚本（AutoX脚本）
- 使用：点击系统托盘图标，选择“钉钉打卡脚本”，自动打开浏览器，按需要生成脚本
- 注意：生成的脚本仅供参考，具体使用请根据实际情况修改
- todo:
- [ ] 生成脚本后自动复制到剪贴板
- [ ] 保存到文件
- [ ] 屏幕自动解锁
- [ ] OCR识别打卡页面（WebView）的元素位置
- [ ] OCR识别是否打卡成功
- [ ] 公众号推送打卡结果
- [ ] 微信机器人推送打卡结果

### 3.3. 待补充其他功能

## 4. 更新日志
- 2024-10-24: v0.2.0
  - Dingtalk自动签到脚本生成器


- 2024-10-13: v0.1.0
  - 保持Teams在线

## 5. 打包方法
> 本工具包使用pyinstaller可打包成Mac、Windows、Linux可执行文件\
> 打包方法尚未完善，仅供参考
1. 安装pyinstaller
```pip install pyinstaller```
2. 打包
```pyinstaller -F main.py```
3. 运行
```dist/main.exe```
