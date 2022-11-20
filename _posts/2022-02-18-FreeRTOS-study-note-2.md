---
layout: post
category: [FreeRTOS学习笔记]
tag: [FreeRTOS, 学习笔记]
title: FreeRTOS学习笔记2
---
## 2. 移植步骤

**基础例程概况：**

![image-20220216234957285](/assets/images/FreeRTOS-study/image-20220216234957285.png)

**1）复制FreeRTOS源文件：**![image-20220217000254173](/assets/images/FreeRTOS-study/image-20220217000254173.png)

**添加FreeRTOS的include路径：**![image-20220217000448478](/assets/images/FreeRTOS-study/image-20220217000448478.png)

**2）配置FreeRTOS：**通过`FreeRTOSConfig.h`来进行系统配置和裁剪。

板子对应的`FreeRTOSConfig.h`文件位置（复制到项目中）：![image-20220217144647789](/assets/images/FreeRTOS-study/image-20220217144647789.png)

![image-20220217145326925](/assets/images/FreeRTOS-study/image-20220217145326925.png)

**3）移植正点原子SYSTEM通用文件（sys, uart, delay）：**

FreeRTOS的系统时钟`xPortSysTickHandler()`由滴答定时器`SysTick_Handler()`提供，滴答定时器时钟频率`SysTick`可以和`AHB`相等（从而让FreeRTOS系统的时钟频率和AHB一致），可在`delay.c`的`delay_init()`修改`SysTick`频率，从而控制FreeRTOS的系统时钟频率(`SysTick->LOAD`)，而**FreeRTOS可直接使用`configTICK_RATE_HZ`在`delay_init()`修改系统时钟频率，即每`1/configTICK_RATE_HZ`系统时钟中断一次。**

FreeRTOS的`port.c`里也定义了`SysTick_Handler()`，与在`delay.c`文件自定义的`SysTick_Handler()`冲突，需要屏蔽：

![image-20220217164658063](/assets/images/FreeRTOS-study/image-20220217164658063.png)

**sys.h:**

```c
#ifndef __SYS_H
#define __SYS_H
#include "stm32f4xx.h"

// 0,不支持os
// 1,支持os
#define SYSTEM_SUPPORT_OS 1 //定义系统文件夹是否支持OS

//位带操作,实现51类似的GPIO控制功能
//具体实现思想,参考<<CM3权威指南>>第五章(87页~92页).M4同M3类似,只是寄存器地址变了.
// IO口操作宏定义
#define BITBAND(addr, bitnum)                                                  \
  ((addr & 0xF0000000) + 0x2000000 + ((addr & 0xFFFFF) << 5) + (bitnum << 2))
#define MEM_ADDR(addr) *((volatile unsigned long *)(addr))
#define BIT_ADDR(addr, bitnum) MEM_ADDR(BITBAND(addr, bitnum))
// IO口地址映射
#define GPIOA_ODR_Addr (GPIOA_BASE + 20) // 0x40020014
#define GPIOB_ODR_Addr (GPIOB_BASE + 20) // 0x40020414
#define GPIOC_ODR_Addr (GPIOC_BASE + 20) // 0x40020814
#define GPIOD_ODR_Addr (GPIOD_BASE + 20) // 0x40020C14
#define GPIOE_ODR_Addr (GPIOE_BASE + 20) // 0x40021014
#define GPIOF_ODR_Addr (GPIOF_BASE + 20) // 0x40021414
#define GPIOG_ODR_Addr (GPIOG_BASE + 20) // 0x40021814
#define GPIOH_ODR_Addr (GPIOH_BASE + 20) // 0x40021C14
#define GPIOI_ODR_Addr (GPIOI_BASE + 20) // 0x40022014

#define GPIOA_IDR_Addr (GPIOA_BASE + 16) // 0x40020010
#define GPIOB_IDR_Addr (GPIOB_BASE + 16) // 0x40020410
#define GPIOC_IDR_Addr (GPIOC_BASE + 16) // 0x40020810
#define GPIOD_IDR_Addr (GPIOD_BASE + 16) // 0x40020C10
#define GPIOE_IDR_Addr (GPIOE_BASE + 16) // 0x40021010
#define GPIOF_IDR_Addr (GPIOF_BASE + 16) // 0x40021410
#define GPIOG_IDR_Addr (GPIOG_BASE + 16) // 0x40021810
#define GPIOH_IDR_Addr (GPIOH_BASE + 16) // 0x40021C10
#define GPIOI_IDR_Addr (GPIOI_BASE + 16) // 0x40022010

// IO口操作,只对单一的IO口!
//确保n的值小于16!
#define PAout(n) BIT_ADDR(GPIOA_ODR_Addr, n) //输出
#define PAin(n) BIT_ADDR(GPIOA_IDR_Addr, n)  //输入

#define PBout(n) BIT_ADDR(GPIOB_ODR_Addr, n) //输出
#define PBin(n) BIT_ADDR(GPIOB_IDR_Addr, n)  //输入

#define PCout(n) BIT_ADDR(GPIOC_ODR_Addr, n) //输出
#define PCin(n) BIT_ADDR(GPIOC_IDR_Addr, n)  //输入

#define PDout(n) BIT_ADDR(GPIOD_ODR_Addr, n) //输出
#define PDin(n) BIT_ADDR(GPIOD_IDR_Addr, n)  //输入

#define PEout(n) BIT_ADDR(GPIOE_ODR_Addr, n) //输出
#define PEin(n) BIT_ADDR(GPIOE_IDR_Addr, n)  //输入

#define PFout(n) BIT_ADDR(GPIOF_ODR_Addr, n) //输出
#define PFin(n) BIT_ADDR(GPIOF_IDR_Addr, n)  //输入

#define PGout(n) BIT_ADDR(GPIOG_ODR_Addr, n) //输出
#define PGin(n) BIT_ADDR(GPIOG_IDR_Addr, n)  //输入

#define PHout(n) BIT_ADDR(GPIOH_ODR_Addr, n) //输出
#define PHin(n) BIT_ADDR(GPIOH_IDR_Addr, n)  //输入

#define PIout(n) BIT_ADDR(GPIOI_ODR_Addr, n) //输出
#define PIin(n) BIT_ADDR(GPIOI_IDR_Addr, n)  //输入

//以下为汇编函数
void WFI_SET(void);      //执行WFI指令
void INTX_DISABLE(void); //关闭所有中断
void INTX_ENABLE(void);  //开启所有中断
void MSR_MSP(u32 addr);  //设置堆栈地址
#endif
```

**sys.c:**

```c
#include "sys.h"

// THUMB指令不支持汇编内联
//采用如下方法实现执行汇编指令WFI
__asm void WFI_SET(void)
{
	WFI;
}
//关闭所有中断(但是不包括fault和NMI中断)
__asm void INTX_DISABLE(void)
{
	CPSID I
	BX LR
}
//开启所有中断
__asm void INTX_ENABLE(void)
{
	CPSIE I
	BX LR
}
//设置栈顶地址
// addr:栈顶地址
__asm void MSR_MSP(u32 addr)
{
	MSR MSP, r0 // set Main Stack value
	BX r14
}
```

**usart.c:**

```c
#include "usart.h"
#include "sys.h"

//如果使用ucos,则包括下面的头文件即可.
#if SYSTEM_SUPPORT_OS
#include "FreeRTOS.h" //FreeRTOS使用
#endif

//加入以下代码,支持printf函数,而不需要选择use MicroLIB
#if 1
#pragma import(__use_no_semihosting)
//标准库需要的支持函数
struct __FILE {
  int handle;
};

FILE __stdout;
//定义_sys_exit()以避免使用半主机模式
void _sys_exit(int x) { x = x; }
//重定义fputc函数
int fputc(int ch, FILE *f) {
  while ((USART1->SR & 0X40) == 0)
    ; //循环发送,直到发送完毕
  USART1->DR = (u8)ch;
  return ch;
}
#endif

#if EN_USART1_RX //如果使能了接收
//串口1中断服务程序
//注意,读取USARTx->SR能避免莫名其妙的错误
u8 USART_RX_BUF[USART_REC_LEN]; //接收缓冲,最大USART_REC_LEN个字节.
//接收状态
// bit15，	接收完成标志
// bit14，	接收到0x0d
// bit13~0，	接收到的有效字节数目
u16 USART_RX_STA = 0; //接收状态标记

//初始化IO 串口1
// bound:波特率
void uart_init(u32 bound) {
  // GPIO端口设置
  GPIO_InitTypeDef GPIO_InitStructure;
  USART_InitTypeDef USART_InitStructure;
  NVIC_InitTypeDef NVIC_InitStructure;

  RCC_AHB1PeriphClockCmd(RCC_AHB1Periph_GPIOA, ENABLE);  //使能GPIOA时钟
  RCC_APB2PeriphClockCmd(RCC_APB2Periph_USART1, ENABLE); //使能USART1时钟

  //串口1对应引脚复用映射
  GPIO_PinAFConfig(GPIOA, GPIO_PinSource9,
                   GPIO_AF_USART1); // GPIOA9复用为USART1
  GPIO_PinAFConfig(GPIOA, GPIO_PinSource10,
                   GPIO_AF_USART1); // GPIOA10复用为USART1

  // USART1端口配置
  GPIO_InitStructure.GPIO_Pin = GPIO_Pin_9 | GPIO_Pin_10; // GPIOA9与GPIOA10
  GPIO_InitStructure.GPIO_Mode = GPIO_Mode_AF;            //复用功能
  GPIO_InitStructure.GPIO_Speed = GPIO_Speed_50MHz;       //速度50MHz
  GPIO_InitStructure.GPIO_OType = GPIO_OType_PP;          //推挽复用输出
  GPIO_InitStructure.GPIO_PuPd = GPIO_PuPd_UP;            //上拉
  GPIO_Init(GPIOA, &GPIO_InitStructure);                  //初始化PA9，PA10

  // USART1 初始化设置
  USART_InitStructure.USART_BaudRate = bound; //波特率设置
  USART_InitStructure.USART_WordLength =
      USART_WordLength_8b; //字长为8位数据格式
  USART_InitStructure.USART_StopBits = USART_StopBits_1; //一个停止位
  USART_InitStructure.USART_Parity = USART_Parity_No;    //无奇偶校验位
  USART_InitStructure.USART_HardwareFlowControl =
      USART_HardwareFlowControl_None; //无硬件数据流控制
  USART_InitStructure.USART_Mode = USART_Mode_Rx | USART_Mode_Tx; //收发模式
  USART_Init(USART1, &USART_InitStructure); //初始化串口1

  USART_Cmd(USART1, ENABLE); //使能串口1

  // USART_ClearFlag(USART1, USART_FLAG_TC);

#if EN_USART1_RX
  USART_ITConfig(USART1, USART_IT_RXNE, ENABLE); //开启相关中断

  // Usart1 NVIC 配置
  NVIC_InitStructure.NVIC_IRQChannel = USART1_IRQn; //串口1中断通道
  NVIC_InitStructure.NVIC_IRQChannelPreemptionPriority = 3; //抢占优先级3
  NVIC_InitStructure.NVIC_IRQChannelSubPriority = 3;        //子优先级3
  NVIC_InitStructure.NVIC_IRQChannelCmd = ENABLE;           // IRQ通道使能
  NVIC_Init(&NVIC_InitStructure); //根据指定的参数初始化VIC寄存器、

#endif
}

void USART1_IRQHandler(void) //串口1中断服务程序
{
  u8 Res;
  if (USART_GetITStatus(USART1, USART_IT_RXNE) !=
      RESET) //接收中断(接收到的数据必须是0x0d 0x0a结尾)
  {
    Res = USART_ReceiveData(USART1); //(USART1->DR);	//读取接收到的数据

    if ((USART_RX_STA & 0x8000) == 0) //接收未完成
    {
      if (USART_RX_STA & 0x4000) //接收到了0x0d
      {
        if (Res != 0x0a)
          USART_RX_STA = 0; //接收错误,重新开始
        else
          USART_RX_STA |= 0x8000; //接收完成了
      } else                      //还没收到0X0D
      {
        if (Res == 0x0d)
          USART_RX_STA |= 0x4000;
        else {
          USART_RX_BUF[USART_RX_STA & 0X3FFF] = Res;
          USART_RX_STA++;
          if (USART_RX_STA > (USART_REC_LEN - 1))
            USART_RX_STA = 0; //接收数据错误,重新开始接收
        }
      }
    }
  }
}
#endif
```

**usart.h:**

```c
#ifndef __USART_H
#define __USART_H
#include "stdio.h"
#include "stm32f4xx_conf.h"
#include "sys.h"

#define USART_REC_LEN 200 //定义最大接收字节数 200
#define EN_USART1_RX 1    //使能（1）/禁止（0）串口1接收

extern u8 USART_RX_BUF
    [USART_REC_LEN]; //接收缓冲,最大USART_REC_LEN个字节.末字节为换行符
extern u16 USART_RX_STA; //接收状态标记
//如果想串口中断接收，请不要注释以下宏定义
void uart_init(u32 bound);
#endif
```

**delay.h:**

```c
#ifndef __DELAY_H
#define __DELAY_H
#include <sys.h>

void delay_init(u8 SYSCLK);
void delay_us(u32 nus);
void delay_ms(u32 nms);
void delay_xms(u32 nms);
#endif
```

**delay.c:**

```c
#include "delay.h"
#include "sys.h"

//如果使用OS,则包括下面的头文件即可
#if SYSTEM_SUPPORT_OS
#include "FreeRTOS.h" //FreeRTOS使用
#include "task.h"
#endif

static u8 fac_us = 0;  // us延时倍乘数
static u16 fac_ms = 0; // ms延时倍乘数,在os下,代表每个节拍的ms数

extern void xPortSysTickHandler(void);

// systick中断服务函数,使用OS时用到
void SysTick_Handler(void) {
  if (xTaskGetSchedulerState() != taskSCHEDULER_NOT_STARTED) //系统已经运行
  {
    // FreeRTOS的心跳就是由滴答定时器产生的
    xPortSysTickHandler();
  }
}

//初始化延迟函数
// SYSTICK的时钟固定为AHB时钟，基础例程里面SYSTICK时钟频率为AHB/8
//这里为了兼容FreeRTOS，所以将SYSTICK的时钟频率改为AHB的频率！
// SYSCLK:系统时钟频率
void delay_init(u8 SYSCLK) {
  u32 reload;
  SysTick_CLKSourceConfig(SysTick_CLKSource_HCLK);
  fac_us = SYSCLK; //不论是否使用OS,fac_us都需要使用
  reload = SYSCLK; //每秒钟的计数次数 单位为M
  reload *=
      1000000 /
      configTICK_RATE_HZ; //根据configTICK_RATE_HZ设定溢出时间
                          // reload为24位寄存器,最大值:16777216,在168M下,约合0.0998s左右
  fac_ms = 1000 / configTICK_RATE_HZ; //代表OS可以延时的最少单位
  SysTick->CTRL |= SysTick_CTRL_TICKINT_Msk; //开启SYSTICK中断
  SysTick->LOAD = reload;                    //每1/configTICK_RATE_HZ断一次
  SysTick->CTRL |= SysTick_CTRL_ENABLE_Msk;  //开启SYSTICK
}

//延时nus
// nus:要延时的us数.
// nus:0~204522252(最大值即2^32/fac_us@fac_us=168)
void delay_us(u32 nus) {
  u32 ticks;
  u32 told, tnow, tcnt = 0;
  u32 reload = SysTick->LOAD; // LOAD的值
  ticks = nus * fac_us;       //需要的节拍数
  told = SysTick->VAL;        //刚进入时的计数器值
  while (1) {
    tnow = SysTick->VAL;
    if (tnow != told) {
      if (tnow < told)
        tcnt += told - tnow; //这里注意一下SYSTICK是一个递减的计数器就可以了.
      else
        tcnt += reload - tnow + told;
      told = tnow;
      if (tcnt >= ticks)
        break; //时间超过/等于要延迟的时间,则退出.
    }
  };
}
//延时nms
// nms:要延时的ms数
// nms:0~65535
void delay_ms(u32 nms) {
  if (xTaskGetSchedulerState() != taskSCHEDULER_NOT_STARTED) //系统已经运行
  {
    if (nms >= fac_ms) //延时的时间大于OS的最少时间周期
    {
      vTaskDelay(nms / fac_ms); // FreeRTOS延时
    }
    nms %= fac_ms; // OS已经无法提供这么小的延时了,采用普通方式延时
  }
  delay_us((u32)(nms * 1000)); //普通方式延时
}

//延时nms,不会引起任务调度
// nms:要延时的ms数
void delay_xms(u32 nms) {
  u32 i;
  for (i = 0; i < nms; i++)
    delay_us(1000);
}
```

**4）FreeRTOS简单实验（点灯和串口打印）：**

**led.c(记得Keil工程也要添加led.c):**

```c
#include "led.h"

//初始化PF9和PF10为输出口.并使能这两个口的时钟
// LED IO初始化
void LED_Init(void) {
  GPIO_InitTypeDef GPIO_InitStructure;

  RCC_AHB1PeriphClockCmd(RCC_AHB1Periph_GPIOF, ENABLE); //使能GPIOF时钟

  // GPIOF9,F10初始化设置
  GPIO_InitStructure.GPIO_Pin = GPIO_Pin_9 | GPIO_Pin_10; // LED0和LED1对应IO口
  GPIO_InitStructure.GPIO_Mode = GPIO_Mode_OUT;           //普通输出模式
  GPIO_InitStructure.GPIO_OType = GPIO_OType_PP;          //推挽输出
  GPIO_InitStructure.GPIO_Speed = GPIO_Speed_100MHz;      // 100MHz
  GPIO_InitStructure.GPIO_PuPd = GPIO_PuPd_UP;            //上拉
  GPIO_Init(GPIOF, &GPIO_InitStructure);                  //初始化GPIO
  GPIO_SetBits(GPIOF, GPIO_Pin_9 | GPIO_Pin_10); // GPIOF9,F10设置高，灯灭
}
```

**led.h:**

```c
#ifndef __LED_H
#define __LED_H
#include "sys.h"

// LED端口定义
#define LED0 PFout(9)  // DS0
#define LED1 PFout(10) // DS1

void LED_Init(void); //初始化
#endif
```

**main.c:**

```c
#include "FreeRTOS.h"
#include "delay.h"
#include "led.h"
#include "sys.h"
#include "task.h"
#include "usart.h"

//任务优先级
#define START_TASK_PRIO 1
//任务堆栈大小
#define START_STK_SIZE 128
//任务句柄
TaskHandle_t StartTask_Handler;
//任务函数
void start_task(void *pvParameters);

//任务优先级
#define LED0_TASK_PRIO 2
//任务堆栈大小
#define LED0_STK_SIZE 50
//任务句柄
TaskHandle_t LED0Task_Handler;
//任务函数
void led0_task(void *pvParameters);

//任务优先级
#define LED1_TASK_PRIO 3
//任务堆栈大小
#define LED1_STK_SIZE 50
//任务句柄
TaskHandle_t LED1Task_Handler;
//任务函数
void led1_task(void *pvParameters);

//任务优先级
#define FLOAT_TASK_PRIO 4
//任务堆栈大小
#define FLOAT_STK_SIZE 128
//任务句柄
TaskHandle_t FLOATTask_Handler;
//任务函数
void float_task(void *pvParameters);

int main(void) {
  NVIC_PriorityGroupConfig(NVIC_PriorityGroup_4); //设置系统中断优先级分组4
  delay_init(168);                                //初始化延时函数
  uart_init(115200);                              //初始化串口
  LED_Init();                                     //初始化LED端口

  //创建开始任务
  xTaskCreate((TaskFunction_t)start_task,   //任务函数
              (const char *)"start_task",   //任务名称
              (uint16_t)START_STK_SIZE,     //任务堆栈大小
              (void *)NULL,                 //传递给任务函数的参数
              (UBaseType_t)START_TASK_PRIO, //任务优先级
              (TaskHandle_t *)&StartTask_Handler); //任务句柄
  vTaskStartScheduler();                           //开启任务调度
}

//开始任务任务函数
void start_task(void *pvParameters) {
  taskENTER_CRITICAL(); //进入临界区
  //创建LED0任务
  xTaskCreate((TaskFunction_t)led0_task, (const char *)"led0_task",
              (uint16_t)LED0_STK_SIZE, (void *)NULL,
              (UBaseType_t)LED0_TASK_PRIO, (TaskHandle_t *)&LED0Task_Handler);
  //创建LED1任务
  xTaskCreate((TaskFunction_t)led1_task, (const char *)"led1_task",
              (uint16_t)LED1_STK_SIZE, (void *)NULL,
              (UBaseType_t)LED1_TASK_PRIO, (TaskHandle_t *)&LED1Task_Handler);
  //浮点测试任务
  xTaskCreate((TaskFunction_t)float_task, (const char *)"float_task",
              (uint16_t)FLOAT_STK_SIZE, (void *)NULL,
              (UBaseType_t)FLOAT_TASK_PRIO, (TaskHandle_t *)&FLOATTask_Handler);
  vTaskDelete(StartTask_Handler); //删除开始任务
  taskEXIT_CRITICAL();            //退出临界区
}

// LED0任务函数
void led0_task(void *pvParameters) {
  while (1) {
    LED0 = ~LED0;
    vTaskDelay(500);
  }
}

// LED1任务函数
void led1_task(void *pvParameters) {
  while (1) {
    LED1 = 0;
    vTaskDelay(200);
    LED1 = 1;
    vTaskDelay(800);
  }
}

//浮点测试任务
void float_task(void *pvParameters) {
  static float float_num = 0.00;
  while (1) {
    float_num += 0.01f;
    printf("float_num: %.4f\r\n", float_num);
    vTaskDelay(1000);
  }
}
```
