---
layout: post
category: [FreeRTOS学习笔记]
tag: [FreeRTOS, 学习笔记]
title: FreeRTOS学习笔记3
---
# 三、FreeRTOS系统讲解

## 1. `FreeRTOSConfig.h`实现系统剪裁

**`INCLUDE_*`:**使用`INCLUDE_`开头的宏用来表示使能或除能FreeRTOS中相应的 API 函数，作用就 是用来配置FreeRTOS中的可选 API 函数的。

**`config*`**:

* `configAPPLICATION_ALLOCATED_HEAP`：FreeRTOS的堆内存大小默认由编译器分配，该配置为1则用户自己设置，需要考虑所使用的内存管理方式（heap_1.c、heap_2.c、heap_3.c、heap_4.c 、 heap_5.c）。

* `configASSERT`：需要自己定义，一般调试阶段用，会加大开销，用于检测传入的参数是否合理，参数为0则错误：

{% raw %}
```c
    // 断言，将错误打印出来 
    // 当参数 x 错误的时候就通过串口打印出发生错误的文件名和错误所在的行号，调试代码的时候可以使用断言，当调试完成以后尽量去掉断言，防止增加开销
    #define vAssertCalled(char,int) printf("Error:%s,%d\r\n",char,int)
    #define configASSERT(x) if((x)==0) vAssertCalled(__FILE__,__LINE__)
```
{% endraw %}

* `configCHECK_FOR_STACK_OVERFLOW`：检测堆栈是否溢出，堆栈溢出检测会增加上下文切换的开销，建议在调试的时候使用。使用`xTaskCreate()`则所创建的任务**自动**从FreeRTOX系统的堆`ucHeap`分配，堆栈大小由该函数`usStackDepth`决定；使用`xTaskCreateStatic()`则任务堆栈数组`pxStackBuffer`由用户设置。FreeRTOS使用两种方法来检测堆栈溢出(`#define configCHECK_FOR_STACK_OVERFLOW 1`和`#define configCHECK_FOR_STACK_OVERFLOW 2`)，方法1速度更快，方法2能检测到的堆栈溢出情况更多，该配置不为0时需要自定义`void vApplicationStackOverflowHook(TaskHandle_t xTask, char * pcTaskName);`函数，当内核检测到堆栈溢出以后就会调用该函数，`xTask`是任务句柄，`pcTaskNmae`是任务名字。**任务上下文切换时任务的现场数据都被保存到这个任务的堆栈里。**

* `configCPU_CLOCK_HZ`：设置CPU频率。

* `configSUPPORT_DYNAMIC_ALLOCATION`：为1则在创建FreeRTOS的内核对象的时候所需要的RAM就会从FreeRTOS的堆中动态的获取内存，如果定义为 0 的话所需的 RAM 就需要用户自行提供。

* `configENABLE_BACKWARD_COMPATIBILITY`：向后兼容，主要是FreeRTOS版本的数据类型的兼容。

* `configGENERATE_RUN_TIME_STATS`：为1则开启时间统计功能，还需要定义`portCONFIGURE_TIMER_FOR_RUN_TIME_STATS()`和`portGET_RUN_TIME_COUNTER_VALUE()或 portALT_GET_RUN_TIME_COUNTER_VALUE(Time)`这两种宏（初始化外设来作为时间统计的基准时钟和返回当前基准时钟的时钟值）。

* `configIDLE_SHOULD_YIELD`：空闲任务是否为其他处于同优先级的任务让出CPU使用权，建议关闭。

* `configKERNEL_INTERRUPT_PRIORITY`、`configMAX_SYSCALL_INTERRUPT_PRIORITY`、`configMAX_API_CALL_INTERRUPT_PRIORITY`：中断配置相关。

* `configMAX_CO_ROUTINE_PRIORITIES`：设置协程最大优先级数，设置后协程优先级为`0~configMAX_CO_ROUTINE_PRIORITIES-1`。

* `configMAX_PRIORITIES`：设置任务最大优先级数，数字越大任务的优先级越高。

* `configMAX_TASK_NAME_LEN`：任务名最大长度。

* `configMINIMAL_STACK_SIZE`：空闲任务的最小堆栈大小，单位为字，不是字节。

* `configNUM_THREAD_LOCAL_STORAGE_POINTERS`：设置每个任务的本地存储指针数组大小，任务控制块中有本地存储数组指针，用户应用程 序可以在这些本地存储中存入一些数据。

* `configQUEUE_REGISTRY_SIZE`：设置可以注册的队列和信号量的最大数量，在使用内核调试器查看信号量和队列的时候需 要设置此宏，而且要先将消息队列和信号量进行注册，只有注册了的队列和信号量才会再内核
    调试器中看到，如果不使用内核调试器的话此宏设置为 0 即可。

* `configSUPPORT_STATIC_ALLOCATION`：当此宏定义为 1，在创建一些内核对象的时候需要用户指定RAM，当为 0 的时候就会自使 用 heap.c 中的动态内存管理函数来自动的申请RAM。

* `configTICK_RATE_HZ`：设置 FreeRTOS 的系统时钟节拍频率，单位为 HZ，此频率就是滴答定时器的中断频率，需 要使用此宏来配置滴答定时器的中断，设为1000，周期就是1ms。

* `configTIMER_QUEUE_LENGTH`：此宏是配置 FreeRTOS 软件定时器的，FreeRTOS 的软件定时器 API 函数会通过命令队列向 软件定时器任务发送消息，此宏用来设置这个软件定时器的命令队列长度。

* `configTIMER_TASK_PRIORITY`：设置软件定时器任务的任务优先级。

* `configTIMER_TASK_STACK_DEPTH`：设置定时器服务任务的任务堆栈大小。

* `configTOTAL_HEAP_SIZE`：设置堆大小，如果使用了动态内存管理的话，FreeRTOS 在创建任务、信号量、队列等的时 候就会使用 heap_x.c(x 为 1~5)中的内存申请函数来申请内存。这些内存就是从堆
    ucHeap[configTOTAL_HEAP_SIZE]中申请的，堆的大小由 configTOTAL_HEAP_SIZE 来定义。

* `configUSE_16_BIT_TICKS`：设置系统节拍计数器变量数据类型，系统节拍计数器变量类型为 TickType_t，当 configUSE_16_BIT_TICKS 为 1 的时候 TickType_t 就是 16 位的，当 configUSE_16_BIT_TICKS
    为 0 的话 TickType_t 就是 32 位的。

* `configUSE_APPLICATION_TASK_TAG`：此宏设置为 1 的 话 函 数 configUSE_APPLICATION_TASK_TAGF() 和xTaskCallApplicationTaskHook()就会被编译。

* `configUSE_CO_ROUTINES`：此宏为 1 的时候启用协程，协程可以节省开销，但是功能有限，现在的 MCU 性能已经非 常强大了，建议关闭协程。

* `configUSE_COUNTING_SEMAPHORES`：设置为 1 的时候启用计数型信号量，相关的 API 函数会被编译。

* `configUSE_DAEMON_TASK_STARTUP_HOOK`：当宏 configUSE_TIMERS 和 configUSE_DAEMON_TASK_STARTUP_HOOK都为 1 的时需 要定义函数 void vApplicationDaemonTaskStartupHook(void)。

* `configUSE_IDLE_HOOK`：为 1 时使用空闲任务钩子函数，用户需要实现空闲任务钩子函数void vApplicationIdleHook( void )。

* `configUSE_MALLOC_FAILED_HOOK`：为 1 时使用内存分配失败钩子函数，用户需要实现内存分配失败钩子函数void vApplicationMallocFailedHook( void )。

* `configUSE_MUTEXES`：为 1 时使用互斥信号量，相关的 API 函数会被编译。

* `configUSE_PORT_OPTIMISED_TASK_SELECTION`：FreeRTOS 有两种方法来选择下一个要运行的任务，一个是通用的方法（当宏 configUSE_PORT_OPTIMISED_TASK_SELECTION 为 0，或者硬件不支持的时 候；希望所有硬件通用的时候；全部用 C 语言来实现，但是效率比特殊方法低；不限制最大优先级数目的时候。），另外一个是特殊的 方法，也就是硬件方法（不是所有的硬件都支持；当宏 configUSE_PORT_OPTIMISED_TASK_SELECTION 为 1 的时候；硬件拥有特殊的指令，比如计算前导零(CLZ)指令；比通用方法效率高；会限制优先级数目，一般是 32 个。），使用MCU自带的硬件指令来实现。STM32 有 计 算 前 导 零 的 指 令 ， 所 以 我 们 可 以 使 用 特 殊 方 法 ， 即 将 宏 configUSE_PORT_OPTIMISED_TASK_SELECTION 定义为 1。

* `configUSE_PREEMPTION`：为 1 时使用抢占式调度器，为 0 时使用协程。如果使用抢占式调度器的话内核会在每个时 钟节拍中断中进行任务切换，当使用协程的话会在如下地方进行任务切换：一个任务调用了函数 taskYIELD()；一个任务调用了可以使任务进入阻塞态的 API 函数；应用程序明确定义了在中断中执行上下文切换。

* `configUSE_QUEUE_SETS`：为 1 时启用队列集功能。

* `configUSE_RECURSIVE_MUTEXES`：为 1 时使用递归互斥信号量，相关的 API 函数会被编译。

* `configUSE_STATS_FORMATTING_FUNCTIONS`：宏 configUSE_TRACE_FACILITY 和 configUSE_STATS_FORMATTING_FUNCTIONS 都为 1 的时候函数 vTaskList()和 vTaskGetRunTimeStats()会被编译。

* `configUSE_TASK_NOTIFICATIONS`：为 1 的时候使用任务通知功能，相关的 API 函数会被编译，开启了此功能的话每个任务会 多消耗 8 个字节。

* `configUSE_TICK_HOOK`：为 1 时使能时间片钩子函数，用户需要实现时间片钩子函数void vApplicationTickHook( void )。

* `configUSE_TICKLESS_IDLE`：为 1 时使能低功耗 tickless 模式。

* `configUSE_TIMERS`：为 1 时使用软件定时器，相关的 API 函数会被编译，当宏 configUSE_TIMERS 为 1 的话， 那么宏 configTIMER_TASK_PRIORITY 、 configTIMER_QUEUE_LENGTH 和
    configTIMER_TASK_STACK_DEPTH 必须定义。

* `configUSE_TIME_SLICING`：默认情况下，FreeRTOS 使用抢占式调度器，这意味着调度器永远都在执行已经就绪了的最 高优先级任务，优先级相同的任务在时钟节拍中断中进行切换，当宏configUSE_TIME_SLICING 为 0 的时候不会在时钟节拍中断中执行相同优先级任务的任务切换，默认情况下宏
    configUSE_TIME_SLICING为 1。

* `configUSE_TRACE_FACILITY`：为 1 启用可视化跟踪调试，会增加一些结构体成员和 API 函数。

{% raw %}
```c
// FreeRTOS V9.0.0
#ifndef FREERTOS_CONFIG_H
#define FREERTOS_CONFIG_H
#include "sys.h"
#include "usart.h"
//针对不同的编译器调用不同的stdint.h文件
#if defined(__ICCARM__) || defined(__CC_ARM) || defined(__GNUC__)
#include <stdint.h>
extern uint32_t SystemCoreClock;
#endif
//断言
#define vAssertCalled(char, int) printf("Error:%s,%d\r\n", char, int)
#define configASSERT(x) \
    if ((x) == 0)       \
    vAssertCalled(__FILE__, __LINE__)
/***************************************************************************************************************/
/*                                        FreeRTOS基础配置配置选项                                              */
/***************************************************************************************************************/
#define configUSE_PREEMPTION 1                    // 1使用抢占式内核，0使用协程
#define configUSE_TIME_SLICING 1                  // 1使能时间片调度(默认式使能的)
#define configUSE_PORT_OPTIMISED_TASK_SELECTION 1 // 1启用特殊方法来选择下一个要运行的任务
                                                  //一般是硬件计算前导零指令，如果所使用的
                                                  // MCU没有这些硬件指令的话此宏应该设置为0！
#define configUSE_TICKLESS_IDLE 0                      // 1启用低功耗tickless模式
#define configUSE_QUEUE_SETS 1                         //为1时启用队列
#define configCPU_CLOCK_HZ (SystemCoreClock)           // CPU频率
#define configTICK_RATE_HZ (1000)                      //时钟节拍频率，这里设置为1000，周期就是1ms
#define configMAX_PRIORITIES (32)                      //可使用的最大优先级
#define configMINIMAL_STACK_SIZE ((unsigned short)130) //空闲任务使用的堆栈大小
#define configMAX_TASK_NAME_LEN (16)                   //任务名字字符串长度
#define configUSE_16_BIT_TICKS 0         //系统节拍计数器变量数据类型，
                                         // 1表示为16位无符号整形，0表示为32位无符号整形
#define configIDLE_SHOULD_YIELD 1        //为1时空闲任务放弃CPU使用权给其他同优先级的用户任务
#define configUSE_TASK_NOTIFICATIONS 1   //为1时开启任务通知功能，默认开启
#define configUSE_MUTEXES 1              //为1时使用互斥信号量
#define configQUEUE_REGISTRY_SIZE 8      //不为0时表示启用队列记录，具体的值是可以
                                         //记录的队列和信号量最大数目。
#define configCHECK_FOR_STACK_OVERFLOW 0 //大于0时启用堆栈溢出检测功能，如果使用此功能
                                         //用户必须提供一个栈溢出钩子函数，如果使用的话
                                         //此值可以为1或者2，因为有两种栈溢出检测方法。
#define configUSE_RECURSIVE_MUTEXES 1    //为1时使用递归互斥信号量
#define configUSE_MALLOC_FAILED_HOOK 0   // 1使用内存申请失败钩子函数
#define configUSE_APPLICATION_TASK_TAG 0
#define configUSE_COUNTING_SEMAPHORES 1 //为1时使用计数信号量
/***************************************************************************************************************/
/*                                FreeRTOS与内存申请有关配置选项                                                */
/***************************************************************************************************************/
#define configSUPPORT_DYNAMIC_ALLOCATION 1          //支持动态内存申请
#define configTOTAL_HEAP_SIZE ((size_t)(20 * 1024)) //系统所有总的堆大小
/***************************************************************************************************************/
/*                                FreeRTOS与钩子函数有关的配置选项                                              */
/***************************************************************************************************************/
#define configUSE_IDLE_HOOK 0 // 1，使用空闲钩子；0，不使用
#define configUSE_TICK_HOOK 0 // 1，使用时间片钩子；0，不使用
/***************************************************************************************************************/
/*                                FreeRTOS与运行时间和任务状态收集有关的配置选项                                 */
/***************************************************************************************************************/
#define configGENERATE_RUN_TIME_STATS 0        //为1时启用运行时间统计功能
#define configUSE_TRACE_FACILITY 1             //为1启用可视化跟踪调试
#define configUSE_STATS_FORMATTING_FUNCTIONS 1 //与宏configUSE_TRACE_FACILITY同时为1时会编译下面3个函数
                                               // prvWriteNameToBuffer(),vTaskList(),
                                               // vTaskGetRunTimeStats()
/***************************************************************************************************************/
/*                                FreeRTOS与协程有关的配置选项                                                  */
/***************************************************************************************************************/
#define configUSE_CO_ROUTINES 0             //为1时启用协程，启用协程以后必须添加文件croutine.c
#define configMAX_CO_ROUTINE_PRIORITIES (2) //协程的有效优先级数目
/***************************************************************************************************************/
/*                                FreeRTOS与软件定时器有关的配置选项                                            */
/***************************************************************************************************************/
#define configUSE_TIMERS 1                                          //为1时启用软件定时器
#define configTIMER_TASK_PRIORITY (configMAX_PRIORITIES - 1)        //软件定时器优先级
#define configTIMER_QUEUE_LENGTH 5                                  //软件定时器队列长度
#define configTIMER_TASK_STACK_DEPTH (configMINIMAL_STACK_SIZE * 2) //软件定时器任务堆栈大小
/***************************************************************************************************************/
/*                                FreeRTOS可选函数配置选项                                                      */
/***************************************************************************************************************/
#define INCLUDE_xTaskGetSchedulerState 1
#define INCLUDE_vTaskPrioritySet 1
#define INCLUDE_uxTaskPriorityGet 1
#define INCLUDE_vTaskDelete 1
#define INCLUDE_vTaskCleanUpResources 1
#define INCLUDE_vTaskSuspend 1
#define INCLUDE_vTaskDelayUntil 1
#define INCLUDE_vTaskDelay 1
#define INCLUDE_eTaskGetState 1
#define INCLUDE_xTimerPendFunctionCall 1
/***************************************************************************************************************/
/*                                FreeRTOS与中断有关的配置选项                                                  */
/***************************************************************************************************************/
#ifdef __NVIC_PRIO_BITS
#define configPRIO_BITS __NVIC_PRIO_BITS
#else
#define configPRIO_BITS 4
#endif
#define configLIBRARY_LOWEST_INTERRUPT_PRIORITY 15     //中断最低优先级
#define configLIBRARY_MAX_SYSCALL_INTERRUPT_PRIORITY 5 //系统可管理的最高中断优先级
#define configKERNEL_INTERRUPT_PRIORITY (configLIBRARY_LOWEST_INTERRUPT_PRIORITY << (8 - configPRIO_BITS))
#define configMAX_SYSCALL_INTERRUPT_PRIORITY (configLIBRARY_MAX_SYSCALL_INTERRUPT_PRIORITY << (8 - configPRIO_BITS))
/***************************************************************************************************************/
/*                                FreeRTOS与中断服务函数有关的配置选项                                          */
/***************************************************************************************************************/
#define xPortPendSVHandler PendSV_Handler
#define vPortSVCHandler SVC_Handler
#endif /* FREERTOS_CONFIG_H */
```
{% endraw %}

## 2. FreeRTOS中断配置和临界端

**1）`Cortex-M`内核中断机制：**

`Cortex-M`内核（`Cortex-M3`和`Cortex-M4`）的MCU有**用于中断管理**的嵌套向量中断控制器**NVIC**，最多支持240个IRQ、1个NMI、一个SysTick定时器中断和多个系统异常。

`CMSIS`标准将管理中断（异常）的寄存器（NVIC和系统控制块SCB）定义为结构体：STM32F

407的`core_cm4.h`的`NVIC_Type`和`SCB_Type`，NVIC和SCB都位于系统控制空间(SCS)内，SCS的地址从0XE000E000 开始:

{% raw %}
```c
#define SCS_BASE (0xE000E000UL) // SCS系统控制空间起始地址
#define NVIC_BASE (SCS_BASE + 0x0100UL)
#define SCB_BASE (SCS_BASE + 0x0D00UL) 
#define SCnSCB ((SCnSCB_Type*) SCS_BASE) 
#define SCB ((SCB_Type *) SCB_BASE) ((NVIC_Type *) NVIC_BASE ) // SCB寄存器起始地址
#define NVIC ((NVIC_Type *) NVIC_BASE ) // NVIC寄存器起始地址
```
{% endraw %}

在STM32F407的软件工程的启动文件中，有中断向量表（可从其看出有多少个中断和中断类型）

。在使用FreeRTOS，需要注意这两个中断类型的中断优先级：PendSV和SysTick。

**2）优先级分组：**

每个中断对应一对优先级（抢占优先级和响应优先级，也叫分组优先级和子优先级），高优先级中断（优先级数小）先得到响应。

Cortex-M处理器有三个固定优先级和 256 个（8位）可编程的优先级，最多有 128 个抢占优先级，但是实际的优先级数量是由芯片厂商来决定的。**STM32 就只有 16 级优先级**（标准定义是那么定义，芯片生产商可以修改），对应4位。

> Cortex-M3允许具有较少中断源时使用较少的寄存器位指定中断源的优先级，因此STM32把指定中断优先级的寄存器位减少到4位，这4个寄存器位的分组方式如下：
>
> 第0组：所有4位用于指定响应优先级，没有抢占优先级数，响应优先级数最大16。
>
> 第1组：最高1位用于指定抢占式优先级，最低3位用于指定响应优先级，抢占优先级数最大2，响应优先级数最大8。
>
> 第2组：最高2位用于指定抢占式优先级，最低2位用于指定响应优先级，抢占优先级数最大4，响应优先级数最大4。
>
> 第3组：最高3位用于指定抢占式优先级，最低1位用于指定响应优先级，抢占优先级数最大6，响应优先级数最大2。
>
> 第4组：所有4位用于指定抢占式优先级，抢占优先级数最大16，没有响应优先级数。
>
> 可以通过调用STM32的固件库中的函数NVIC_PriorityGroupConfig()选择使用哪种优先级分组方式，这个函数的参数有下列5种：
>
> NVIC_PriorityGroup_0 => 选择第0组
>
> NVIC_PriorityGroup_1 => 选择第1组
>
> NVIC_PriorityGroup_2 => 选择第2组
>
> NVIC_PriorityGroup_3 => 选择第3组
>
> NVIC_PriorityGroup_4 => 选择第4组

**STM32的做法：**宏定义`NVIC_PriorityGroup_*`是一个值（`msic.h`），该值会写入`NVIC`寄存器组里的`应用程序中断及复位控制寄存器(AIRCR)`的`优先级组(PRIGROUP)`位段，通过读取该位段的值从而得知抢占优先级和响应优先级的位数各自是多少。

**FreeRTOS 的中断配置没有处理亚优先级这种情况，所以STM32F407移植FreeRTOS只能配置为组4，直接就16个优先级。**

每个外部中断都有一个对应的优先级寄存器，每个寄存器占 8 位，4 个相邻的优先级寄存器拼成一个32位寄存器，STM32的PendSV和SysTick的优先级设置地址分别是0xE000_ED22和0xE000_ED23，FreeRTOS 在设置 PendSV 和 SysTick 的中断优先级的时候都是直接操作的地址 0xE000_ED20（直接往地址赋值），因为0xE000_ED20~0xE000_ED23这四个8位寄存器组成了一个32位寄存器。

**3）中断屏蔽：**`PRIMASK`、`FAULTMASK`和`BASEPRI`。

`PRIMASK`屏蔽模式下只能有`NMI`和`HardFalut`这两个中断，没有其他异常和中断。

`FAULTMASK`屏蔽模式下只能有`NMI`这个中断，没有其他异常和中断。

`BASEPRI`屏蔽模式下，低于某个阈值的中断会被屏蔽。

{% raw %}
```c
// 1. PRIMASK和FAULTMASK
CPSIE I; //清除 PRIMASK(使能中断)，F是FAULTMASK
CPSID I; //设置 PRIMASK(禁止中断)
或者
MOVS R0, #1
MSR PRIMASK, R0; // 将1写入PRIMASK禁止所有中断，PRIMASK可改成FAULTMASK
或者
MOVS R0, #0
MSR PRIMASK, R0; // 将0写入PRIMASK以使能中断，PRIMASK可改成FAULTMASK
// 2. BASEPRI
MOV R0, #0X60 // 优先级低于0X60的中断都屏蔽掉
MSR BASEPRI, R0
或者
MOV R0, #0 // 取消BASEPRI对中断的屏蔽
MSR BASEPRI, R0
```
{% endraw %}

**4）FreeRTOS中断配置：**

* `configPRIO_BITS`：用来设置MCU使用几位优先级，STM32 使用的是 4 位，因此此宏为 4。

* `configLIBRARY_LOWEST_INTERRUPT_PRIORITY`：设置最低优先级。STM32 优先级使用了 4 位，配置的使用组 4，也就是 4 位都是抢占优先级，因此优先级数就是 16 个，最低优先级那就是 15，所以此宏就是 15。
* `configKERNEL_INTERRUPT_PRIORITY`：用来设置PendSV和滴答定时器的中断优先级。
* `configLIBRARY_MAX_SYSCALL_INTERRUPT_PRIORITY`：设置FreeRTOS系统可管理的最大优先级，也就是BASEPRI 寄存器说的那个阈值优先级。假如设置为了 5。也就是高于 5 的优先级(优先级数小于 5)不归FreeRTOS管理。
* `configMAX_SYSCALL_INTERRUPT_PRIORITY`：阈值，低于此优先级的中断可以安全的调用 FreeRTOS 的 API 函数，高于此优先级的中断 FreeRTOS 是不能禁止和屏蔽的，**针对实时性要求严格的任务**，中断服务函数也不能调用 FreeRTOS 的 API 函数。<img src="/assets/images/FreeRTOS-study/image-20220217225143268.png" alt="image-20220217225143268" style="zoom:67%;" />

**5）FreeRTOS开关中断：**`portENABLE_INTERRUPTS()`和`portDISABLE_INTERRUPTS()`，定义在`portmacro.h`中。

**6）FreeRTOS临界段代码：**`taskENTER_CRITICAL()` 、` taskENTER_CRITICAL_FROM_ISR()`、`taskEXIT_CRITICAL()` 、和`taskEXIT_CRITICAL_FROM_ISR()`，在`task.h`中定义。

任务级临界代码保护使用方法如下（优先级低于`configMAX_SYSCALL_INTERRUPT_PRIORITY`的中断被屏蔽）：

{% raw %}
```c
void taskcritical_test(void) {
	while(1) {
        taskENTER_CRITICAL(); // 等于portDISABLE_INTERRUPTS();
        total_num+=0.01f; 
        printf("total_num 的值为: %.4f\r\n",total_num); 
        taskEXIT_CRITICAL(); // 等于portENABLE_INTERRUPTS();
        vTaskDelay(1000);
	}
}
```
{% endraw %}

`taskENTER_CRITICAL_FROM_ISR()`和`taskEXIT_CRITICAL_FROM_ISR()`是用在**中断服务程序**中的，而且这个中断的优先级一定要低于`configMAX_SYSCALL_INTERRUPT_PRIORITY`：

{% raw %}
```c
//定时器3中断服务函数，注意一定要导入stm32fxx_tim.c
void TIM3_IRQHandler(void) {
	if(TIM_GetITStatus(TIM3,TIM_IT_Update)==SET) { //溢出中断 
		status_value = taskENTER_CRITICAL_FROM_ISR();
		total_num+=1; 
    	printf("float_num的值为: %d\r\n",total_num);
		taskEXIT_CRITICAL_FROM_ISR(status_value);
	}
	TIM_ClearITPendingBit(TIM3,TIM_IT_Update); //清除中断标志位
}
```
{% endraw %}

**STM32中定时器中断的使用（注意一定要导入stm32fxx_tim.c）：**

{% raw %}
```c
#include "stm32f4xx.h"
//通用定时器3中断初始化
// arr：自动重装值。
// psc：时钟预分频数
//定时器溢出时间计算方法:Tout=((arr+1)*(psc+1))/Ft us.
// Ft=定时器工作频率,单位:Mhz
//这里使用的是定时器3!
void TIM3_Int_Init(u16 arr, u16 psc) {
  TIM_TimeBaseInitTypeDef TIM_TimeBaseInitStructure;
  NVIC_InitTypeDef NVIC_InitStructure;
  RCC_APB1PeriphClockCmd(RCC_APB1Periph_TIM3, ENABLE); ///使能TIM3时钟
  TIM_TimeBaseInitStructure.TIM_Period = arr;    //自动重装载值
  TIM_TimeBaseInitStructure.TIM_Prescaler = psc; //定时器分频
  TIM_TimeBaseInitStructure.TIM_CounterMode = TIM_CounterMode_Up; //向上计数模式
  TIM_TimeBaseInitStructure.TIM_ClockDivision = TIM_CKD_DIV1;
  TIM_TimeBaseInit(TIM3, &TIM_TimeBaseInitStructure); //初始化TIM3
  TIM_ITConfig(TIM3, TIM_IT_Update, ENABLE); //允许定时器3更新中断
  TIM_Cmd(TIM3, ENABLE);                     //使能定时器3
  NVIC_InitStructure.NVIC_IRQChannel = TIM3_IRQn; //定时器3中断
  NVIC_InitStructure.NVIC_IRQChannelPreemptionPriority = 0x04; //抢占优先级4
  NVIC_InitStructure.NVIC_IRQChannelSubPriority = 0x00;        //子优先级0
  NVIC_InitStructure.NVIC_IRQChannelCmd = ENABLE;
  NVIC_Init(&NVIC_InitStructure);
}
//定时器3中断服务函数
void TIM3_IRQHandler(void) {
  if (TIM_GetITStatus(TIM3, TIM_IT_Update) == SET) { //溢出中断
    printf("TIM3输出.......\r\n");
  }
  TIM_ClearITPendingBit(TIM3, TIM_IT_Update); //清除中断标志位
}
// 使用
TIM3_Int_Init(10000 - 1, 8400 - 1); //初始化定时器3，定时器周期1S
```
{% endraw %}

## 3. FreeRTOS任务管理

**1）任务与协程：**在FreeRTOS中应用既可以使用任务，也可以使用协程(Co-Routine)，或者两者混合使用。 但是任务和协程使用不同的API函数，因此不能通过队列(或信号量)将数据从任务发送给协程， 反之亦然。协程是为那些资源很少的MCU准备的，其开销很小，但是 FreeRTOS 官方已经不打算再更新协程了。

RTOS 调度器的职责是确保当一个任务开始执行的时候其上下文环境(寄存器值，堆栈内容等)和任务上一次退出的时候相同 ==> 每个任务都必须有个堆栈。

协程是为那些资源很少的MCU而做的，但是随着MCU的飞速发展，性能越来越强大，现 在协程几乎很少用到了！但是 FreeRTOS 目前还没有把协程移除的计划，但是 FreeRTOS 是绝对不会再更新和维护协程了。在概念上协程和任务是相似的。所有的协程使用同一个堆栈(如果是任务的话每个任务都有自己的堆栈)，这样就比使用任务消耗更少的RAM。

**2）任务状态：**<img src="/assets/images/FreeRTOS-study/image-20220217235235086.png" alt="image-20220217235235086" style="zoom:67%;" />

**3）任务优先级：**优先级数字越低表示任务的优先级越低，0 的优先级最低，configMAX_PRIORITIES-1 的优先级最高。空闲任务的优先级最低，为 0。

**4）任务实现：**

{% raw %}
```c
void vATaskFunction(void *pvParameters) {
	for( ; ; ) {
        vTaskDelay();
	} 
    /*不能从任务函数中返回或者退出，从任务函数中返回或退出的话就会调用
    configASSERT()，前提是定义了 configASSERT()。
    如果一定要从任务函数中退出的话那一定 要调用函数 
    vTaskDelete(NULL)来删除此任务。*/
	vTaskDelete(NULL); 
}
```
{% endraw %}

**5）任务控制块：**FreeRTOS 的每个任务都有一些属性需要存储，FreeRTOS 把这些属性集合到一起用一个结 构体来表示，这个结构体叫做任务控制块：TCB_t，在使用函数 xTaskCreate()创建任务的时候就会**自动的给每个任务分配一个任务控制块**。在老版本的 FreeRTOS 中任务控制块叫做 tskTCB。

**6）任务堆栈大小：**在`portmacro.h`中指定。

{% raw %}
```c
#define portSTACK_TYPE uint32_t // 4个字节
#define portBASE_TYPE long
typedef portSTACK_TYPE StackType_t;
```
{% endraw %}

**7）任务创建和删除API：**<img src="/assets/images/FreeRTOS-study/image-20220218000524649.png" alt="image-20220218000524649" style="zoom:67%;" />

**任务需要RAM来保存与任务有关的状态信息(任务控制块)，任务也需要一定的 RAM 来作为任务堆栈。**

* `xTaskCreate()`：任务所需RAM自动从FreeRTOS的堆中分配，因此必须提供内存管理方式（`heap_*.c`)，`configSUPPORT_DYNAMIC_ALLOCATION必须为`必须为1，新创建的任务默认就是就绪态的，因此不管在任务调度器启动前还是启动后，都可以创建任务。

{% raw %}
```c
    BaseType_t xTaskCreate( TaskFunction_t pxTaskCode, // 任务函数
                            const char * const pcName, // 任务名字，长度不能超过configMAX_TASK_NAME_LEN
                            const uint16_t usStackDepth, // 堆栈大小
                            void * const pvParameters, // 传递给任务函数的参数
                            UBaseType_t uxPriority, // 任务优先级
                            TaskHandle_t * const pxCreatedTask ) // 任务句柄
    // 返回值
    pdPASS: 任务创建成功。
    errCOULD_NOT_ALLOCATE_REQUIRED_MEMORY： 任务创建失败，因为堆内存不足。
```
{% endraw %}

* `xTaskCreateStatic()`：任务所需的RAM由用户提供，`configSUPPORT_STATIC_ALLOCATION`必须设为1，还需要实现函 数`vApplicationGetIdleTaskMemory()`和`vApplicationGetTimerTaskMemory()`。任务的堆栈、任务控制块就需要由用户来指定了。

{% raw %}
```c
    #include "FreeRTOS.h"
    #include "delay.h"
    #include "led.h"
    #include "sys.h"
    #include "task.h"
    #include "timer.h"
    #include "usart.h"
    static StackType_t IdleTaskStack[configMINIMAL_STACK_SIZE]; //空闲任务任务堆栈
    static StaticTask_t IdleTaskTCB; //空闲任务控制块
    static StackType_t TimerTaskStack[configTIMER_TASK_STACK_DEPTH]; //定时器服务任务堆栈
    static StaticTask_t TimerTaskTCB; //定时器服务任务控制块
    #define START_TASK_PRIO 1 //任务优先级
    #define START_STK_SIZE 128 //任务堆栈大小
    StackType_t StartTaskStack[START_STK_SIZE]; //任务堆栈
    StaticTask_t StartTaskTCB; //任务控制块
    TaskHandle_t StartTask_Handler; //任务句柄
    void start_task(void *pvParameters); //任务函数
    #define TASK1_TASK_PRIO 2 //任务优先级
    #define TASK1_STK_SIZE 128 //任务堆栈大小
    StaskType_t Task1TaskStack[TASK1_STK_SIZE]; //任务堆栈
    StaticTask_t Task1TaskTCB; //任务控制块
    TaskHandle_t Task1Task_Handler; //任务句柄
    void task1_task(void *pvParameters); //任务函数
    #define TASK2_TASK_PRIO 3 //任务优先级
    #define TASK2_STK_SIZE 128 //任务堆栈大小
    StackType_t Task2TaskStack[TASK2_STK_SIZE]; //任务堆栈
    StaticTask_t Task2TaskTCB; //任务控制块
    TaskHandle_t Task2Task_Handler; //任务句柄
    void task2_task(void *pvParameters); //任务函数
    //获取空闲任务地任务堆栈和任务控制块内存，因为本例程使用的
    //静态内存，因此空闲任务的任务堆栈和任务控制块的内存就应该
    //有用户来提供，FreeRTOS提供了接口函数vApplicationGetIdleTaskMemory()
    //实现此函数即可。
    // ppxIdleTaskTCBBuffer:任务控制块内存
    // ppxIdleTaskStackBuffer:任务堆栈内存
    // pulIdleTaskStackSize:任务堆栈大小
    void vApplicationGetIdleTaskMemory(StaticTask_t **ppxIdleTaskTCBBuffer,
                                       StackType_t **ppxIdleTaskStackBuffer,
                                       uint32_t *pulIdleTaskStackSize) {
      *ppxIdleTaskTCBBuffer = &IdleTaskTCB;
      *ppxIdleTaskStackBuffer = IdleTaskStack;
      *pulIdleTaskStackSize = configMINIMAL_STACK_SIZE;
    }
    //获取定时器服务任务的任务堆栈和任务控制块内存
    // ppxTimerTaskTCBBuffer:任务控制块内存
    // ppxTimerTaskStackBuffer:任务堆栈内存
    // pulTimerTaskStackSize:任务堆栈大小
    void vApplicationGetTimerTaskMemory(StaticTask_t **ppxTimerTaskTCBBuffer,
                                        StackType_t **ppxTimerTaskStackBuffer,
                                        uint32_t *pulTimerTaskStackSize) {
      *ppxTimerTaskTCBBuffer = &TimerTaskTCB;
      *ppxTimerTaskStackBuffer = TimerTaskStack;
      *pulTimerTaskStackSize = configTIMER_TASK_STACK_DEPTH;
    }
    int main(void) {
      NVIC_PriorityGroupConfig(NVIC_PriorityGroup_4); //设置系统中断优先级分组4
      delay_init(168);                                //初始化延时函数
      uart_init(115200);                              //初始化串口
      LED_Init();                                     //初始化LED端口
      //创建开始任务
      StartTask_Handler =
          xTaskCreateStatic((TaskFunction_t)start_task, //任务函数
                            (const char *)"start_task", //任务名称
                            (uint32_t)START_STK_SIZE,   //任务堆栈大小
                            (void *)NULL, //传递给任务函数的参数
                            (UBaseType_t)START_TASK_PRIO,   //任务优先级
                            (StackType_t *)StartTaskStack,  //任务堆栈
                            (StaticTask_t *)&StartTaskTCB); //任务控制块
      vTaskStartScheduler();                                //开启任务调度
    }
    //开始任务任务函数
    void start_task(void *pvParameters) {
      taskENTER_CRITICAL(); //进入临界区
                            //创建TASK1任务
      Task1Task_Handler = xTaskCreateStatic(
          (TaskFunction_t)task1_task, (const char *)"task1_task",
          (uint32_t)TASK1_STK_SIZE, (void *)NULL, (UBaseType_t)TASK1_TASK_PRIO,
          (StackType_t *)Task1TaskStack, (StaticTask_t *)&Task1TaskTCB);
      //创建TASK2任务
      Task2Task_Handler = xTaskCreateStatic(
          (TaskFunction_t)task2_task, (const char *)"task2_task",
          (uint32_t)TASK2_STK_SIZE, (void *)NULL, (UBaseType_t)TASK2_TASK_PRIO,
          (StackType_t *)Task2TaskStack, (StaticTask_t *)&Task2TaskTCB);
      vTaskDelete(StartTask_Handler); //删除开始任务
      taskEXIT_CRITICAL();            //退出临界区
    }
    // task1任务函数
    void task1_task(void *pvParameters) {
      u8 task1_num = 0;
      while (1) {
        task1_num++; //任务执1行次数加1 注意task1_num1加到255的时候会清零！！
        LED0 = !LED0;
        printf("任务1已经执行：%d次\r\n", task1_num);
        if (task1_num == 5) {
          if (Task2Task_Handler != NULL) //任务2是否存在？
          {
            vTaskDelete(Task2Task_Handler); //任务1执行5次删除任务2
            Task2Task_Handler = NULL;       //任务句柄清零
            printf("任务1删除了任务2!\r\n");
          }
        }
        vTaskDelay(1000); //延时1s，也就是1000个时钟节拍
      }
    }
    // task2任务函数
    void task2_task(void *pvParameters) {
      u8 task2_num = 0;
      while (1) {
        task2_num++; //任务2执行次数加1 注意task1_num2加到255的时候会清零！！
        LED1 = !LED1;
        printf("任务2已经执行：%d次\r\n", task2_num);
        vTaskDelay(1000); //延时1s，也就是1000个时钟节拍
      }
    }
```
{% endraw %}

{% raw %}
```c
    // 返回值：
    NULL：任务创建失败，puxStackBuffer 或 pxTaskBuffer 为 NULL 的时候会导致这个 错误的发生。
    其他值: 任务创建成功，返回任务的任务句柄。
```
{% endraw %}

* `xTaskCreateRestricted(const TaskParameters_t * const pxTaskDefinition, TaskHandle_t *
    pxCreatedTask)`：此函数要求所使用的 MCU 有 MPU(内存保护单元)， 用此函数创建的任务会受到MPU的保护，其他的功能和函数 xTaxkCreate()一样。

{% raw %}
```c
    // 参数
    pxTaskDefinition: 指向一个结构体 TaskParameters_t，这个结构体描述了任务的任务函数、 堆栈大小、优先级等。此结构体在文件 task.h 中有定义。 
    pxCreatedTask：任务句柄。
    // 返回值
    pdPASS:任务创建成功。
    其他值: 任务未创建成功，很有可能是因为 FreeRTOS 的堆太小了。
```
{% endraw %}

* `vTaskDelete(TaskHandle_t xTaskToDelete)`：参数是任务句柄，没有返回值。如果任务是使用动态方法创建的，也就是使用函数xTaskCreate()创建的，那么在此任务被删除以后此任务之前申请的堆栈和控制块内存会在空闲任务中被释放掉，因此当调用函数 vTaskDelete()删除任务以后必须给空闲任务一定的运行时间。**空间任务用来释放内核所分配的内存空间。**但用户在任务中`pvPortMalloc()`自己手动分配了内存，必须自己`vPortFree()`手动释放掉，不然会导致内存泄露。

* 调用`vTaskStartScheduler()`开启FreeRTOS的任务调度器，FreeRTOS开始运行。

    







