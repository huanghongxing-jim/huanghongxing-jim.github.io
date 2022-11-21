---
layout: post
category: [esp32]
tag: [esp32cam, 安信可, 无线图传, Arduino]
title: esp32cam学习笔记
---


# 一、硬件介绍

淘宝买的，底板跟了个ch340芯片，接上microusb，就能将Arduino IDE烧录到里面。

![](/assets/images/esp32cam-first-attempt/2022-07-31-15-53-33.png)

# 二、开发流程

## 1. 准备

### 1.1 Arduino IDE的`附加开发板管理网址`：
{% raw %}
```shell
https://www.arduino.cn/package_esp32_index.json
https://dl.espressif.com/dl/package_esp32_index.json
https://arduino.esp8266.com/stable/package_esp8266com_index.json
https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json
```
{% endraw %}

### 1.2 安装：工具 -> 开发板管理器 -> **esp32**。


![](/assets/images/esp32cam-first-attempt/2022-07-31-16-54-14.png)

### 1.3 选择开发板：
![](/assets/images/esp32cam-first-attempt/2022-07-31-16-42-46.png)

## 2. 程序

![](/assets/images/esp32cam-first-attempt/2022-07-31-16-43-56.png)

**改动：**

![](/assets/images/esp32cam-first-attempt/2022-07-31-16-45-50.png)

## 3. 烧录和运行

**串口会打印摄像头的ip地址。**

![](/assets/images/esp32cam-first-attempt/2022-07-31-16-46-31.png)

## 4. 界面

![](/assets/images/esp32cam-first-attempt/2022-07-31-16-46-47.png)

## 5. 程序调用

{% raw %}
```python
import cv2 as cv
from Config import Config
import requests
class Config:
    def __init__(self, ip_addr="192.168.3.26"):
        self.cam_ip_addr = "http://" + ip_addr
    def get_stream_addr(self):
        return self.cam_ip_addr + ":81/stream"
    def set(self, var: str, val: int):
        content = self.cam_ip_addr + f"/control?var={var}&val={val}"
        r = requests.get(content)
        if not 200 == r.status_code:
            print(f"设置{var}为{val}失败。")
c = Config("192.168.3.26")
c.set("framesize", 10)
c.set("brightness", 2)
c.set("contrast", 0)
c.set("quality", 10)
#c.set("face detect", 0)
capture = cv.VideoCapture(c.get_stream_addr())
while(True):
    ret, frame = capture.read()
    if ret:
        cv.imshow('frame', frame)
    if cv.waitKey(1) == ord('q'):
        break
```
{% endraw %}


