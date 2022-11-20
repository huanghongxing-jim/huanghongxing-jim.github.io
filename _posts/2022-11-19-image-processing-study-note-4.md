---
layout: post
category: [计算机视觉]
tag: [数字图像处理, 学习笔记]
title: 数字图像处理学习笔记4
---
{% raw %}

形态学基本操作：腐蚀、膨胀，进阶：开运算、闭运算。
基础理论：集合论。
### 一、集合论
**集合论基本概念：**
![4b4e3c7b85f87f1f2ed4729751dd848b.png](/assets/images/image-processing-study-note/Image51.png)
![d90e611d68cbed25f82851dac9848798.png](/assets/images/image-processing-study-note/Image52.png)
### 二、腐蚀/膨胀
##### 1. 膨胀
![f2bbfc1730f82fa11d2c712ebd3958f3.png](/assets/images/image-processing-study-note/Image53.png)
用处：桥接裂缝和填充孔洞。
##### 2. 腐蚀
![f3093e5407cf40c1274594395aafecd7.png](/assets/images/image-processing-study-note/Image54.png)
结构元素B是对称的，则图像X被B腐蚀和图像X被B的对称集合腐蚀，结果都一样；否则不一样。
##### 3. 膨胀/腐蚀
河岸的补集为河面，河岸的腐蚀等价于河面的膨胀 ==> 膨胀和腐蚀具有对偶性 ==> 膨胀和腐蚀能相互转换 ==> 一套硬件就可以实现腐蚀、膨胀运算。
结构元素的形状可以各式各样。
### 三、开运算/闭运算
1. 开操作：对象的轮廓变得光滑，断开狭窄的间断和消除细小的突出物。
![c046358687c07d2af6df4339fc2c2530.png](/assets/images/image-processing-study-note/Image55.png)
2. 闭操作：轮廓更为光滑，消弥狭窄的间断和细长的鸿沟，消除小的孔洞，并填补轮廓线中的断裂。
![770ecf8a39a05c18881d13297d425ca4.png](/assets/images/image-processing-study-note/Image56.png)
![5f8ae5d5e00d4a706cf12a4fccd0a39a.png](/assets/images/image-processing-study-note/Image57.png)
### 四、二值数学形态学基本算法
##### 1. 形态滤波 ==> 筛选特定形状的子图像
![0241298afad9bcf330d13ce5c7ba1d58.png](/assets/images/image-processing-study-note/Image58.png)
##### 2. 边界提取
![d9a27b11799284758c7d5932643d52ba.png](/assets/images/image-processing-study-note/Image59.png)
##### 3. [区域填充](https://www.cnblogs.com/pingwen/p/12245857.html)
![637a07ead23edd2a224d2603494aa065.png](/assets/images/image-processing-study-note/Image60.png)
```matlab
img = rgb2gray(imread('temp.jpg'));
BInnerEle = zeros(size(img));
BInnerEle(250, 300) = 1; % 内部填充，在点（250,300）开始膨胀
BOuterEle = zeros(size(img));
BOuterEle(40, 40) = 1; % 外部填充，在点（40,40）开始膨胀
se = [0 1 0;1 1 1;0 1 0];
B1 = imdilate(BInnerEle, se) & img;
B2 = imdilate(B1, se) & img;
B3 = imdilate(BOuterEle, se) & img;
B4 = imdilate(B3, se) & img;
fInner = figure('NumberTitle','off','toolbar','none','menubar','none','name','内部填充','position',[100 100 100 100]);
fOuter = figure('NumberTitle','off','toolbar','none','menubar','none','name','外部填充','position',[200 200 200 200]);
while 1
    figure(fInner), imshow(B2);
    figure(fOuter), imshow(B4);
    if (B1 == B2)
        break;
    else
        B1 = B2;
        B2 = imdilate(B1, se) & img;
        B3 = B4;
        B4 = imdilate(B3, se) & img;
    end
end
```
左边gif是内部填充，右边gif是外部填充：
![b5d51d0d47c2e8eda7f7d618d4ff6ee0.gif](/assets/images/image-processing-study-note/video.gif)
##### 4. 击中和击不中变换 ==> 图像匹配
![0351e32bfc00530bb63b26e9ec7655a1.png](/assets/images/image-processing-study-note/Image61.png)
**高级形态学函数（基础还是腐蚀/膨胀）：
`Boarder边界`、`Hole filling孔洞填充`、`Labeling标记`、`Lowpass filter低通滤波器`、`Hightpass filter高通滤波器`、`Separation分割`、`Skeleton骨架化`、`Segmentation分离`、`Distance距离变换`、`Danlelsson朴素贝叶斯`、`Circle圆拟合`、`Convex Hull凸包算法`。**


{% endraw %}  