---
layout: post
category: [FreeRTOS学习笔记]
tag: [FreeRTOS, 学习笔记]
title: FreeRTOS学习笔记4
---
**8）任务挂起和恢复：**<img src="/assets/images/FreeRTOS-study/image-20220218005157889.png" alt="image-20220218005157889" style="zoom:67%;" />

* `void vTaskSuspend( TaskHandle_t xTaskToSuspend )`：可以通过函数`xTaskGetHandle()`来根据任务**名字**来获取某个任务的任务句柄，如果参数为NULL 的话表示挂起任务自己，没有返回值。

* `void vTaskResume( TaskHandle_t xTaskToResume)`：挂起态进入到就绪态。

* `BaseType_t xTaskResumeFromISR( TaskHandle_t xTaskToResume)`：在中断服务函数中恢复一个任务。

{% raw %}
```c
    // 返回值
    pdTRUE:恢复运行的任务的任务优先级等于或者高于正在运行的任务(被中断打断的任务)，这意味着在退出中断服务函数以后必须进行一次上下文切换。
    pdFALSE:恢复运行的任务的任务优先级低于当前正在运行的任务(被中断打断的任务)，这意味着在退出中断服务函数的以后不需要进行上下文切换。
```
{% endraw %}

{% raw %}
```c
    // 外部中断4服务程序 
    void EXTI4_IRQHandler(void) {
    	BaseType_t YieldRequired; 
        delay_xms(20);
    	//消抖
    	if(KEY0==0) {
    		YieldRequired=xTaskResumeFromISR(Task2Task_Handler);//恢复任务 2
    		printf("恢复任务 2 的运行!\r\n"); 
        	if(YieldRequired==pdTRUE) {
    		/*如果函数 xTaskResumeFromISR()返回值为 pdTRUE，那么说明要恢复的这个 任务的任务优先级等于或者高于正在运行的任务(被中断打断的任务),所以在 退出中断的时候一定要进行上下文切换！*/ 					portYIELD_FROM_ISR(YieldRequired);
    		} 
    	}
        EXTI_ClearITPendingBit(EXTI_Line4);//清除 LINE4 上的中断标志位
    }
```
{% endraw %}

## 4. FreeRTOS列表和列表项

列表是 FreeRTOS 中的一个数据结构，概念上和链表有点类似，列表被用来跟踪 FreeRTOS 中的任务。与列表相关的全部东西都在文件 list.c 和 list.h 中。在 list.h 中定义了一个叫 List_t 的结构体。

**1）数据结构：**

<img src="/assets/images/FreeRTOS-study/image-20220218120047267.png" alt="image-20220218120047267" style="zoom:67%;" />![image-20220218120144687](/assets/images/FreeRTOS-study/image-20220218120144687.png)

> 列表项中一个非常重要的成员是`pvOwner`，它指向列表项所属的任务控制块`TCB`，何为TCB？简单理解为储存任务特性的结构，任务具有状态、堆栈、优先级等特性，这些特性需要储存起来供系统使用，比如根据优先级进行任务切换等等，储存的结构就称为TCB，TCB应该是操作系统中最大的一个结构体了，包含着非常多的信息。

**2）相关API（`list.c`和`list.h`）：**

{% raw %}
```c
void vListInitialise( List_t * const pxList ); // 列表初始化
void vListInitialiseItem( ListItem_t * const pxItem ); // 列表项初始化
void vListInsert( List_t * const pxList, ListItem_t * const pxNewListItem ); // 列表项根据值从小到大插入
void vListInsertEnd( List_t * const pxList, ListItem_t * const pxNewListItem ); // 列表末尾插入
UBaseType_t uxListRemove( ListItem_t * const pxItemToRemove ); // 返回新列表的当前列表项数目
listGET_OWNER_OF_NEXT_ENTRY( pxTCB, pxList ); // 列表遍历，还函数是个宏，用于从多个同优先级的就绪任务中查找下一个要运行的任务。pxTCB用来保存pxIndex所指向的列表项的pvOwner变量值，也就是这个列表项属于谁的？通常是一个任务的任务控制块。pxList表示要遍历的列表
```
{% endraw %}

**3）例子：**

{% raw %}
```c
#include "FreeRTOS.h"
List_t TestList;	  //测试用列表
ListItem_t ListItem1; //测试用列表项1
ListItem_t ListItem2; //测试用列表项2
ListItem_t ListItem3; //测试用列表项3
void list_task(void *pvParameters)
{
	//第一步：初始化列表和列表项
	vListInitialise(&TestList);
	vListInitialiseItem(&ListItem1);
	vListInitialiseItem(&ListItem2);
	vListInitialiseItem(&ListItem3);
	ListItem1.xItemValue = 40; // ListItem1列表项值为40
	ListItem2.xItemValue = 60; // ListItem2列表项值为60
	ListItem3.xItemValue = 50; // ListItem3列表项值为50
	printf("/*******************列表和列表项地址*******************/\r\n");
	printf("项目                              地址				    \r\n");
	printf("TestList                          %#x					\r\n", (int)&TestList);
	printf("TestList->pxIndex                 %#x					\r\n", (int)TestList.pxIndex);
	printf("TestList->xListEnd                %#x					\r\n", (int)(&TestList.xListEnd));
	printf("ListItem1                         %#x					\r\n", (int)&ListItem1);
	printf("ListItem2                         %#x					\r\n", (int)&ListItem2);
	printf("ListItem3                         %#x					\r\n", (int)&ListItem3);
	vListInsert(&TestList, &ListItem1); //插入列表项ListItem1
	printf("/******************添加列表项ListItem1*****************/\r\n");
	printf("项目                              地址				    \r\n");
	printf("TestList->xListEnd->pxNext        %#x					\r\n", (int)(TestList.xListEnd.pxNext));
	printf("ListItem1->pxNext                 %#x					\r\n", (int)(ListItem1.pxNext));
	printf("/*******************前后向连接分割线********************/\r\n");
	printf("TestList->xListEnd->pxPrevious    %#x					\r\n", (int)(TestList.xListEnd.pxPrevious));
	printf("ListItem1->pxPrevious             %#x					\r\n", (int)(ListItem1.pxPrevious));
	vListInsert(&TestList, &ListItem2); //插入列表项ListItem2
	printf("/******************添加列表项ListItem2*****************/\r\n");
	printf("项目                              地址				    \r\n");
	printf("TestList->xListEnd->pxNext        %#x					\r\n", (int)(TestList.xListEnd.pxNext));
	printf("ListItem1->pxNext                 %#x					\r\n", (int)(ListItem1.pxNext));
	printf("ListItem2->pxNext                 %#x					\r\n", (int)(ListItem2.pxNext));
	printf("/*******************前后向连接分割线********************/\r\n");
	printf("TestList->xListEnd->pxPrevious    %#x					\r\n", (int)(TestList.xListEnd.pxPrevious));
	printf("ListItem1->pxPrevious             %#x					\r\n", (int)(ListItem1.pxPrevious));
	printf("ListItem2->pxPrevious             %#x					\r\n", (int)(ListItem2.pxPrevious));
	vListInsert(&TestList, &ListItem3); //插入列表项ListItem3
	printf("/******************添加列表项ListItem3*****************/\r\n");
	printf("项目                              地址				    \r\n");
	printf("TestList->xListEnd->pxNext        %#x					\r\n", (int)(TestList.xListEnd.pxNext));
	printf("ListItem1->pxNext                 %#x					\r\n", (int)(ListItem1.pxNext));
	printf("ListItem3->pxNext                 %#x					\r\n", (int)(ListItem3.pxNext));
	printf("ListItem2->pxNext                 %#x					\r\n", (int)(ListItem2.pxNext));
	printf("/*******************前后向连接分割线********************/\r\n");
	printf("TestList->xListEnd->pxPrevious    %#x					\r\n", (int)(TestList.xListEnd.pxPrevious));
	printf("ListItem1->pxPrevious             %#x					\r\n", (int)(ListItem1.pxPrevious));
	printf("ListItem3->pxPrevious             %#x					\r\n", (int)(ListItem3.pxPrevious));
	printf("ListItem2->pxPrevious             %#x					\r\n", (int)(ListItem2.pxPrevious));
	uxListRemove(&ListItem2); //删除ListItem2
	printf("/******************删除列表项ListItem2*****************/\r\n");
	printf("项目                              地址				    \r\n");
	printf("TestList->xListEnd->pxNext        %#x					\r\n", (int)(TestList.xListEnd.pxNext));
	printf("ListItem1->pxNext                 %#x					\r\n", (int)(ListItem1.pxNext));
	printf("ListItem3->pxNext                 %#x					\r\n", (int)(ListItem3.pxNext));
	printf("/*******************前后向连接分割线********************/\r\n");
	printf("TestList->xListEnd->pxPrevious    %#x					\r\n", (int)(TestList.xListEnd.pxPrevious));
	printf("ListItem1->pxPrevious             %#x					\r\n", (int)(ListItem1.pxPrevious));
	printf("ListItem3->pxPrevious             %#x					\r\n", (int)(ListItem3.pxPrevious));
	TestList.pxIndex = TestList.pxIndex->pxNext; // pxIndex向后移一项，这样pxIndex就会指向ListItem1。
	vListInsertEnd(&TestList, &ListItem2);		 //列表末尾添加列表项ListItem2
	printf("/***************在末尾添加列表项ListItem2***************/\r\n");
	printf("项目                              地址				    \r\n");
	printf("TestList->pxIndex                 %#x					\r\n", (int)TestList.pxIndex);
	printf("TestList->xListEnd->pxNext        %#x					\r\n", (int)(TestList.xListEnd.pxNext));
	printf("ListItem2->pxNext                 %#x					\r\n", (int)(ListItem2.pxNext));
	printf("ListItem1->pxNext                 %#x					\r\n", (int)(ListItem1.pxNext));
	printf("ListItem3->pxNext                 %#x					\r\n", (int)(ListItem3.pxNext));
	printf("/*******************前后向连接分割线********************/\r\n");
	printf("TestList->xListEnd->pxPrevious    %#x					\r\n", (int)(TestList.xListEnd.pxPrevious));
	printf("ListItem2->pxPrevious             %#x					\r\n", (int)(ListItem2.pxPrevious));
	printf("ListItem1->pxPrevious             %#x					\r\n", (int)(ListItem1.pxPrevious));
	printf("ListItem3->pxPrevious             %#x					\r\n", (int)(ListItem3.pxPrevious));
}
```
{% endraw %}

## 5. FreeRTOS调度器原理讲解

<img src="/assets/images/FreeRTOS-study/image-20220218122434558.png" alt="image-20220218122434558" style="zoom: 67%;" />

> 空闲任务:  vTaskStartScheduler()函数会创建一个名为“IDLE”的任务，这个任务叫做空闲任务。顾名思义，空闲任务就是空闲的时候运行的任务，也就是系统中其他 的任务由于各种原因不能运行的时候空闲任务就在运行。空闲任务是 FreeRTOS 系统自动创建 的，不需要用户手动创建。任务调度器启动以后就必须有一个任务运行！但是空闲任务不仅仅是为了满足任务调度器启动以后至少有一个任务运行而创建的，空闲任务中还会去做一些其他 的事情，如下： 1、判断系统是否有任务删除，如果有的话就在空闲任务中释放被删除任务的任务堆栈和任务控制块的内存。 2、运行用户设置的空闲任务钩子函数。 3、判断是否开启低功耗 tickless 模式，如果开启的话还需要做相应的处理 空闲任务的任务优先级是最低的，为 0，任务函数为 prvIdleTask()。

## 6. FreeRTOS任务切换

> SVC--系统服务调用，PendSV--可悬起系统调用，多用在系统软件开发中。SVC用于产生系统函数的调用请求，例如操作系统不让用户程序直接访问硬件，而是通过一些系统服务函数，让用户程序使用SVC发出对系统服务函数的呼叫请求，以此来间接访问硬件。NMI服务例程不能使用SVC指令，否则产生硬fault。SVC异常必须得到立即响应，否则将会产生硬fault。

* FreeRTOS任务上下文切换发生在`PendSV`中断服务函数`xPortPendSVHandler()==PendSV_Handler()`里，任务切换的场合：可以执行一个系统调用；系统滴答定时器（SysTick）中断。

* 任务切换函数`taskYIELD()==portYIELD()`（`task.h`）。

* 系统滴答定时器（SysTick）中断进行任务切换:

{% raw %}
```c
    void xPortSysTickHandler( void ) {
    	vPortRaiseBASEPRI(); 
    	if( xTaskIncrementTick() != pdFALSE ) { 
        	portNVIC_INT_CTRL_REG = portNVIC_PENDSVSET_BIT; // 通过向中断控制和壮态寄存器 ICSR 的 bit28 写入 1 挂起 PendSV 来启动 PendSV 中 断。这样就可以在 PendSV 中断服务函数中进行任务切换了
        } 
    	vPortClearBASEPRIFromISR();
    }
```
{% endraw %}

## 7. FreeROTS内核控制函数

内核控制函数就是 FreeRTOS 内核所使用的函数，一般情况下应用层程序不使 用这些函数，在 FreeRTOS 官网可以找到这些函数。

![image-20220218142724388](/assets/images/FreeRTOS-study/image-20220218142724388.png)

## 8. 任务相关API函数

![image-20220218142748705](/assets/images/FreeRTOS-study/image-20220218142748705.png)

**FreeRTOS 运行时间壮态统计函数`vTaskGetRunTimeStats()`获取任务的运行时间信息：**

{% raw %}
```c
#include "sys.h"
#include "delay.h"
#include "usart.h"
#include "key.h"
#include "string.h"
#include "FreeRTOS.h"
#include "task.h"
#define START_TASK_PRIO 1
#define START_STK_SIZE 128
TaskHandle_t StartTask_Handler;
void start_task(void *pvParameters);
#define TASK1_TASK_PRIO 2
#define TASK1_STK_SIZE 128
TaskHandle_t Task1Task_Handler;
void task1_task(void *pvParameters);
#define TASK2_TASK_PRIO 3
#define TASK2_STK_SIZE 128
TaskHandle_t Task2Task_Handler;
void task2_task(void *pvParameters);
#define RUNTIMESTATS_TASK_PRIO 4
#define RUNTIMESTATS_STK_SIZE 128
TaskHandle_t RunTimeStats_Handler;
void RunTimeStats_task(void *pvParameters);
char RunTimeInfo[400]; // 保存任务运行时间信息
int main(void)
{
	NVIC_PriorityGroupConfig(NVIC_PriorityGroup_4); //设置系统中断优先级分组4
	delay_init(168);								//初始化延时函数
	uart_init(115200);								//初始化串口
	xTaskCreate((TaskFunction_t)start_task,			 //任务函数
				(const char *)"start_task",			 //任务名称
				(uint16_t)START_STK_SIZE,			 //任务堆栈大小
				(void *)NULL,						 //传递给任务函数的参数
				(UBaseType_t)START_TASK_PRIO,		 //任务优先级
				(TaskHandle_t *)&StartTask_Handler); //任务句柄
	vTaskStartScheduler();							 //开启任务调度
}
void start_task(void *pvParameters)
{
	taskENTER_CRITICAL(); //进入临界区
	//创建TASK1任务
	xTaskCreate((TaskFunction_t)task1_task,
				(const char *)"task1_task",
				(uint16_t)TASK1_STK_SIZE,
				(void *)NULL,
				(UBaseType_t)TASK1_TASK_PRIO,
				(TaskHandle_t *)&Task1Task_Handler);
	//创建TASK2任务
	xTaskCreate((TaskFunction_t)task2_task,
				(const char *)"task2_task",
				(uint16_t)TASK2_STK_SIZE,
				(void *)NULL,
				(UBaseType_t)TASK2_TASK_PRIO,
				(TaskHandle_t *)&Task2Task_Handler);
	//创建RunTimeStats任务
	xTaskCreate((TaskFunction_t)RunTimeStats_task,
				(const char *)"RunTimeStats_task",
				(uint16_t)RUNTIMESTATS_STK_SIZE,
				(void *)NULL,
				(UBaseType_t)RUNTIMESTATS_TASK_PRIO,
				(TaskHandle_t *)&RunTimeStats_Handler);
	vTaskDelete(StartTask_Handler); //删除开始任务
	taskEXIT_CRITICAL();			//退出临界区
}
void task1_task(void *pvParameters) {
	while (1) {
		vTaskDelay(1000);										  
	}
}
void task2_task(void *pvParameters) {	
    while (1) {
		vTaskDelay(1000);												
	}
}
// RunTimeStats任务
void RunTimeStats_task(void *pvParameters) {
	u8 key = 0;
	while (1) {
		key = KEY_Scan(0);
		if (key == WKUP_PRES) {
			memset(RunTimeInfo, 0, 400);	   //信息缓冲区清零
			vTaskGetRunTimeStats(RunTimeInfo); //获取任务运行时间信息
			printf("任务名\t\t\t运行时间\t运行所占百分比\r\n");
			printf("%s\r\n", RunTimeInfo);
		}
		vTaskDelay(10); //延时10ms，也就是1000个时钟节拍
	}
}
```
{% endraw %}

结果：![image-20220218143747388](/assets/images/FreeRTOS-study/image-20220218143747388.png)

## 9. FreeRTOS时间管理

**1）FreeRTOS延时函数：**

* `vTaskDelay()`：`INCLUDE_vTaskDelay`必须为1。`task.c`。相对延时函数。参数为要延时的时间节拍数。

* `prvAddCurrentTaskToDelayedList(TickType_t xTicksToWait, const BaseType_t xCanBlockIndefinitely)`：用于将当前任务添加到等待列表中。`task.c`。

* `xTaskDelayUntil(TickType_t * const pxPreviousWakeTime, const TickType_t xTimeIncrement)`：阻塞任务，阻塞时间是一个绝对时间，那些需要按照一定的频率 运行的任务可以使用该函数。`task.c`。

{% raw %}
```c
    void TestTask( void * pvParameters ) {
    	TickType_t PreviousWakeTime; 
        //延时 50ms，但是函数 vTaskDelayUntil()的参数需要设置的是延时的节拍数，不能直接 
        //设置延时时间，因此使用函数 pdMS_TO_TICKS 将时间转换为节拍数。 
        const TickType_t TimeIncrement = pdMS_TO_TICKS( 50 );
    	PreviousWakeTime = xTaskGetTickCount();
    	for( ;; ) {
        /******************************************************************/
        /*************************任务主体*********************************/
        /******************************************************************/
        //调用函数 vTaskDelayUntil 进行延时 
        	vTaskDelayUntil( &PreviousWakeTime, TimeIncrement);
    	}
    }
```
{% endraw %}

**2）FreeRTOS系统时钟节拍：**

不管是什么系统，运行都需要有个系统时钟节拍，前面已经提到多次了，`xTickCount`就是 FreeRTOS 的系统时钟节拍计数器。每个滴答定时器中断中`xTickCount`就会加一，`xTickCount`的具体操作过程是在函数`xTaskIncrementTick()`中进行的，此函数在文件`tasks.c`中有定义。

## 10. FreeRTOS队列

FreeRTOS 提供了一个叫做**队列**的机制来完成任务与任务、任务与中断之间的消息传递，还有**专属于中断服务程序的队列机制`*FromISR()`**。

**例子：**

{% raw %}
```c
#include "sys.h"
#include "delay.h"
#include "usart.h"
#include "key.h"
#include "malloc.h"
#include "FreeRTOS.h"
#include "task.h"
#include "queue.h"
#include "string.h" // 该库来自编译环境，提供strchr()、strlen()、strlcpy()等字符串操作
#define START_TASK_PRIO 1
#define START_STK_SIZE 256
TaskHandle_t StartTask_Handler;
void start_task(void *pvParameters);
#define TASK1_TASK_PRIO 2
#define TASK1_STK_SIZE 256
TaskHandle_t Task1Task_Handler;
void task1_task(void *pvParameters);
#define KEYPROCESS_TASK_PRIO 3
#define KEYPROCESS_STK_SIZE 256
TaskHandle_t Keyprocess_Handler;
void Keyprocess_task(void *pvParameters);
//按键消息队列的数量
#define KEYMSG_Q_NUM 1       //按键消息队列的数量
#define MESSAGE_Q_NUM 4      //发送数据的消息队列的数量
QueueHandle_t Key_Queue;     //按键值消息队列句柄
QueueHandle_t Message_Queue; //信息队列句柄
//查询Message_Queue队列中的总队列数量和剩余队列数量
void check_msg_queue(void)
{
    u8 *p;
    u8 msgq_remain_size; //消息队列剩余大小
    u8 msgq_total_size;  //消息队列总大小
    taskENTER_CRITICAL();                                                                            
    msgq_remain_size = uxQueueSpacesAvailable(Message_Queue); //得到队列剩余大小
    msgq_total_size = uxQueueMessagesWaiting(Message_Queue) + uxQueueSpacesAvailable(Message_Queue); //得到队列总大小，总大小=使用+剩余的。
    p = mymalloc(SRAMIN, 20); //申请内存，SRAMIN是内部内存池
    sprintf((char *)p, "Total Size:%d", msgq_total_size); //显示DATA_Msg消息队列总的大小
    sprintf((char *)p, "Remain Size:%d", msgq_remain_size); //显示DATA_Msg剩余大小
    myfree(SRAMIN, p);   //释放内存
    taskEXIT_CRITICAL(); //退出临界区
}
int main(void)
{
    NVIC_PriorityGroupConfig(NVIC_PriorityGroup_4); //设置系统中断优先级分组4
    delay_init(168);                                //初始化延时函数
    uart_init(115200);                              //初始化串口
    LED_Init();                                     //初始化LED端口
    KEY_Init();                                     //初始化按键
    TIM9_Int_Init(5000, 16800 - 1);                 //初始化定时器9，周期500ms
    my_mem_init(SRAMIN);                            //初始化内部内存池
    xTaskCreate((TaskFunction_t)start_task,          //任务函数
                (const char *)"start_task",          //任务名称
                (uint16_t)START_STK_SIZE,            //任务堆栈大小
                (void *)NULL,                        //传递给任务函数的参数
                (UBaseType_t)START_TASK_PRIO,        //任务优先级
                (TaskHandle_t *)&StartTask_Handler); //任务句柄
    vTaskStartScheduler();                           //开启任务调度
}
void start_task(void *pvParameters)
{
    taskENTER_CRITICAL(); 
    //创建消息队列
    Key_Queue = xQueueCreate(KEYMSG_Q_NUM, sizeof(u8));         //创建消息Key_Queue
    Message_Queue = xQueueCreate(MESSAGE_Q_NUM, USART_REC_LEN); //创建消息Message_Queue, USART_REC_LEN是串口最大允许接收的字节数(不大于2的14次方)
    xTaskCreate((TaskFunction_t)task1_task,
                (const char *)"task1_task",
                (uint16_t)TASK1_STK_SIZE,
                (void *)NULL,
                (UBaseType_t)TASK1_TASK_PRIO,
                (TaskHandle_t *)&Task1Task_Handler);
    xTaskCreate((TaskFunction_t)Keyprocess_task,
                (const char *)"keyprocess_task",
                (uint16_t)KEYPROCESS_STK_SIZE,
                (void *)NULL,
                (UBaseType_t)KEYPROCESS_TASK_PRIO,
                (TaskHandle_t *)&Keyprocess_Handler);
    vTaskDelete(StartTask_Handler); //删除开始任务
    taskEXIT_CRITICAL();            //退出临界区
}
// task1任务函数
void task1_task(void *pvParameters) {
    u8 key, i = 0;
    BaseType_t err;
    while (1) {
        key = KEY_Scan(0);                //扫描按键
        if ((Key_Queue != NULL) && (key)) { //消息队列Key_Queue创建成功,并且按键被按下
            /* 10是阻塞时间，数据类型是TickType_t，此参数指示当队列满的时候任务进入阻塞态等待队列空闲的最大时间。
            如果为0的话当队列满的时候就立即返回；当为portMAX_DELAY的话就会一直等待，
            直到队列有空闲的队列项，也就是死等，但是宏INCLUDE_vTaskSuspend必须为 1。*/
            err = xQueueSend(Key_Queue, &key, 10);
            if (err == errQUEUE_FULL) { //发送按键值
                printf("队列Key_Queue已满，数据发送失败!\r\n");
            }
        }
        i++;
        if (i % 10 == 0)
            check_msg_queue(); //检Message_Queue队列的容量
        if (i == 50) {
            i = 0;
            LED0 = !LED0;
        }
        vTaskDelay(10); //延时10ms，也就是10个时钟节拍
    }
}
// Keyprocess_task函数
void Keyprocess_task(void *pvParameters) {
    u8 key;
    while (1) {
        if (Key_Queue != NULL) {
            //请求消息Key_Queue，portMAX_DELAY定义在portmacro.h里
            if (xQueueReceive(Key_Queue, &key, portMAX_DELAY)) { 
                switch (key) {
                case WKUP_PRES:
                    break;
                case KEY2_PRES: 
                    break;
                case KEY0_PRES:
                    break;
                }
            }
        }
        vTaskDelay(10); //延时10ms，也就是10个时钟节拍
    }
}
```
{% endraw %}

## 11.FreeRTOS信号量

二值信号量（优先级翻转），计数型信号量，互斥信号量，递归互斥信号量。

## 12. FreeRTOS软件定时器

MCU自带的定时器属于硬件定时器，不同的 MCU 其硬件定时器数量不同。FreeRTOS提供了软件定时器，但精度没有硬件定时器高。

**1）相关配置`FreeRTOSConfig.h`：**

* `configUSE_TIMERS`：设置为1的话定时器服务任务就会在启动 FreeRTOS 调度器的时候**自动创建**。
* `configTIMER_TASK_PRIORITY`：设置软件定时器服务任务的任务优先级，可以为 0~( configMAX_PRIORITIES-1)。

* `configTIMER_QUEUE_LENGTH`：设置定时器命令队列的队列长度。
* `configTIMER_TASK_STACK_DEPTH`：此宏用来设置定时器服务任务的任务堆栈大小，单位为字，不是字节，对于 STM32 来说 一个字是 4 字节。由于定时器服务任务中会执行定时器的回调函数，因此任务堆栈的大小一定要根据定时器的回调函数来设置。

**2）类别：**单次定时器和周期定时器。

**3）软件定时器复位：**任务函数`xTimerReset()`和中断服务函数`xTimerResetFromISR()`。

**4）创建定时器：**动态方法`xTimerCreate()`和静态方法`xTimerCreateStatic()`。

**5）开启定时器：**任务函数`xTimerStart()`和中断函数`xTimerStartFromISR()`。

**6）停止定时器：**任务函数`xTimerStop()`和中断函数`xTimerStopFromISR()`。

例子：

{% raw %}
```c
#include "sys.h"
#include "delay.h"
#include "usart.h"
#include "led.h"
#include "timer.h" // STM32自带定时器
#include "key.h"
#include "string.h"
#include "malloc.h"
#include "FreeRTOS.h"
#include "task.h"
#include "timers.h" // FreeRTOS软件定时器库函数
#define START_TASK_PRIO 1
#define START_STK_SIZE 256
TaskHandle_t StartTask_Handler;
void start_task(void *pvParameters);
#define TIMERCONTROL_TASK_PRIO 2
#define TIMERCONTROL_STK_SIZE 256
TaskHandle_t TimerControlTask_Handler;
void timercontrol_task(void *pvParameters);
TimerHandle_t AutoReloadTimer_Handle; //周期定时器句柄
TimerHandle_t OneShotTimer_Handle;	  //单次定时器句柄
void AutoReloadCallback(TimerHandle_t xTimer); //周期定时器回调函数
void OneShotCallback(TimerHandle_t xTimer);	   //单次定时器回调函数
int main(void) {
	NVIC_PriorityGroupConfig(NVIC_PriorityGroup_4); //设置系统中断优先级分组4
	delay_init(168);								//初始化延时函数
	uart_init(115200);								//初始化串口
	LED_Init();										//初始化LED端口
	KEY_Init();										//初始化按键
	my_mem_init(SRAMIN);							//初始化内部内存池
	xTaskCreate((TaskFunction_t)start_task,			 //任务函数
				(const char *)"start_task",			 //任务名称
				(uint16_t)START_STK_SIZE,			 //任务堆栈大小
				(void *)NULL,						 //传递给任务函数的参数
				(UBaseType_t)START_TASK_PRIO,		 //任务优先级
				(TaskHandle_t *)&StartTask_Handler); //任务句柄
	vTaskStartScheduler();							 //开启任务调度
}
void start_task(void *pvParameters) {
	taskENTER_CRITICAL(); //进入临界区
	//创建软件周期定时器
	AutoReloadTimer_Handle = xTimerCreate((const char *)"AutoReloadTimer",
                                            /*  1000是定时器周期，单位时钟节拍数，可借助portTICK_PERIOD_MS将ms转为节拍数。
                                            假如定时器的周期为100个时钟节拍的话，那么xTimerPeriodInTicks 就为100，
                                            当定时器周期为 500ms 的时候 xTimerPeriodInTicks 就可以设置为(500/ portTICK_PERIOD_MS) */
										  (TickType_t)1000, 
										  (UBaseType_t)pdTRUE, // pdTRUE是周期定时器，pdFALSE是单次定时器
										  (void *)1, // 定时器ID号，能让多个定时器公用一个回调函数
										  (TimerCallbackFunction_t)AutoReloadCallback); //周期定时器，周期1s(1000个时钟节拍)，周期模式
																						//创建单次定时器
	OneShotTimer_Handle = xTimerCreate((const char *)"OneShotTimer",
									   (TickType_t)2000,
									   (UBaseType_t)pdFALSE,
									   (void *)2,
									   (TimerCallbackFunction_t)OneShotCallback); //单次定时器，周期2s(2000个时钟节拍)，单次模式
	//创建定时器控制任务
	xTaskCreate((TaskFunction_t)timercontrol_task,
				(const char *)"timercontrol_task",
				(uint16_t)TIMERCONTROL_STK_SIZE,
				(void *)NULL,
				(UBaseType_t)TIMERCONTROL_TASK_PRIO,
				(TaskHandle_t *)&TimerControlTask_Handler);
	vTaskDelete(StartTask_Handler); //删除开始任务
	taskEXIT_CRITICAL();			//退出临界区
}
// TimerControl的任务函数
void timercontrol_task(void *pvParameters) {
	u8 key, num;
	while (1)
	{
		//只有两个定时器都创建成功了才能对其进行操作
		if ((AutoReloadTimer_Handle != NULL) && (OneShotTimer_Handle != NULL))
		{
			key = KEY_Scan(0);
			switch (key)
			{
			case WKUP_PRES:								//当key_up按下的话打开周期定时器
				xTimerStart(AutoReloadTimer_Handle, 0); //开启周期定时器
				printf("开启定时器1\r\n");
				break;
			case KEY0_PRES:							 //当key0按下的话打开单次定时器
				xTimerStart(OneShotTimer_Handle, 0); //开启单次定时器
				printf("开启定时器2\r\n");
				break;
			case KEY1_PRES:							   //当key1按下话就关闭定时器
				xTimerStop(AutoReloadTimer_Handle, 0); //关闭周期定时器
				xTimerStop(OneShotTimer_Handle, 0);	   //关闭单次定时器
				printf("关闭定时器1和2\r\n");
				break;
			}
		}
		num++;
		if (num == 50) { //每500msLED0闪烁一次
			num = 0;
			LED0 = !LED0;
		}
		vTaskDelay(10); //延时10ms，也就是10个时钟节拍
	}
}
//周期定时器的回调函数
void AutoReloadCallback(TimerHandle_t xTimer) {
	static u8 tmr1_num = 0;
	tmr1_num++;												 //周期定时器执行次数加1
}
//单次定时器的回调函数
void OneShotCallback(TimerHandle_t xTimer) {
	static u8 tmr2_num = 0;
	tmr2_num++;												   //周期定时器执行次数加1
	printf("定时器2运行结束\r\n");
}
```
{% endraw %}

## 13. FreeRTOS事件标志组

使用信号量完成同步，但是使用信号量来同步的话任务只能与单个的事件或任务进行同步。有时候某个任务可能会需要与多个事件或任务进行同步，此时信号量就无能为力了。FreeRTOS 为此提供了一个可选的解决方法，那就是事件标志组。

## 14. FreeRTOS任务通知

任务通知(Task Notifictions)功能可以代替信号量、消息队列、事件标志组等，需要将`configUSE_TASK_NOTIFICATIONS`设置为1。

![image-20220218155046552](/assets/images/FreeRTOS-study/image-20220218155046552.png)

## 15. FreeRTOS低功耗模式Tickless

**1）STM32的三种低功耗模式：**![image-20220218161055480](/assets/images/FreeRTOS-study/image-20220218161055480.png)

**2）Tickless低功耗原理：**

* 处理器大量事件都在处理空闲任务，可以考虑处理空闲任务就进入低功耗模式。
* FreeRTOS系统时钟由滴答定时器提供，Tickless低功耗模式下，处理器会关闭系统节拍中断（滴答定时器中断），**有其他中断或其他任务需要处理时才会退出低功耗模式**。
* 得知下一个任务的启动时间，就可以在应用层任务里退出Tickless低功耗模式。

**3）Tickless实现：**

* 配置`configUSE_TICKLESS_IDLE`为1（`FreeRTOSConfig.h`）。
* 当系统**只有空闲任务**和低功耗模式的运行时间大于`configEXPECTED_IDLE_TIME_BEFORE_SLEEP`个时钟节拍时，系统调用`portSUPPRESS_TICKS_AND_SLEEP()`来处理低功耗相关的工作，参数是还有多长时间将有任务进入就绪态，该参数意义是低功耗模式的运行时间。**如果使用STM32板子FreeRTOS已提供该宏函数(`portmacro.h`)，自己编写的话`configUSE_TICKLESS_IDLE`需要设置为2。**

**4）其他低功耗处理：**

* 宏`configEXPECTED_IDLE_TIME_BEFORE_SLEEP`在`FreeRTOSConfig.h`中定义，在`prvIdleTask()`中使用，是低功耗模式的最短运行时间，单位是时钟节拍。

* 除了将cpu设置低功耗模式，还有其他处理：

    * 降低cpu频率；
    * 修改时钟源，外部晶振的功耗肯定比处理器内部的时钟源高；
    * 关闭其他外设时钟；
    * 关闭其他模块电源。

    上述这些处理由`configPRE_SLEEP_PROCESSING()`和`configPOST_SLEEP_PROCESSING()`这两个宏完成（在`FreeRTOSConfig.h`定义）。

{% raw %}
```c
    /********************************************************************************/ 
    /* FreeRTOS 与低功耗管理相关配置 */
    /********************************************************************************/ 
    extern void PreSleepProcessing(uint32_t ulExpectedIdleTime); 
    extern void PostSleepProcessing(uint32_t ulExpectedIdleTime);
    //进入低功耗模式前要做的处理 
    #define configPRE_SLEEP_PROCESSING PreSleepProcessing 
    //退出低功耗模式后要做的处理
    #define configPOST_SLEEP_PROCESSING PostSleepProcessing
```
{% endraw %}

    函数`PreSleepProcessing()`和`PostSleepProcessing()`在其他`C`文件中：

{% raw %}
```c
    //进入低功耗模式前需要处理的事情 
    //ulExpectedIdleTime：低功耗模式运行时间 
    void PreSleepProcessing(uint32_t ulExpectedIdleTime) {
    	//关闭某些低功耗模式下不使用的外设时钟， 
        RCC_AHB1PeriphClockCmd(RCC_AHB1Periph_GPIOB, DISABLE);
        RCC_AHB1PeriphClockCmd(RCC_AHB1Periph_GPIOC, DISABLE); 	
        RCC_AHB1PeriphClockCmd(RCC_AHB1Periph_GPIOD, DISABLE); 
        RCC_AHB1PeriphClockCmd(RCC_AHB1Periph_GPIOE, DISABLE); 
        RCC_AHB1PeriphClockCmd(RCC_AHB1Periph_GPIOF, DISABLE); 
        RCC_AHB1PeriphClockCmd(RCC_AHB1Periph_GPIOG, DISABLE); 
        RCC_AHB1PeriphClockCmd(RCC_AHB1Periph_GPIOH, DISABLE);
    }
    //退出低功耗模式以后需要处理的事情 
    //ulExpectedIdleTime：低功耗模式运行时间 
    void PostSleepProcessing(uint32_t ulExpectedIdleTime) {
    	//退出低功耗模式以后打开那些被关闭的外设时钟 
        RCC_AHB1PeriphClockCmd(RCC_AHB1Periph_GPIOB, ENABLE);
        RCC_AHB1PeriphClockCmd(RCC_AHB1Periph_GPIOC, ENABLE); 
        RCC_AHB1PeriphClockCmd(RCC_AHB1Periph_GPIOD, ENABLE); 
        RCC_AHB1PeriphClockCmd(RCC_AHB1Periph_GPIOE, ENABLE); 
        RCC_AHB1PeriphClockCmd(RCC_AHB1Periph_GPIOF, ENABLE); 
        RCC_AHB1PeriphClockCmd(RCC_AHB1Periph_GPIOG, ENABLE); 
        RCC_AHB1PeriphClockCmd(RCC_AHB1Periph_GPIOH, ENABLE);
    }
```
{% endraw %}

## 16. FreeRTOS空闲任务

空闲任务是处理器空闲的时候去运行的一个任务，当系统中没有其他就绪任务 的时候空闲任务就会开始运行，空闲任务最重要的作用就是让处理器在无事可做的时候找点事做，防止处理器无聊。

FreeRTOS调度器启动后会自动创建一个最低优先级的空闲任务。当`configIDLE_SHOULD_YIELD`为1则用户可以创建和空闲任务相同优先级的任务，并且该任务为抢占空闲任务的调度。

Hook函数（用户需要具体编写这些函数的内容）：

<img src="/assets/images/FreeRTOS-study/image-20220218165106067.png" alt="image-20220218165106067" style="zoom:67%;" />

**空闲任务Hook函数：**每个空闲任务周期都会调用空闲任务Hook函数`vApplicationIdleHook()`，该函数可以自定义，但是不能在函数内部调用任何可以阻塞空闲任务的API函数，比如`vTaskDelay()`，或者其他带有阻塞时间的信号量或队列操作函数。**可以看出相对与通用低功耗模式，FreeRTOS自带的Tickless模式更加合理有效，所以如果有低功耗设计需求的话尽量使用FreeRTOS自带的 Tickless 模式。**

例子：

{% raw %}
``` c
// FreeRTOSConfig.h
#include configUSE_TICKLESS_IDLE 0 // 关闭低功耗 tickless 模式
#include configUSE_IDLE_HOOK 1 //使能空闲任务钩子函数
// main.c
void BeforeEnterSleep(void) { //进入低功耗模式前需要处理的事情 
	//关闭某些低功耗模式下不使用的外设时钟， 
    RCC_AHB1PeriphClockCmd(RCC_AHB1Periph_GPIOB, DISABLE); 
    RCC_AHB1PeriphClockCmd(RCC_AHB1Periph_GPIOC, DISABLE); 
    RCC_AHB1PeriphClockCmd(RCC_AHB1Periph_GPIOD, DISABLE); 
    RCC_AHB1PeriphClockCmd(RCC_AHB1Periph_GPIOE, DISABLE); 
    RCC_AHB1PeriphClockCmd(RCC_AHB1Periph_GPIOF, DISABLE); 
    RCC_AHB1PeriphClockCmd(RCC_AHB1Periph_GPIOG, DISABLE); 
    RCC_AHB1PeriphClockCmd(RCC_AHB1Periph_GPIOH, DISABLE);
}
void AfterExitSleep(void) { //退出低功耗模式以后需要处理的事情 
	//退出低功耗模式以后打开那些被关闭的外设时钟 
    RCC_AHB1PeriphClockCmd(RCC_AHB1Periph_GPIOB, ENABLE); 
    RCC_AHB1PeriphClockCmd(RCC_AHB1Periph_GPIOC, ENABLE); 
    RCC_AHB1PeriphClockCmd(RCC_AHB1Periph_GPIOD, ENABLE); 
    RCC_AHB1PeriphClockCmd(RCC_AHB1Periph_GPIOE, ENABLE); 
    RCC_AHB1PeriphClockCmd(RCC_AHB1Periph_GPIOF, ENABLE); 
    RCC_AHB1PeriphClockCmd(RCC_AHB1Periph_GPIOG, ENABLE); 
    RCC_AHB1PeriphClockCmd(RCC_AHB1Periph_GPIOH, ENABLE);
}
void vApplicationIdleHook(void) { //空闲任务钩子函数
    __disable_irq();
    __dsb(portSY_FULL_READ_WRITE);
    __isb(portSY_FULL_READ_WRITE); 
    BeforeEnterSleep(); //进入睡眠模式之前需要处理的事情
    __wfi(); // 调用WFI指令使STM32F407进入睡眠模式
    AfterExitSleep(); //退出睡眠模式之后需要处理的事情
    __dsb(portSY_FULL_READ_WRITE); 
    __isb(portSY_FULL_READ_WRITE); 
    __enable_irq();
}
```
{% endraw %}

## 17. FreeRTOS内存管理

内存管理是一个系统基本组成部分，FreeRTOS 中大量使用到了内存管理，比如**创建任务、 信号量、队列**等会自动从堆中申请内存。用户应用层代码也可以 FreeRTOS 提供的内存管理函数来申请和释放内存。

FreeRTOS中的内存堆为`ucHeap[]`，大小为`configTOTAL_HEAP_SIZE`，`FreeRTOSConfig.h`的`configAPPLICATION_ALLOCATED_HEAP`为1时用户自行定义内存堆（可以定义到外部的`SRAM`或`SDRAM`中）。使用`xPortGetFreeHeapSize()`可以获取内存堆中剩余内存的大小。

标准C库中的`malloc()`和`free()`可实现动态内存管理，但有缺点，FreeRTOS用`pvPortMalloc()`和`vPortFree()`代替：

<img src="/assets/images/FreeRTOS-study/image-20220218171654016.png" alt="image-20220218171654016" style="zoom: 67%;" />

**FreeRTOS各种内存分配方法特点：**

1. `heap_1`：没有`free`，直接再原有的基础上对齐累加。不花里胡哨，**适合小型的不需要释放存储空间的代码。**
2. `heap_2`：有一个**链表结构体**，会引起内存碎片，但相比于`heap1`多了`free`函数，是会自动释放之前申请的过大内存块。
3. `heap_3`：只是对标准`C`库中的`malloc`和`free`进行封装，做了线性保护，系统的内存堆由编译器提供，不是`ucHeap[]`。大小由`.s`启动文件中的**`Heap_Size`的堆大小**决定，`configTOTAL_HEAP_SIZE`没用。
4. `heap_4`：比`heap2`多了**处理内存碎片**，还会把地址**连续的内存块合并**起来。查找空闲插入点，检查要插入的内存块是否可以和前一个内存块合并。
5. `heap_5`：可以跨越不同的存储单元，**把不同物理单元中不连续内存段整合成一个连续的映射内存**，再像`heap4`的一样处理，`heap4`的只能在同一个物理单元中实现。STM32 的内部 RAM 可以作为内存堆，但是 STM32 内部RAM比较小，遇到那些需要大容量RAM的应用就不行了，如音视频处理。不过 STM32 可以外接 SRAM 甚至大容量的 SDRAM，如果使用`heap_4`的话就只能在内部 RAM 和外部 SRAM 或 SDRAM 之间二选一了，使用`heap_5`的话就不存在这个问题，两个都可以一起作为内存堆来用。需要先调用函数 `vPortDefineHeapRegions()`来对内存堆做初始化处理。

**用法：**

{% raw %}
```c
u8 *buffer;
buffer = pvPortMalloc(30); // 申请30个字节
vPortFree(buffer); // 释放内存
buffer = NULL;
```
{% endraw %}



