---
layout: post
category: [Linux驱动学习笔记]
tag: [Linux驱动, 设备树, 嵌入式, Device Tree]
title: 嵌入式Linux设备树完全指南
---

# 一、设备树概述

设备树（Device Tree）是一种描述硬件信息的数据结构，用于将硬件信息从内核代码中分离出来。在 Linux 3.x 版本之后，ARM 架构的内核强制使用设备树来描述硬件。

## 1. 为什么需要设备树？

在设备树出现之前，硬件信息都硬编码在内核源码的 `.c` 文件中：

- 每个 ARM 开发板都需要修改内核代码
- 代码冗余严重，维护困难
- 编译时间长，灵活性差

**设备树的优势：**

- 硬件描述与驱动代码分离
- 一个内核镜像可以支持多个硬件平台
- 修改硬件配置不需要重新编译内核
- 便于硬件抽象和代码复用

## 2. 设备树的组成

设备树包含两个部分：

1. **DTS（Device Tree Source）**：设备树源文件，文本格式，人类可读
2. **DTB（Device Tree Blob）**：编译后的二进制文件，内核可读

# 二、DTS 语法基础

## 1. 基本结构

```dts
/dts-v1/;                    // DTS 版本声明

/ {                          // 根节点
    model = "My Board";      // 开发板名称
    compatible = "vendor,myboard";  // 兼容性字符串
    
    cpus {                   // 子节点
        #address-cells = <1>;
        #size-cells = <0>;
        
        cpu0: cpu@0 {        // 带标签的节点
            device_type = "cpu";
            compatible = "arm,cortex-a7";
            reg = <0>;
        };
    };
};
```

## 2. 节点命名规则

```dts
node-name@unit-address {
    // 属性
}
```

- `node-name`：节点名称，最多 31 个字符
- `@unit-address`：单元地址，可选，通常与 `reg` 属性第一个地址值相同
- 示例：`serial@101f0000`、`gpio@50000000`

## 3. 常用属性

### compatible 属性（兼容性）

```dts
compatible = "vendor,device";
compatible = "vendor,device", "generic-device";  // 多个兼容字符串
```

驱动程序通过 `compatible` 属性匹配设备。

### reg 属性（寄存器）

```dts
// #address-cells = <1> 表示地址用1个cell表示
// #size-cells = <1> 表示大小用1个cell表示

serial@101f0000 {
    compatible = "arm,pl011";
    reg = <0x101f0000 0x1000>;  // 地址 0x101f0000，大小 0x1000
};
```

### ranges 属性（地址映射）

```dts
soc {
    #address-cells = <1>;
    #size-cells = <1>;
    ranges = <0x0 0xe0000000 0x00100000>;  // 子地址 0 -> 父地址 0xe0000000，大小 0x100000
    
    serial@0 {
        reg = <0x0 0x1000>;  // 实际地址 = 0xe0000000 + 0x0 = 0xe0000000
    };
};
```

### status 属性（设备状态）

```dts
status = "okay";     // 启用设备（默认值）
status = "disabled"; // 禁用设备
status = "fail";     // 设备不可操作
```

### interrupt 相关属性

```dts
gpio: gpio@50000000 {
    compatible = "vendor,gpio";
    reg = <0x50000000 0x1000>;
    interrupts = <0 25 4>;  // 中断号
    interrupt-parent = <&gic>;  // 中断控制器
};
```

## 4. 标签和引用

```dts
gpio1: gpio@50000000 {  // gpio1 是标签
    compatible = "vendor,gpio";
    reg = <0x50000000 0x1000>;
};

&gpio1 {  // 通过标签引用并扩展节点
    status = "okay";
};

led {
    gpios = <&gpio1 5 0>;  // 引用 gpio1 标签
};
```

# 三、设备树编译和使用

## 1. 编译命令

```bash
# 将 DTS 编译为 DTB
dtc -I dts -O dtb -o myboard.dtb myboard.dts

# 反编译 DTB 到 DTS
dtc -I dtb -O dts -o myboard.dts myboard.dtb
```

## 2. 内核编译时包含设备树

在内核源码目录下：

```bash
make dtbs           # 编译所有设备树
make myboard.dtb    # 编译指定设备树
```

## 3. 启动时加载设备树

**U-Boot 方式：**

```bash
# 加载 DTB 到内存
tftp 0x80000000 myboard.dtb

# 加载内核
tftp 0x80800000 zImage

# 启动
bootz 0x80800000 - 0x80000000
```

# 四、实际示例：定义一个 LED 设备

## 1. GPIO LED 设备树节点

```dts
/ {
    leds {
        compatible = "gpio-leds";
        
        led1 {
            label = "heartbeat";
            gpios = <&gpio1 3 0>;  // GPIO1_IO03，默认低电平
            linux,default-trigger = "heartbeat";
            default-state = "off";
        };
        
        led2 {
            label = "user";
            gpios = <&gpio1 5 0>;
            default-state = "on";
        };
    };
};
```

## 2. 对应的驱动程序（简化版）

```c
#include <linux/module.h>
#include <linux/platform_device.h>
#include <linux/gpio.h>
#include <linux/of_gpio.h>

struct led_data {
    int gpio;
    const char *label;
};

static int led_probe(struct platform_device *pdev)
{
    struct device_node *np = pdev->dev.of_node;
    struct device_node *child;
    struct led_data *led;
    int gpio, ret;
    
    // 遍历所有子节点
    for_each_child_of_node(np, child) {
        // 从设备树获取 GPIO 信息
        gpio = of_get_named_gpio(child, "gpios", 0);
        if (!gpio_is_valid(gpio)) {
            dev_err(&pdev->dev, "Invalid GPIO\n");
            continue;
        }
        
        // 获取标签
        of_property_read_string(child, "label", &led->label);
        
        // 申请并设置 GPIO
        ret = devm_gpio_request_one(&pdev->dev, gpio,
                                    GPIOF_OUT_INIT_LOW, led->label);
        if (ret) {
            dev_err(&pdev->dev, "Failed to request GPIO\n");
            continue;
        }
        
        dev_info(&pdev->dev, "LED %s registered on GPIO %d\n", 
                 led->label, gpio);
    }
    
    return 0;
}

static const struct of_device_id led_of_match[] = {
    { .compatible = "gpio-leds", },
    { },
};
MODULE_DEVICE_TABLE(of, led_of_match);

static struct platform_driver led_driver = {
    .probe = led_probe,
    .driver = {
        .name = "gpio-leds",
        .of_match_table = led_of_match,
    },
};
module_platform_driver(led_driver);

MODULE_LICENSE("GPL");
```

# 五、常用 API 函数

## 1. 获取设备节点

```c
// 通过 compatible 属性查找节点
struct device_node *np = of_find_compatible_node(NULL, NULL, "gpio-leds");

// 通过路径查找节点
struct device_node *np = of_find_node_by_path("/leds/led1");

// 通过别名查找节点
struct device_node *np = of_find_node_by_alias("led1");

// 获取子节点
struct device_node *child;
for_each_child_of_node(np, child) {
    // 处理子节点
}
```

## 2. 读取属性值

```c
// 读取 u32 值
u32 val;
of_property_read_u32(np, "reg", &val);

// 读取字符串
const char *str;
of_property_read_string(np, "label", &str);

// 读取数组
u32 regs[2];
of_property_read_u32_array(np, "reg", regs, 2);

// 读取 GPIO
int gpio = of_get_named_gpio(np, "gpios", 0);

// 读取中断号
int irq = irq_of_parse_and_map(np, 0);
```

## 3. 读取状态属性

```c
// 检查设备是否启用
if (of_device_is_available(np)) {
    // 设备状态是 "okay"
}

// 检查 compatible 属性
if (of_device_is_compatible(np, "gpio-leds")) {
    // 设备匹配
}
```

# 六、设备树 overlay（动态设备树）

在运行时动态添加/修改设备树，常用于可热插拔设备。

## 1. 创建 Overlay DTS

```dts
/dts-v1/;
/plugin/;

/ {
    fragment@0 {
        target = <&i2c1>;
        
        __overlay__ {
            #address-cells = <1>;
            #size-cells = <0>;
            
            temp_sensor: lm75@48 {
                compatible = "national,lm75";
                reg = <0x48>;
                status = "okay";
            };
        };
    };
};
```

## 2. 加载 Overlay

```bash
# 编译
dtc -@ -I dts -O dtb -o overlay.dtbo overlay.dts

# 加载到系统
mkdir -p /sys/kernel/config/device-tree/overlays/my_overlay
cat overlay.dtbo > /sys/kernel/config/device-tree/overlays/my_overlay/dtbo
```

# 七、调试技巧

## 1. 在 Linux 中查看设备树

```bash
# 查看设备树信息
ls /sys/firmware/devicetree/

# 读取属性（需要转换）
hexdump -C /sys/firmware/devicetree/base/model

# 更友好的方式
dtc -I fs /sys/firmware/devicetree -O dts -p
```

## 2. 内核日志调试

在驱动中添加调试信息：

```c
dev_info(&pdev->dev, "Device %s probed\n", np->name);
dev_info(&pdev->dev, "GPIO = %d\n", gpio);
```

查看日志：

```bash
dmesg | grep "device-tree"
dmesg | grep "your-driver-name"
```

## 3. 常见问题

**问题1：设备树修改不生效**

- 检查是否重新编译了 DTB
- 确认 U-Boot 加载了新的 DTB
- 查看 `/sys/firmware/devicetree` 确认

**问题2：驱动未匹配设备**

- 检查 `compatible` 字符串是否一致
- 使用 `ls /sys/bus/platform/devices/` 查看设备
- 检查 `status` 属性是否为 `"okay"`

**问题3：GPIO 申请失败**

- 检查 GPIO 是否已被其他驱动占用
- 使用 `cat /sys/kernel/debug/gpio` 查看 GPIO 状态
- 检查 pinmux 配置是否正确

# 八、总结

设备树是嵌入式 Linux 开发中不可或缺的一部分，它实现了硬件描述和驱动代码的分离，提高了代码的可维护性和可移植性。掌握设备树的编写和使用，是嵌入式 Linux 开发者的基本技能。

**关键要点：**

1. 设备树将硬件信息从内核代码中分离
2. DTS 是源文件，DTB 是编译后的二进制
3. `compatible` 属性用于驱动匹配
4. 使用 `of_` 前缀的 API 函数读取设备树信息
5. 可以在 `/sys/firmware/devicetree` 中查看当前设备树

**学习建议：**

- 从现有开发板的设备树文件入手学习
- 对照硬件原理图理解设备树节点
- 多使用内核提供的调试接口
- 参考内核源码 `Documentation/devicetree/` 目录

---

**参考资料：**

- Linux 内核源码 `Documentation/devicetree/`
- `scripts/dtc/dtc-grammar.txt`
- 《Linux设备驱动开发详解》
