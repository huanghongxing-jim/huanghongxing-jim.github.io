---
layout: post
category: [FreeRTOS学习笔记]
tag: [FreeRTOS, 学习笔记]
title: FreeRTOS学习笔记1
---
# 一、资源

## 1. 硬件

使用的板子是正点原子的`STM32F407`最小系统板，芯片是`STM32F407ZGT`。板载资源（《STM32F407最小系统板开发指南-库函数版本_V1.1.pdf》）：

![image-20220215231728103](/assets/images/FreeRTOS-study/image-20220215231728103.png)

<img src="/assets/images/FreeRTOS-study/1E24ABB56DBDD608AAD3E49A87902725.png" alt="img" style="zoom: 25%;" />

## 2. 系统

[FreeRTOS官网](https://www.freertos.org/)下载FreeRTOS源码（FreeRTOSv9.0.0）：

<img src="/assets/images/FreeRTOS-study/image-20220215233214965.png" alt="image-20220215233214965" style="zoom:67%;" />

![image-20220215235026632](/assets/images/FreeRTOS-study/image-20220215235026632.png)

**RVDS文件夹里对不同架构的MCU做了分类，STM32F407参考ARM_CM4F(port.c, portmacro.h)架构。**

# 二、移植

## 1. 基础例程

### 概念：

* ARM：做芯片标准的公司。
* TI、ST公司：根据芯片标准做芯片的公司。

* CMSIS(Cortex Microcontroler Software Interface Standard)标准：为了让不同芯片生成商（ST、TI）所生产的Cortex-M4芯片在软件上兼容。基于CMSIS标准的应用程序结构：

    <img src="/assets/images/FreeRTOS-study/image-20220216165923676.png" alt="image-20220216165923676" style="zoom: 67%;" />

###  官方固件库(1.4版本)

![image-20220216171733416](/assets/images/FreeRTOS-study/image-20220216171733416.png)

### 固件库主要文件关系图

![image-20220216173702933](/assets/images/FreeRTOS-study/image-20220216173702933.png)

**还需要启动文件：调用SystemInit()，然后进入main()函数。不同型号的芯片启动文件不一样。**

` STM32F4 `的启动文件存放在目录`\STM32F4xx_DSP_StdPeriph_Lib_V1.4.0\Libraries\CMSIS\Device\ST\STM32F4xx\Source\Templates\arm`下面。

### 工程模板（正点原子）

1. 本地新建工程文件夹，Keil里New Project将工程保存进该文件夹里，弹出了Device界面，选择对应的芯片。**该Device是让Keil环境兼容不同芯片的开发编译，故而需要到Keil官网安装对应的器件pack才有得选择。**

2. FWLIB和CORE:![image-20220216180827504](/assets/images/FreeRTOS-study/image-20220216180827504.png)

3. USER：![image-20220216181659344](/assets/images/FreeRTOS-study/image-20220216181659344.png)

4. 工程添加文件：<img src="/assets/images/FreeRTOS-study/image-20220216191524314.png" alt="image-20220216191524314" style="zoom:67%;" />

5. 设置编译环境：![image-20220216184629830](/assets/images/FreeRTOS-study/image-20220216184629830.png)

6. 清空`stm32f4xx_it.c`文件和编辑`main.c`文件：

    ```c
    // main.c
    
    #include "stm32f4xx.h"
    
    void Delay(__IO uint32_t nCount) {
      while (nCount--) {
      }
    }
    
    int main(void) {
    
      GPIO_InitTypeDef GPIO_InitStructure;
      RCC_AHB1PeriphClockCmd(RCC_AHB1Periph_GPIOF, ENABLE);
      GPIO_InitStructure.GPIO_Pin = GPIO_Pin_9 | GPIO_Pin_10;
      GPIO_InitStructure.GPIO_Mode = GPIO_Mode_OUT;
      GPIO_InitStructure.GPIO_OType = GPIO_OType_PP;
      GPIO_InitStructure.GPIO_Speed = GPIO_Speed_100MHz;
      GPIO_InitStructure.GPIO_PuPd = GPIO_PuPd_UP;
      GPIO_Init(GPIOF, &GPIO_InitStructure);
    
      while (1) {
        GPIO_SetBits(GPIOF, GPIO_Pin_9 | GPIO_Pin_10);
        Delay(0x7FFFFF);
        GPIO_ResetBits(GPIOF, GPIO_Pin_9 | GPIO_Pin_10);
        Delay(0x7FFFFF);
      }
    }
    ```
<img src="/assets/images/FreeRTOS-study/image-20220216224022065.png" alt="image-20220216224022065" style="zoom:67%;" />

7. 编译：<img src="/assets/images/FreeRTOS-study/image-20220216191741658.png" alt="image-20220216191741658" style="zoom: 67%;" />

8. 烧写：<img src="/assets/images/FreeRTOS-study/image-20220216193613872.png" alt="image-20220216193613872" style="zoom:67%;" />

    **注意：**

    * STM32串口下载方法：BOOT0接V3.3，BOOT1接GND，按复位键。一键烧写电路注意通过控制DTR和RTS电平，从而控制BOOT0和RESET。
    * FlyMcu每次下载要整片擦除，故下载较慢，DAP下载不用，JLINK下载也很快。

9. **便捷通用代码（正点原子）：**delay, sys, usart。这些代码是 STM32F4xx 系列的底层核心驱动函数，可以用在 STM32F4xx系列的各个型号上面，能够快速的给任何一款 STM32F4 构建最基本的框架。

    使用示例（main.c）：

    ```c
    #include "delay.h"
    #include "stm32f4xx.h"
    #include "usart.h"
    int main(void) {
      u32 t = 0;
      uart_init(115200);
      delay_init(84); // 84是系统时钟频率
      while (1) {
        printf("t:%d\r\n", t);
        delay_ms(500);
        t++;
      }
    }
    ```

    ![image-20220216232834325](/assets/images/FreeRTOS-study/image-20220216232834325.png)

    串口打印输出：<img src="/assets/images/FreeRTOS-study/image-20220216233759762.png" alt="image-20220216233759762" style="zoom:67%;" />

    **delay.c:**

    ```c
    #include "delay.h"
    #include "sys.h"
    ////////////////////////////////////////////////////////////////////////////////// 	 
    //如果使用OS,则包括下面的头文件（以ucos为例）即可.
    #if SYSTEM_SUPPORT_OS
    #include "includes.h"					//支持OS时，使用	  
    #endif
    //////////////////////////////////////////////////////////////////////////////////  
    //本程序只供学习使用，未经作者许可，不得用于其它任何用途
    //ALIENTEK STM32F407开发板
    //使用SysTick的普通计数模式对延迟进行管理(支持OS)
    //包括delay_us,delay_ms
    //正点原子@ALIENTEK
    //技术论坛:www.openedv.com
    //创建日期:2014/5/2
    //版本：V1.3
    //版权所有，盗版必究。
    //Copyright(C) 广州市星翼电子科技有限公司 2014-2024
    //All rights reserved
    //********************************************************************************
    //修改说明
    //V1.1 20140803 
    //1,delay_us,添加参数等于0判断,如果参数等于0,则直接退出. 
    //2,修改ucosii下,delay_ms函数,加入OSLockNesting的判断,在进入中断后,也可以准确延时.
    //V1.2 20150411  
    //修改OS支持方式,以支持任意OS(不限于UCOSII和UCOSIII,理论上任意OS都可以支持)
    //添加:delay_osrunning/delay_ostickspersec/delay_osintnesting三个宏定义
    //添加:delay_osschedlock/delay_osschedunlock/delay_ostimedly三个函数
    //V1.3 20150521
    //修正UCOSIII支持时的2个bug：
    //delay_tickspersec改为：delay_ostickspersec
    //delay_intnesting改为：delay_osintnesting
    ////////////////////////////////////////////////////////////////////////////////// 
    
    static u8  fac_us=0;							//us延时倍乘数			   
    static u16 fac_ms=0;							//ms延时倍乘数,在os下,代表每个节拍的ms数
    	
    #if SYSTEM_SUPPORT_OS							//如果SYSTEM_SUPPORT_OS定义了,说明要支持OS了(不限于UCOS).
    //当delay_us/delay_ms需要支持OS的时候需要三个与OS相关的宏定义和函数来支持
    //首先是3个宏定义:
    //    delay_osrunning:用于表示OS当前是否正在运行,以决定是否可以使用相关函数
    //delay_ostickspersec:用于表示OS设定的时钟节拍,delay_init将根据这个参数来初始哈systick
    // delay_osintnesting:用于表示OS中断嵌套级别,因为中断里面不可以调度,delay_ms使用该参数来决定如何运行
    //然后是3个函数:
    //  delay_osschedlock:用于锁定OS任务调度,禁止调度
    //delay_osschedunlock:用于解锁OS任务调度,重新开启调度
    //    delay_ostimedly:用于OS延时,可以引起任务调度.
    
    //本例程仅作UCOSII和UCOSIII的支持,其他OS,请自行参考着移植
    //支持UCOSII
    #ifdef 	OS_CRITICAL_METHOD						//OS_CRITICAL_METHOD定义了,说明要支持UCOSII				
    #define delay_osrunning		OSRunning			//OS是否运行标记,0,不运行;1,在运行
    #define delay_ostickspersec	OS_TICKS_PER_SEC	//OS时钟节拍,即每秒调度次数
    #define delay_osintnesting 	OSIntNesting		//中断嵌套级别,即中断嵌套次数
    #endif
    
    //支持UCOSIII
    #ifdef 	CPU_CFG_CRITICAL_METHOD					//CPU_CFG_CRITICAL_METHOD定义了,说明要支持UCOSIII	
    #define delay_osrunning		OSRunning			//OS是否运行标记,0,不运行;1,在运行
    #define delay_ostickspersec	OSCfg_TickRate_Hz	//OS时钟节拍,即每秒调度次数
    #define delay_osintnesting 	OSIntNestingCtr		//中断嵌套级别,即中断嵌套次数
    #endif
    
    
    //us级延时时,关闭任务调度(防止打断us级延迟)
    void delay_osschedlock(void)
    {
    #ifdef CPU_CFG_CRITICAL_METHOD   			//使用UCOSIII
    	OS_ERR err; 
    	OSSchedLock(&err);						//UCOSIII的方式,禁止调度，防止打断us延时
    #else										//否则UCOSII
    	OSSchedLock();							//UCOSII的方式,禁止调度，防止打断us延时
    #endif
    }
    
    //us级延时时,恢复任务调度
    void delay_osschedunlock(void)
    {	
    #ifdef CPU_CFG_CRITICAL_METHOD   			//使用UCOSIII
    	OS_ERR err; 
    	OSSchedUnlock(&err);					//UCOSIII的方式,恢复调度
    #else										//否则UCOSII
    	OSSchedUnlock();						//UCOSII的方式,恢复调度
    #endif
    }
    
    //调用OS自带的延时函数延时
    //ticks:延时的节拍数
    void delay_ostimedly(u32 ticks)
    {
    #ifdef CPU_CFG_CRITICAL_METHOD
    	OS_ERR err; 
    	OSTimeDly(ticks,OS_OPT_TIME_PERIODIC,&err);//UCOSIII延时采用周期模式
    #else
    	OSTimeDly(ticks);						//UCOSII延时
    #endif 
    }
     
    //systick中断服务函数,使用OS时用到
    void SysTick_Handler(void)
    {	
    	if(delay_osrunning==1)					//OS开始跑了,才执行正常的调度处理
    	{
    		OSIntEnter();						//进入中断
    		OSTimeTick();       				//调用ucos的时钟服务程序               
    		OSIntExit();       	 				//触发任务切换软中断
    	}
    }
    #endif
    			   
    //初始化延迟函数
    //当使用OS的时候,此函数会初始化OS的时钟节拍
    //SYSTICK的时钟固定为AHB时钟的1/8
    //SYSCLK:系统时钟频率
    void delay_init(u8 SYSCLK)
    {
    #if SYSTEM_SUPPORT_OS 						//如果需要支持OS.
    	u32 reload;
    #endif
     	SysTick_CLKSourceConfig(SysTick_CLKSource_HCLK_Div8); 
    	fac_us=SYSCLK/8;						//不论是否使用OS,fac_us都需要使用
    #if SYSTEM_SUPPORT_OS 						//如果需要支持OS.
    	reload=SYSCLK/8;						//每秒钟的计数次数 单位为M	   
    	reload*=1000000/delay_ostickspersec;	//根据delay_ostickspersec设定溢出时间
    											//reload为24位寄存器,最大值:16777216,在168M下,约合0.7989s左右	
    	fac_ms=1000/delay_ostickspersec;		//代表OS可以延时的最少单位	   
    	SysTick->CTRL|=SysTick_CTRL_TICKINT_Msk;   	//开启SYSTICK中断
    	SysTick->LOAD=reload; 					//每1/delay_ostickspersec秒中断一次	
    	SysTick->CTRL|=SysTick_CTRL_ENABLE_Msk; 	//开启SYSTICK    
    #else
    	fac_ms=(u16)fac_us*1000;				//非OS下,代表每个ms需要的systick时钟数   
    #endif
    }								    
    
    #if SYSTEM_SUPPORT_OS 						//如果需要支持OS.
    //延时nus
    //nus:要延时的us数.	
    //nus:0~204522252(最大值即2^32/fac_us@fac_us=21)	    								   
    void delay_us(u32 nus)
    {		
    	u32 ticks;
    	u32 told,tnow,tcnt=0;
    	u32 reload=SysTick->LOAD;				//LOAD的值	    	 
    	ticks=nus*fac_us; 						//需要的节拍数 
    	delay_osschedlock();					//阻止OS调度，防止打断us延时
    	told=SysTick->VAL;        				//刚进入时的计数器值
    	while(1)
    	{
    		tnow=SysTick->VAL;	
    		if(tnow!=told)
    		{	    
    			if(tnow<told)tcnt+=told-tnow;	//这里注意一下SYSTICK是一个递减的计数器就可以了.
    			else tcnt+=reload-tnow+told;	    
    			told=tnow;
    			if(tcnt>=ticks)break;			//时间超过/等于要延迟的时间,则退出.
    		}  
    	};
    	delay_osschedunlock();					//恢复OS调度											    
    }  
    //延时nms
    //nms:要延时的ms数
    //nms:0~65535
    void delay_ms(u16 nms)
    {	
    	if(delay_osrunning&&delay_osintnesting==0)//如果OS已经在跑了,并且不是在中断里面(中断里面不能任务调度)	    
    	{		 
    		if(nms>=fac_ms)						//延时的时间大于OS的最少时间周期 
    		{ 
       			delay_ostimedly(nms/fac_ms);	//OS延时
    		}
    		nms%=fac_ms;						//OS已经无法提供这么小的延时了,采用普通方式延时    
    	}
    	delay_us((u32)(nms*1000));				//普通方式延时
    }
    #else  //不用ucos时
    //延时nus
    //nus为要延时的us数.	
    //注意:nus的值,不要大于798915us(最大值即2^24/fac_us@fac_us=21)
    void delay_us(u32 nus)
    {		
    	u32 temp;	    	 
    	SysTick->LOAD=nus*fac_us; 				//时间加载	  		 
    	SysTick->VAL=0x00;        				//清空计数器
    	SysTick->CTRL|=SysTick_CTRL_ENABLE_Msk ; //开始倒数 	 
    	do
    	{
    		temp=SysTick->CTRL;
    	}while((temp&0x01)&&!(temp&(1<<16)));	//等待时间到达   
    	SysTick->CTRL&=~SysTick_CTRL_ENABLE_Msk; //关闭计数器
    	SysTick->VAL =0X00;       				//清空计数器 
    }
    //延时nms
    //注意nms的范围
    //SysTick->LOAD为24位寄存器,所以,最大延时为:
    //nms<=0xffffff*8*1000/SYSCLK
    //SYSCLK单位为Hz,nms单位为ms
    //对168M条件下,nms<=798ms 
    void delay_xms(u16 nms)
    {	 		  	  
    	u32 temp;		   
    	SysTick->LOAD=(u32)nms*fac_ms;			//时间加载(SysTick->LOAD为24bit)
    	SysTick->VAL =0x00;           			//清空计数器
    	SysTick->CTRL|=SysTick_CTRL_ENABLE_Msk ;          //开始倒数 
    	do
    	{
    		temp=SysTick->CTRL;
    	}while((temp&0x01)&&!(temp&(1<<16)));	//等待时间到达   
    	SysTick->CTRL&=~SysTick_CTRL_ENABLE_Msk;       //关闭计数器
    	SysTick->VAL =0X00;     		  		//清空计数器	  	    
    } 
    //延时nms 
    //nms:0~65535
    void delay_ms(u16 nms)
    {	 	 
    	u8 repeat=nms/540;						//这里用540,是考虑到某些客户可能超频使用,
    											//比如超频到248M的时候,delay_xms最大只能延时541ms左右了
    	u16 remain=nms%540;
    	while(repeat)
    	{
    		delay_xms(540);
    		repeat--;
    	}
    	if(remain)delay_xms(remain);
    } 
    #endif
    ```

    **delay.h:**

    ```c
    #ifndef __DELAY_H
    #define __DELAY_H 			   
    #include <sys.h>	  
    //////////////////////////////////////////////////////////////////////////////////  
    //本程序只供学习使用，未经作者许可，不得用于其它任何用途
    //ALIENTEK STM32F407开发板
    //使用SysTick的普通计数模式对延迟进行管理(支持ucosii)
    //包括delay_us,delay_ms
    //正点原子@ALIENTEK
    //技术论坛:www.openedv.com
    //修改日期:2014/5/2
    //版本：V1.0
    //版权所有，盗版必究。
    //Copyright(C) 广州市星翼电子科技有限公司 2014-2024
    //All rights reserved
    //********************************************************************************
    //修改说明
    //无
    ////////////////////////////////////////////////////////////////////////////////// 	 
    void delay_init(u8 SYSCLK);
    void delay_ms(u16 nms);
    void delay_us(u32 nus);
    
    #endif
    ```

    **sys.c:**

    ```c
    #include "sys.h"  
    //////////////////////////////////////////////////////////////////////////////////	 
    //本程序只供学习使用，未经作者许可，不得用于其它任何用途
    //ALIENTEK STM32F407开发板
    //系统时钟初始化	
    //包括时钟设置/中断管理/GPIO设置等
    //正点原子@ALIENTEK
    //技术论坛:www.openedv.com
    //创建日期:2014/5/2
    //版本：V1.0
    //版权所有，盗版必究。
    //Copyright(C) 广州市星翼电子科技有限公司 2014-2024
    //All rights reserved
    //********************************************************************************
    //修改说明
    //无
    //////////////////////////////////////////////////////////////////////////////////  
    
    
    //THUMB指令不支持汇编内联
    //采用如下方法实现执行汇编指令WFI  
    __asm void WFI_SET(void)
    {
    	WFI;		  
    }
    //关闭所有中断(但是不包括fault和NMI中断)
    __asm void INTX_DISABLE(void)
    {
    	CPSID   I
    	BX      LR	  
    }
    //开启所有中断
    __asm void INTX_ENABLE(void)
    {
    	CPSIE   I
    	BX      LR  
    }
    //设置栈顶地址
    //addr:栈顶地址
    __asm void MSR_MSP(u32 addr) 
    {
    	MSR MSP, r0 			//set Main Stack value
    	BX r14
    }
    ```

    **sys.h:**

    ```c
    #ifndef __SYS_H
    #define __SYS_H	 
    #include "stm32f4xx.h" 
    //////////////////////////////////////////////////////////////////////////////////	 
    //本程序只供学习使用，未经作者许可，不得用于其它任何用途
    //ALIENTEK STM32F407开发板
    //系统时钟初始化	
    //正点原子@ALIENTEK
    //技术论坛:www.openedv.com
    //创建日期:2014/5/2
    //版本：V1.0
    //版权所有，盗版必究。
    //Copyright(C) 广州市星翼电子科技有限公司 2014-2024
    //All rights reserved
    //********************************************************************************
    //修改说明
    //无
    ////////////////////////////////////////////////////////////////////////////////// 
    
    
    //0,不支持ucos
    //1,支持ucos
    #define SYSTEM_SUPPORT_OS		0		//定义系统文件夹是否支持UCOS
    																	    
    	 
    //位带操作,实现51类似的GPIO控制功能
    //具体实现思想,参考<<CM3权威指南>>第五章(87页~92页).M4同M3类似,只是寄存器地址变了.
    //IO口操作宏定义
    #define BITBAND(addr, bitnum) ((addr & 0xF0000000)+0x2000000+((addr &0xFFFFF)<<5)+(bitnum<<2)) 
    #define MEM_ADDR(addr)  *((volatile unsigned long  *)(addr)) 
    #define BIT_ADDR(addr, bitnum)   MEM_ADDR(BITBAND(addr, bitnum)) 
    //IO口地址映射
    #define GPIOA_ODR_Addr    (GPIOA_BASE+20) //0x40020014
    #define GPIOB_ODR_Addr    (GPIOB_BASE+20) //0x40020414 
    #define GPIOC_ODR_Addr    (GPIOC_BASE+20) //0x40020814 
    #define GPIOD_ODR_Addr    (GPIOD_BASE+20) //0x40020C14 
    #define GPIOE_ODR_Addr    (GPIOE_BASE+20) //0x40021014 
    #define GPIOF_ODR_Addr    (GPIOF_BASE+20) //0x40021414    
    #define GPIOG_ODR_Addr    (GPIOG_BASE+20) //0x40021814   
    #define GPIOH_ODR_Addr    (GPIOH_BASE+20) //0x40021C14    
    #define GPIOI_ODR_Addr    (GPIOI_BASE+20) //0x40022014     
    
    #define GPIOA_IDR_Addr    (GPIOA_BASE+16) //0x40020010 
    #define GPIOB_IDR_Addr    (GPIOB_BASE+16) //0x40020410 
    #define GPIOC_IDR_Addr    (GPIOC_BASE+16) //0x40020810 
    #define GPIOD_IDR_Addr    (GPIOD_BASE+16) //0x40020C10 
    #define GPIOE_IDR_Addr    (GPIOE_BASE+16) //0x40021010 
    #define GPIOF_IDR_Addr    (GPIOF_BASE+16) //0x40021410 
    #define GPIOG_IDR_Addr    (GPIOG_BASE+16) //0x40021810 
    #define GPIOH_IDR_Addr    (GPIOH_BASE+16) //0x40021C10 
    #define GPIOI_IDR_Addr    (GPIOI_BASE+16) //0x40022010 
     
    //IO口操作,只对单一的IO口!
    //确保n的值小于16!
    #define PAout(n)   BIT_ADDR(GPIOA_ODR_Addr,n)  //输出 
    #define PAin(n)    BIT_ADDR(GPIOA_IDR_Addr,n)  //输入 
    
    #define PBout(n)   BIT_ADDR(GPIOB_ODR_Addr,n)  //输出 
    #define PBin(n)    BIT_ADDR(GPIOB_IDR_Addr,n)  //输入 
    
    #define PCout(n)   BIT_ADDR(GPIOC_ODR_Addr,n)  //输出 
    #define PCin(n)    BIT_ADDR(GPIOC_IDR_Addr,n)  //输入 
    
    #define PDout(n)   BIT_ADDR(GPIOD_ODR_Addr,n)  //输出 
    #define PDin(n)    BIT_ADDR(GPIOD_IDR_Addr,n)  //输入 
    
    #define PEout(n)   BIT_ADDR(GPIOE_ODR_Addr,n)  //输出 
    #define PEin(n)    BIT_ADDR(GPIOE_IDR_Addr,n)  //输入
    
    #define PFout(n)   BIT_ADDR(GPIOF_ODR_Addr,n)  //输出 
    #define PFin(n)    BIT_ADDR(GPIOF_IDR_Addr,n)  //输入
    
    #define PGout(n)   BIT_ADDR(GPIOG_ODR_Addr,n)  //输出 
    #define PGin(n)    BIT_ADDR(GPIOG_IDR_Addr,n)  //输入
    
    #define PHout(n)   BIT_ADDR(GPIOH_ODR_Addr,n)  //输出 
    #define PHin(n)    BIT_ADDR(GPIOH_IDR_Addr,n)  //输入
    
    #define PIout(n)   BIT_ADDR(GPIOI_ODR_Addr,n)  //输出 
    #define PIin(n)    BIT_ADDR(GPIOI_IDR_Addr,n)  //输入
    
    //以下为汇编函数
    void WFI_SET(void);		//执行WFI指令
    void INTX_DISABLE(void);//关闭所有中断
    void INTX_ENABLE(void);	//开启所有中断
    void MSR_MSP(u32 addr);	//设置堆栈地址 
    #endif
    ```

    **usart.c:**

    ```c
    #include "sys.h"
    #include "usart.h"	
    ////////////////////////////////////////////////////////////////////////////////// 	 
    //如果使用ucos,则包括下面的头文件即可.
    #if SYSTEM_SUPPORT_OS
    #include "includes.h"					//ucos 使用	  
    #endif
    //////////////////////////////////////////////////////////////////////////////////	 
    //本程序只供学习使用，未经作者许可，不得用于其它任何用途
    //ALIENTEK STM32F4探索者开发板
    //串口1初始化		   
    //正点原子@ALIENTEK
    //技术论坛:www.openedv.com
    //修改日期:2014/6/10
    //版本：V1.5
    //版权所有，盗版必究。
    //Copyright(C) 广州市星翼电子科技有限公司 2009-2019
    //All rights reserved
    //********************************************************************************
    //V1.3修改说明 
    //支持适应不同频率下的串口波特率设置.
    //加入了对printf的支持
    //增加了串口接收命令功能.
    //修正了printf第一个字符丢失的bug
    //V1.4修改说明
    //1,修改串口初始化IO的bug
    //2,修改了USART_RX_STA,使得串口最大接收字节数为2的14次方
    //3,增加了USART_REC_LEN,用于定义串口最大允许接收的字节数(不大于2的14次方)
    //4,修改了EN_USART1_RX的使能方式
    //V1.5修改说明
    //1,增加了对UCOSII的支持
    ////////////////////////////////////////////////////////////////////////////////// 	  
     
    
    //////////////////////////////////////////////////////////////////
    //加入以下代码,支持printf函数,而不需要选择use MicroLIB	  
    #if 1
    #pragma import(__use_no_semihosting)             
    //标准库需要的支持函数                 
    struct __FILE 
    { 
    	int handle; 
    }; 
    
    FILE __stdout;       
    //定义_sys_exit()以避免使用半主机模式    
    void _sys_exit(int x) 
    { 
    	x = x; 
    } 
    //重定义fputc函数 
    int fputc(int ch, FILE *f)
    { 	
    	while((USART1->SR&0X40)==0);//循环发送,直到发送完毕   
    	USART1->DR = (u8) ch;      
    	return ch;
    }
    #endif
     
    #if EN_USART1_RX   //如果使能了接收
    //串口1中断服务程序
    //注意,读取USARTx->SR能避免莫名其妙的错误   	
    u8 USART_RX_BUF[USART_REC_LEN];     //接收缓冲,最大USART_REC_LEN个字节.
    //接收状态
    //bit15，	接收完成标志
    //bit14，	接收到0x0d
    //bit13~0，	接收到的有效字节数目
    u16 USART_RX_STA=0;       //接收状态标记	
    
    //初始化IO 串口1 
    //bound:波特率
    void uart_init(u32 bound){
       //GPIO端口设置
      GPIO_InitTypeDef GPIO_InitStructure;
    	USART_InitTypeDef USART_InitStructure;
    	NVIC_InitTypeDef NVIC_InitStructure;
    	
    	RCC_AHB1PeriphClockCmd(RCC_AHB1Periph_GPIOA,ENABLE); //使能GPIOA时钟
    	RCC_APB2PeriphClockCmd(RCC_APB2Periph_USART1,ENABLE);//使能USART1时钟
     
    	//串口1对应引脚复用映射
    	GPIO_PinAFConfig(GPIOA,GPIO_PinSource9,GPIO_AF_USART1); //GPIOA9复用为USART1
    	GPIO_PinAFConfig(GPIOA,GPIO_PinSource10,GPIO_AF_USART1); //GPIOA10复用为USART1
    	
    	//USART1端口配置
      GPIO_InitStructure.GPIO_Pin = GPIO_Pin_9 | GPIO_Pin_10; //GPIOA9与GPIOA10
    	GPIO_InitStructure.GPIO_Mode = GPIO_Mode_AF;//复用功能
    	GPIO_InitStructure.GPIO_Speed = GPIO_Speed_50MHz;	//速度50MHz
    	GPIO_InitStructure.GPIO_OType = GPIO_OType_PP; //推挽复用输出
    	GPIO_InitStructure.GPIO_PuPd = GPIO_PuPd_UP; //上拉
    	GPIO_Init(GPIOA,&GPIO_InitStructure); //初始化PA9，PA10
    
       //USART1 初始化设置
    	USART_InitStructure.USART_BaudRate = bound;//波特率设置
    	USART_InitStructure.USART_WordLength = USART_WordLength_8b;//字长为8位数据格式
    	USART_InitStructure.USART_StopBits = USART_StopBits_1;//一个停止位
    	USART_InitStructure.USART_Parity = USART_Parity_No;//无奇偶校验位
    	USART_InitStructure.USART_HardwareFlowControl = USART_HardwareFlowControl_None;//无硬件数据流控制
    	USART_InitStructure.USART_Mode = USART_Mode_Rx | USART_Mode_Tx;	//收发模式
      USART_Init(USART1, &USART_InitStructure); //初始化串口1
    	
      USART_Cmd(USART1, ENABLE);  //使能串口1 
    	
    	//USART_ClearFlag(USART1, USART_FLAG_TC);
    	
    #if EN_USART1_RX	
    	USART_ITConfig(USART1, USART_IT_RXNE, ENABLE);//开启相关中断
    
    	//Usart1 NVIC 配置
      NVIC_InitStructure.NVIC_IRQChannel = USART1_IRQn;//串口1中断通道
    	NVIC_InitStructure.NVIC_IRQChannelPreemptionPriority=3;//抢占优先级3
    	NVIC_InitStructure.NVIC_IRQChannelSubPriority =3;		//子优先级3
    	NVIC_InitStructure.NVIC_IRQChannelCmd = ENABLE;			//IRQ通道使能
    	NVIC_Init(&NVIC_InitStructure);	//根据指定的参数初始化VIC寄存器、
    
    #endif
    	
    }
    
    
    void USART1_IRQHandler(void)                	//串口1中断服务程序
    {
    	u8 Res;
    #if SYSTEM_SUPPORT_OS 		//如果SYSTEM_SUPPORT_OS为真，则需要支持OS.
    	OSIntEnter();    
    #endif
    	if(USART_GetITStatus(USART1, USART_IT_RXNE) != RESET)  //接收中断(接收到的数据必须是0x0d 0x0a结尾)
    	{
    		Res =USART_ReceiveData(USART1);//(USART1->DR);	//读取接收到的数据
    		
    		if((USART_RX_STA&0x8000)==0)//接收未完成
    		{
    			if(USART_RX_STA&0x4000)//接收到了0x0d
    			{
    				if(Res!=0x0a)USART_RX_STA=0;//接收错误,重新开始
    				else USART_RX_STA|=0x8000;	//接收完成了 
    			}
    			else //还没收到0X0D
    			{	
    				if(Res==0x0d)USART_RX_STA|=0x4000;
    				else
    				{
    					USART_RX_BUF[USART_RX_STA&0X3FFF]=Res ;
    					USART_RX_STA++;
    					if(USART_RX_STA>(USART_REC_LEN-1))USART_RX_STA=0;//接收数据错误,重新开始接收	  
    				}		 
    			}
    		}   		 
      } 
    #if SYSTEM_SUPPORT_OS 	//如果SYSTEM_SUPPORT_OS为真，则需要支持OS.
    	OSIntExit();  											 
    #endif
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
    //////////////////////////////////////////////////////////////////////////////////	 
    //本程序只供学习使用，未经作者许可，不得用于其它任何用途
    //Mini STM32开发板
    //串口1初始化		   
    //正点原子@ALIENTEK
    //技术论坛:www.openedv.csom
    //修改日期:2011/6/14
    //版本：V1.4
    //版权所有，盗版必究。
    //Copyright(C) 正点原子 2009-2019
    //All rights reserved
    //********************************************************************************
    //V1.3修改说明 
    //支持适应不同频率下的串口波特率设置.
    //加入了对printf的支持
    //增加了串口接收命令功能.
    //修正了printf第一个字符丢失的bug
    //V1.4修改说明
    //1,修改串口初始化IO的bug
    //2,修改了USART_RX_STA,使得串口最大接收字节数为2的14次方
    //3,增加了USART_REC_LEN,用于定义串口最大允许接收的字节数(不大于2的14次方)
    //4,修改了EN_USART1_RX的使能方式
    ////////////////////////////////////////////////////////////////////////////////// 	
    #define USART_REC_LEN  			200  	//定义最大接收字节数 200
    #define EN_USART1_RX 			1		//使能（1）/禁止（0）串口1接收
    	  	
    extern u8  USART_RX_BUF[USART_REC_LEN]; //接收缓冲,最大USART_REC_LEN个字节.末字节为换行符 
    extern u16 USART_RX_STA;         		//接收状态标记	
    //如果想串口中断接收，请不要注释以下宏定义
    void uart_init(u32 bound);
    #endif
    ```