---
layout: post
category: [计算机视觉]
tag: [数字图像处理, 学习笔记]
title: 数字图像处理学习笔记2
---
{% raw %}

### 1. 视觉
眼球结构:
![914783cc378ff470b926b479cf4ae051.png](/assets/images/image-processing-study-note/Image14.png)
感受到的亮度 ==> 图像中的灰度
### 2. 数字图像
1. 空间域：图像坐标的取值。
2. ![3d89666da5a5f1aa36a0c6fb1fcd8043.png](/assets/images/image-processing-study-note/Image15.png)
将原点设置在图像左上角的原因：图像显示（电视显示器）扫描都是从左上角开始的，对应与阵列的左上角（第一个元素）。
3. 图像内插（放大、收缩、旋转、几何校正）：
最近邻内插法、双线性内插法、双三次内插法。
### 3. 像素间的关系（领域-邻接-连通）
1. 领域
![92469e5ec8a54057a3c46b205fa632e0.png](/assets/images/image-processing-study-note/Image16.png)
![d8cfc5ff4b87d7d87d502222b2d05925.png](/assets/images/image-processing-study-note/Image17.png)
2. 邻接
![4891085e0f79afc8ffbd6ee600ff10fe.png](/assets/images/image-processing-study-note/Image18.png)
3. 连通
![449d4063f1e8842260bed2df8047f15d.png](/assets/images/image-processing-study-note/Image19.png)
### 4. 距离度量
1. 欧式距离
![e5a5facda87a776d5c0016777f1092f7.png](/assets/images/image-processing-study-note/Image20.png)
2. 城市距离
![262ec6a4fcc068e59e55f6f8f55afa0e.png](/assets/images/image-processing-study-note/Image21.png)
a与b距离是1，a与c距离是2。
### 5. 数学工具
1. 数字图像处理是阵列操作，不是矩阵操作。
阵列操作：
![f64045725b94802a7b15e5fb1a4d7fed.png](/assets/images/image-processing-study-note/Image22.png)
2. 线性操作（H是一个函数，一个算法，一种处理手法）
![3aef63bc7fe90cddeab14dfc4d710582.png](/assets/images/image-processing-study-note/Image23.png)
3. 算术操作（阵列操作）
![44f5d9f97654235004188d9e3b0aa822.png](/assets/images/image-processing-study-note/Image24.png)
1）使用相机拍摄同一张图像，将所拍的这些图像灰度化并相加，再每个像素点取平均，能消除图像噪声。
![ae7cc3a1a5ce9db85f5172579b023759.png](/assets/images/image-processing-study-note/Image25.png)
2）图像相减 ==> 增强
3）图像相乘 ==> ROI
![d5832358f2e81a1e280518107283e49d.png](/assets/images/image-processing-study-note/Image26.png)
4）图像相除
4. 空间操作
1）单像素操作
![88f7c4dc167fa9430622dc2be7f08f7e.png](/assets/images/image-processing-study-note/Image27.png)
T()是处理方法。
2）邻域操作
将一副图像分成很多个邻域，每个邻域经过函数T()变成一个灰度值。
![a2da5aaf5e90aae4af0f0c59b0ee4360.png](/assets/images/image-processing-study-note/Image28.png)
3）几何空间变换
空间坐标变换 ==> 仿射变换：
![3d7bb81765d15d129c3d3ca59e54bef3.png](/assets/images/image-processing-study-note/Image29.png)
![bdb40394994b064023c2ee732707d5af.png](/assets/images/image-processing-study-note/Image30.png)
仿射变换需要和图像内插相结合。
4) 图像配准（目的是找到畸变函数，然后将畸变图像变回来）
![707497780f85a3dda29125531a2071a6.png](/assets/images/image-processing-study-note/Image31.png)
5. 图像变换 ==> 将空间域的图像转化到变化域上进行处理，再返回到空间域
公式：
![9d8e1d60a42fca9bab73769fe7178fd4.png](/assets/images/image-processing-study-note/Image32.png)
流程：
![f5d37b2b3c81891a5d1aefd597561060.png](/assets/images/image-processing-study-note/Image33.png)
![4a70b5cbc31dac2cd133d4856ca9f9b1.png](/assets/images/image-processing-study-note/Image34.png)
6. 概率方法 ==> 假设图像的噪声是随机分布的，那就要找到那个分布函数

{% endraw %}  