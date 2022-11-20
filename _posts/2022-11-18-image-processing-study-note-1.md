---
layout: post
category: [计算机视觉]
tag: [数字图像处理, 学习笔记]
title: 数字图像处理学习笔记1
---
{% raw %}

### 1. 概述
1. 什么是 **数字图像处理**:
* 输入输出是图像
* 图像特征
* 目标识别
2. 数字图像 起源：
报纸业（20世纪20年代） ==> 为了节约成本，编码图像进行传输
3. 应用实例
> **划分方法：**
> 1. 产生图像的方式有很多种，可见光照射到感光胶片上，或者液晶屏通过数字信号成像，再或者，人眼看到的任何景象，都算是图像成像，数字图像中的**数字**的含义是离散值，故而人眼成像不在讨论范围。
> 2. 光也是波长的一部分，所以成像的能源是**波**，按照波划分数字图像处理的应用领域：

| 波 | 应用领域 |
| --- | --- |
| 伽玛射线 | 医学、天文学 |
| X射线 | 医学 |
| 紫外波 | 荧光，ps：纸钞验伪 |
| 可见光 | 感光胶片 |
| 红外 | 能量 |
| 微波 | 遥感 |
| 无线电 | 核磁共振 |
| 声波 | 声呐，超声波成像 |
4. 数字图像处理步骤：
![9471ad82a2c1b678ed294bfd0bd8832b.png](/assets/images/image-processing-study-note/Image1.png)
![97e334b297cf90bd8478bed3aa2dfbc2.png](/assets/images/image-processing-study-note/Image2.png)
5. 通用图像处理系统
![d6d92c507225eba9e559300ee210787f.png](/assets/images/image-processing-study-note/Image3.png)
6. 图像处理大部分环境的噪声有很多，不是给你一张清晰无比的图像让你去做。
7. 成像步骤：
![19ab0ea2114c60905899ce6429620836.png](/assets/images/image-processing-study-note/Image4.png)
8. 图像可以用**红 绿 蓝**三原色表示。
9. 图形（线 圆 矩形） ==> 指令形成
图像 ==> 矩阵
10. 数字图像处理实际上是 二维矩阵的处理 ==> 存储的数据
11. 分辨率 ==> 图像空间分辨率（越小，颗粒越大） 灰度级分辨率（深度，越大，颜色过渡越自然）
12. 图像处理是交叉技术（计算机、传感器、信息技术等），利用计算机对图像进行**去除噪声、增强、复原、分割、提取特征等**的理论、方法和技术称为数字图像处理。
13. 图像重建：输入是数据，输出是图像。
### 2. 图像存储格式
1. 分类（颜色深度）：
黑白（1和0） 8位索引 24位真彩色
2. 8位索引图像 ==> 带有索引表，矩阵每一个值都为这个表的索引号。
![b949d90f8bd4d8682482a97bc3654ca2.png](/assets/images/image-processing-study-note/Image5.png)
1）8位灰度索引图像：索引表中G==B==R==255 ==> 索引号直接就是灰度值，值小，越黑
2）8位伪彩色索引图像：
![aefed9788fdff42df40fc1f13c4bcfdb.png](/assets/images/image-processing-study-note/Image6.png)
颜色索引表，就叫做调色板，放在系统里边。
颜色最多2^8种，过渡不自然，参考24位真彩色图像就知道"伪"的含义了。
3. 24位真彩色图像：R、B、G各占8位，也就是总共有(2^8)^3种颜色，包含颜色多，过渡自然。
4. 位图格式：
BMP GIF TIFF JPEG
### 3. BMP存储格式
文件头（BITMAPFILEHEADER，14字节）  信息头(BITMAPINFOHEADER，40字节)  颜色表(RGBQUAD)  数据区
变量名带有reserved的表示保留字。
![609233915fbb069160488106fa9a2b26.png](/assets/images/image-processing-study-note/Image7.png)
![63705c009cf5959bf7878114ae0170bb.png](/assets/images/image-processing-study-note/Image8.png)
### 4. MATLAB基础
1. 
```matlab
close all; % 关闭所有窗口
clear all; % 清空变量
clc;       % 清屏
x = imread('test.jpg'); % 字符串要用单引号''，用双引号""不认
I = rgb2gray(x);
set(0, "defaultFigurePosition", [100, 100, 1000, 500]);  % 1000列，500行
set(0, "defaultFigureColor", [1 1 1]); % set()的第二个参数不是乱写的
subplot(121), imshow(x); % 121 ==> 1行2列，我排第1列
subplot(122), imshow(I);
```
效果：
![0016c2c004fc32fc29d50d26f3affe23.png](/assets/images/image-processing-study-note/Image9.png)
2. 
```matlab
% 显示两个窗口
figure, imshow(x1);
figure, imshow(x2); 
```
3. 二值化
```matlab
I = imread('test.jpg'); 
bw1 = im2bw(I, 0.5); % 图像二值化，阈值0.4
set(0, "defaultFigurePosition", [100, 100, 1000, 500]); 
set(0, "defaultFigureColor", [1 1 1]); 
figure; % 开一个窗口
subplot(131), imshow(I);
subplot(132), imshow(bw1);
```
4. 
![a3164b21de94b3a219723a3b380bca84.png](/assets/images/image-processing-study-note/Image10.png)
![1057bb9aebbf5db46ad3c6f46a6e52c4.png](/assets/images/image-processing-study-note/Image11.png)
5. 直方图均衡化
test.bmp是8位存储的图像，则其每个元素的灰度值取值范围是[0, 256]，但是用imhist查看其灰度值分布时会发现图像的灰度值是限制在比[0, 256]更小的范围内，这看起来会显得对比度不强，用histeq将这个范围扩大到[0, 256]，尽量保证这个大范围的每个值都有用到，也就是均衡化，能让图像对比度变强。
```matlab
i = imread('test.bmp');
imhist(i); 
i1 = histeq(i);
figure, imshow(i);
figure, imshow(i1);
```
![2999ccb855f1281a9580dbc5b7cf3359.png](/assets/images/image-processing-study-note/Image12.png)
6. 文件信息：
```matlab
ans = imfinfo('test.bmp');
```
7. 
```matlab
i =imread('test.png'); % 1. 原图
bg = imopen(i, strel('disk', 15)); % 5. 使用半径为15的圆盘消除白色物体，获取背景
fg = imsubtract(i, bg); % 2. 与原图像相减获取前景
fg_contrast = imadjust( fg, stretchlim(fg), [0 1]); % 3. 调整前景对比度
fg_contrast_bw = im2bw( fg_contrast, graythresh( fg_contrast ) ); % 4. 将前景图像转化为二值图像
```
![4a4a0d4f60daac5da1294e15becd1382.png](/assets/images/image-processing-study-note/Image13.png)


{% endraw %}  




