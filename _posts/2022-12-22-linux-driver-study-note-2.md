---
layout: post
category: [Linux驱动学习笔记]
tag: [Linux驱动, 学习笔记, 嵌入式]
title: Linux驱动学习笔记2
---

# 一、Firefly Linux SDK开发

**官方提供Linux开发的整套SDK。**

## 1. 使用repo工具更新SDK

> repo是Google开发的用于管理Android版本库的一个工具，使用Python对git进行了一定的封装。

```shell
.repo/repo/repo sync -l
.repo/repo/repo sync -c --no-tags
.repo/repo/repo start firefly --all
```

## 2. SDK目录

![](/assets/images/linux-driver-study-note/2022-08-28-23-27-13.png)
 
## 3. 配置

```shell
./build.sh aio-3399-jd4-ubuntu.mk
```

`aio-3399-jd4-ubuntu.mk`为编译生成`Buildroot`固件的配置文件(**使用`export`指向外部配置文件**):

```shell
export RK_UBOOT_DEFCONFIG=firefly-rk3399 # 编译uboot配置文件
export LINUX_KERNEL_DEFCONFI=firefly_linux_defconfig # 编译kernel配置文件
export RK_KERNEL_DTS=rk3399-firefly-aiojd4 # 编译kernel用到的dts（设备树）
export RK_PARAMETER=parameter-ubuntu.txt # 分区信息，GPT表
```

## 4. 编译各个组件为`Buildroot`固件的组件

> 通常一个嵌入式设备上运行的软件包括`bootloader`，`linux`内核和`rootfs`，各个部分可以独立去开发，在使用的时候分别去交叉编译，烧写这些软件组件。`buildroot`工具提供了一种更加高效的管理方法，它把`bootloader`，`linux`内核和`rootfs`集成在一起，可以非常方便的去定制、管理、编译和组装一个自己需要的软件系统，仅需通过配置(`menuconfig`、`gconfig`和`xconfig`)即可。

## 5. 固件打包

将`uboot.img`(引导程序**镜像**)、`boot.img`(内核+设备树**镜像**)、`rootfs.img`(根文件系统**镜像**)、`parameter.txt`(配置信息)打包到固件里。

```shell
./build.sh updateimg
```

## 6. **难点：配置分区表parameter-ubuntu.txt**

```txt
FIRMWARE_VER: 8.1
MACHINE_MODEL: RK3399
MACHINE_ID: 007
MANUFACTURER: RK3399
MAGIC: 0x5041524B
ATAG: 0x00200800
MACHINE: 3399
CHECK_MASK: 0x80
PWR_HLD: 0,0,A,0,1
TYPE: GPT
CMDLINE: mtdparts=rk29xxnand:0x00002000@0x00004000(uboot),0x00002000@0x00006000(trust),0x00002000@0x00008000(misc),0x00010000@0x0000a000(boot),0x00010000@0x0001a000(recovery),0x00010000@0x0002a000(backup),0x00020000@0x0003a000(oem),0x00700000@0x0005a000(rootfs),-@0x0075a000(userdata:grow)
uuid:rootfs=614e0000-0000-4b53-8000-1d28000054a9
```

* `0x00002000@0x00004000(uboot)`指定`uboot`程序的分区大小`0x00002000`和分区起始地址`0x00004000`。
* `boot`分区包含内核和设备树信息。

> `U-Boot`是一个主要用于嵌入式系统的 **`BootLoader`引导加载程序**，支持包括`ARM`和`x86`的计算机系统结构，自由软件协议是GNU。**主要用于开机时将内核加载到内存中，启动操作系统。**  

# 二、`GPIO`驱动开发

## 1. 设备树DTS概念

> * 设备树(dt, device tree)：在系统引导启动阶段进行设备初始化的时候，将设备树中描述的硬件信息传递给操作系统。
> * dts(device tree source)：设备树源文件，描述设备信息的。
> * dtc(device tree compiler)：设备树编译/反编译/调试工具。
> * dtb(device tree binary)：二进制设备树**镜像**。
> * dtsi(device tree source include):类似设备树文件的头文件，可被dts文件通过include引用，dtsi文件一般是描述硬件共性部分。

* 设备驱动源码 = 驱动代码(操作方法) + 设备代码(描述硬件资源和数据)。
* 驱动代码和设备代码匹配时，驱动代码的**probe函数会被调用去解析设备代码**。
* 硬件资源信息写在dts文件中，不必在修改内核源码。
* 内核要增加解析dts文件格式的代码。

设备树运作框架：

![](/assets/images/linux-driver-study-note/2022-08-29-16-21-03.png)

## 2. GPIO驱动

**配置`GPIO`硬件和解析：**

![](/assets/images/linux-driver-study-note/2022-08-29-20-50-58.png)

`probe()`用于解析硬件设备，自己还得编写`GPIO`的`file_operations`结构体、`open()`、`read()`和`write()`，然后在入口函数中将结构体注册到内核。