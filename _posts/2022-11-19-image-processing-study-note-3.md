---
layout: post
category: [计算机视觉]
tag: [数字图像处理, 学习笔记]
title: 数字图像处理学习笔记3
---


**图像的空间域处理主要分为灰度变换和空间滤波。**
1. 灰度变换
{% raw %}
```math
g(x, y) = T[ f(x, y) ]
```
{% endraw %}
f(x, y)是输入图像，g(x, y)是处理后的图像，T是算子。
2. 空间滤波
空间滤波器 == 空间掩模 == 核 == 模板 == 窗口
空间滤波是对邻域进行处理。
### 1. 灰度变换（目的都是提高对比度，增强图像）
##### 1. 基本灰度变换函数
* 图像反转（ps：负片）
* 对数变换
* 幂律变换
公式：
{% raw %}
```math
s = cr^\gamma
```
{% endraw %}
c和γ都为常数。
![04bf7333d9abf11c2612ef3ac2bca926.png](/assets/images/image-processing-study-note/Image35.png)
从图可以看出，假设γ为25.0，那么输入图像里的像素灰度值小于3L/4时，输出图像的对应元素的灰度值为0，大于3L/4时，输出图像的像素值才会陡升。==> 明显的会越明显，不明显的让他变黑（对比度）。
![126724fc3e552c8042c045ca8a784a4a.png](/assets/images/image-processing-study-note/Image36.png)
处理代码：
{% raw %}
```matlab
close all; 
clear all; 
clc;    
i =imread('test.png');
i = im2double(i);
i = rgb2gray(i);
i0_04 = gammaCorrection(i, 0.04);
i0_2 = gammaCorrection(i, 0.2);
i1 = gammaCorrection(i, 1);
i2_5 = gammaCorrection(i, 2.5);
i25 = gammaCorrection(i, 25);
subplot(231), imshow(i0_04), title("Y=0.04");
subplot(232), imshow(i0_2), title("Y=0.2");
subplot(233), imshow(i1), title("Y=1");
subplot(234), imshow(i2_5), title("Y=2.5");
subplot(235), imshow(i25), title("Y=25");
function [img] = gammaCorrection(i, gamma)
img = 1 * ( i .^ gamma );
end
```
{% endraw %}
##### 2. 分段线性变换函数
* 对比度拉伸（扩展灰度值范围）
* 灰度级分层
![75c215bb645557dcb92dc7904d1caadf.png](/assets/images/image-processing-study-note/Image37.png)
* 比特平面分层
对于8位灰度图像而言，其灰度值范围是[0, 256]，但在比特视角下，对于每一个像素，其对应比特值，假设为0000 0101 ==> 
![4cb4c9d381d4fbe1ee96e4b94f6b68f0.png](/assets/images/image-processing-study-note/Image38.png)
每一像素的每一层面的比特(1和0)都可以组成一幅图像，一共8幅。
### 2. 直方图处理（一种灰度变换方法，可以全局，也可以对图像进行部分处理）
直方图是从离散视角下，图像的灰度值分布情况。
![6eba36b7ff4e606c96f72c6bd1c59bd5.png](/assets/images/image-processing-study-note/Image39.png)
如图，粗略可以看到，图像中灰度值为0.4-0.5之间的像素个数最多。
直方图处理涉及均衡化和规定化两种处理方式。
##### 1. 直方图均衡化
如果一幅图像的灰度直方图几乎覆盖了整个灰度的取值范围，并且除了个别灰度值的个数较为突出，整个灰度值分布近似于均匀分布，那么这幅图像就具有较大的灰度动态范围和较高的对比度，同时图像的细节更为丰富。已经证明，**仅仅依靠输入图像的直方图信息，就可以得到一个变换函数，利用该变换函数可以将输入图像达到上述效果，该过程就是直方图均衡化。**
![c778d1a1cf5346f34dd0f54b39bace52.png](/assets/images/image-processing-study-note/Image40.png)
如图所示，均衡化后的图像的灰度值分布较为均匀。
##### 2. 直方图规定化
就像深度学习的预处理一样，为了保证所拥有的这些图片的灰度动态范围和对比度相同，也就是要他们的灰度直方图分布要相同，往往会先提供一张标准图的图像，该图像被称为标准图，其有个标准图的直方图，然后就要把这些图片的直方图分布弄得和这个标准图的直方图一样，这就是直方图规定化。
![94fdc4b7afed7145b56540f6dff4aa00.png](/assets/images/image-processing-study-note/Image41.png)
**对一幅灰度图像进行灰度变换，使变换后的图像的直方图与另外给定的一幅图像的直方图相匹配（近似相同）。**

{% raw %}
```shell
close all;
clear all;
clc;
staPic = imread('test.png');
staPicHist = imhist(staPic);
img = imread('test.bmp');
imgToStaHist = histeq(img, staPicHist);
subplot(321), imshow(staPic), title('Standard Picture');
subplot(322), imhist(staPic), title('Standard Picture Hist');
subplot(323), imshow(img), title('Image');
subplot(324), imshow(imgToStaHist), title('Image Haved Standarded');
subplot(325), imhist(img), title('Image Hist');
subplot(326), imhist(imgToStaHist), title('Image Hist Haved Standarded');
```
{% endraw %}

![2f3ca1d9848fd55fadbbf29920558a19.png](/assets/images/image-processing-study-note/Image42.png)

### 3. 空间滤波
遍历图片每个像素，使用一个矩阵对每个像素整个邻域里的值进行处理计算，计算得到的值为该像素位置的新值，处理完整张图片后就会出来一张新图片，新图片每个像素的值都由原图对应位置的像素所在邻域的值得到，这叫做滤波。矩阵叫：滤波器，模板（mask），滤波模板，窗口，卷积滤波，卷积模板，卷积核。
分为线性滤波和非线性滤波。

##### 1. 线性空间滤波
将邻域中每个像素与滤波器相应的值相乘，然后对结果求和（线性运算），这种滤波叫线性滤波。
两种模式：相关、卷积。
![bdc38a26899335b8249df5689be428c9.png](/assets/images/image-processing-study-note/Image43.png)
{% raw %}
```matlab
g = imfilter(f, w, filtering_mode, boundary_options, size_options)
```
{% endraw %}
![a6e287aaf79287ea2967aff4d81fab0f.png](/assets/images/image-processing-study-note/Image44.png)
**Matlab滤波运算时，将数据类型转化为浮点型，但最终会将输出图像转换为与输入图像相同的数据类型，如果输入图像是int8，运算时时float，则会发生截断。如果追求高精度，需要用`im2single`, `im2double`, `tofloat`将处理原图。**
##### 2. 非线性空间滤波
非线性空间滤波：对邻域的滤波计算不是采用线性运算，譬如取邻域里最大值。
两个函数：`nlfilter`和`colfilt`。
`colfilt`占更多的内存，但速度快，一般用这个。
{% raw %}
```matlab
g = colfilt(f, [2 3], 'sliding', @fun);
```
{% endraw %}
`f`是输入图像。`[2 3]`是自定义邻域大小。`'sliding'`表示对于输入图像f，是逐像素进行滑动处理的，另一个可选的是`'distinct'`。`@fun`是函数句柄，不是函数名。
**`colfilt`输入到函数`fun`里的参数`A`是个矩阵，行数为邻域里的元素个数，列数为图像的像素个数，也就是将图像的每个邻域存储在`A`的每一列中。**
{% raw %}
```matlab
% fun.m
function gmean = fun(A)
    gmean = prod(A, 1).^(1/size(A, 1));
end
或者 匿名函数
gmean = @(A) prod(A, 1).^(1/size(A, 1));
```
{% endraw %}
`prod(A, 1)`表示将`A`的各列视为向量，并返回一个包含每列乘积的行向量。 `size(A, 1)`表示矩阵`A`第1维的值，也就是行数，`size(A, 2)`是列数。
![2d0cd104bb8e0f3a778d21ab8f8cdd57.png](/assets/images/image-processing-study-note/Image45.png)
##### 3. 滤波器
![05629572998696e699fa22974c82231a.png](/assets/images/image-processing-study-note/Image46.png)
##### 4. 模糊集
![810f920552c42446a1aabbc9a039ff46.png](/assets/images/image-processing-study-note/Image47.png)
{% raw %}
```matlab
function mu = triangmf(z, a, b, c)
    % 三角隶属函数，z是任意长度的向量
    mu = zeros(size(z));
    lowSide = (a <= z) & (z < b);
    highSide = (b <= z) & (z < c);
    mu(lowSide) = (z(lowSide) - a) ./ (b - a);
    mu(highSide) = 1 - (z(highSide) - b) ./ (c - b);
end
% 说明：
z = [1, 2, 32, 4, 5];
a = 3; b = 10;
lowSide = (a <= z) & (z < b); 
mu(lowSide) = (z(lowSide) - a) ./ (b - a);
% lowSide: [ 0 0 0 1 1 ], 值为1表明向量z在这个位置的值 a<=z<b
% z(lowSide): [ x x x 4 5 ], x 表示不处理
% mu(lowSide) ==> mu是个5个元素的向量
```
{% endraw %}
![0b3d06b660cedde886bedadaf415a4e2.png](/assets/images/image-processing-study-note/Image48.png)
**模糊评价系统:**
![f23c170a8ed15949c484b963465600f6.png](/assets/images/image-processing-study-note/Image49.png)
**[模糊工具箱的使用](https://wenku.baidu.com/view/8ce8ad5d3b3567ec102d8aa6.html)：**
![02c88bf8a49a32e413a53f1d5173b32d.png](/assets/images/image-processing-study-note/Image50.png)




