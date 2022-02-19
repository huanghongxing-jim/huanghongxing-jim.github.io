---
layout: post
title: Spring Boot教程笔记--三、SpringBoot日志
---
# 三.SpringBoot日志

## 1.日志框架

JUL, JCL, Jboss-logging, logback, log4j, log4j2, slf4j...

日志门面：日志抽象层。**给项目中导入具体的日志实现就行了，日志框架是抽象层的实现。**

| 日志门面                  | 日志实现                    |
| ------------------------- | --------------------------- |
| JCL, SLF4j, jboss-logging | Log4j, JUl, Log4j2, Logback |

**左边选一个门面（抽象层），右边选一个来实现。**

日志门面：SLF4j, 日志实现：Logback。

SpringBoot:底层是Spring框架，Spring框架默认是用JCL。**SpringBoot选用SLF4j, Logback。**

## 2.SLF4j使用

### 1.系统中使用SLF4j

日志记录方法的调用，不应该直接调用日志的实现类，而是调用日志抽象层里面的方法。

```java
// slf4j的使用方法：给系统导入slf4j的抽象jar和logback的实现jar
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class Temp {
    public static void main(String[] args) {
        Logger logger = LoggerFactory.getLogger(Temp.class);
        logger.info("Temp");
    }
}
```

**注：IDEA中“public static void main(String[] args) {}”快捷键：“psvm”。**

官网的slf4j的使用图例：

![concrete-bindings](/assets/images/spring-boot-develop/concrete-bindings.png)

每一个日志的实现框架都有自己的配置文件。使用slf4j后，配置文件还是做成日志实现框架即Logback自己的配置文件。

### 3.项目里也会用到其他的日志框架

一个项目里可能也会用其他的框架，譬如，Hibernate, MyBatis等，这些框架也可能会用自己的日志框架，所以我们得统一我们项目的日志框架，统一用slf4j+logback输出日!志。

![legacy](/assets/images/spring-boot-develop/legacy.png)

**统一项目的日志框架步骤：**

1. **将系统中其他的日志框架删去 ；**
2. **用中间包替换原来的日志框架；**
3. **导入slf4j和其他的实现框架。**

例子：

![2018-08-03_111757](/assets/images/spring-boot-develop/2018-08-03_111757.png)

项目中也有Commons logging, log4j, java.util.logging这三个日志框架，我们要统一用slf4j这个日志框架的话，得用jcl-over-slf4j.jar, log4j-over-slf4j.jar, jul-to-slf4j.jar分别替换Commons logging, log4j, java.util.logging这三个jar包。

以流程图形式查看依赖：

首先，确认有安装bpm插件:![install-bpm](./images/install-bpm.png)

然后在.xml文件里右键，Diagrams --> show Dependencies就能以流程图形式呈现项目中各个类的依赖关系。

## 3.SpringBoot日志关系

SpringBoot使用logging场景启动器做日志功能：

```xml
		<dependency>
			<groupId>org.springframework.boot</groupId>
			<artifactId>spring-boot-starter-logging</artifactId>
		</dependency>
```

logging场景启动器的依赖关系：

![2018-08-03_131338.png](/assets/images/spring-boot-develop/2018-08-03_131338.png)

starter-logging依赖logback-classic(logback-classsic还依赖logback-core，使用logback记录日志), jul-to-slf4j, log4j-over-slf4j, jcl-over-slf4j这三个依赖slf4j-api（导入了日志抽象层slf4j）。

**注：**

1. **SpringBoot底层也是使用了slf4j+logback的方式进行日志记录。**
2. **SpringBoot也把其他的日志都替换成了slf4j。**
3. **中间的替换包的包名和原先被替换掉的jar包的包名一样，可是里面用到的确实slf4j的东西。**

***如果我们要引入其他框架，一定要把这个框架的默认日志依赖移除掉。***

***SpringBoot能自动适配所有的日志，底层使用的是slf4j+logback的方式记录日志。也就是说，引入其他框架的时候，只需要把这个框架依赖的日志框架排除掉即可，SpringBoot会自动将这个框架的日志框架转成和slf4j+logback适配的方式。***

## 4.日志使用

### 1.默认配置

SpringB默认帮我们配置好了日志，所以我们直接使用就行：

```java
	// 1.声明一个log记录器logger
	Logger logger = LoggerFactory.getLogger(getClass());
	@Test
	public void contextLoads() { // 2.使用日志
		logger.trace("..."); // trace日志，输出跟踪信息
		logger.debug("..."); // debug日志，调试
		logger.info("..."); // info日志，自定义信息
		logger.warn("..."); // warn日志，警告
		logger.error("..."); // error日志，错误
	}
```

日志级别：tarce < debug< info < warn < error。我们可以调整输出的日志级别，调整好，日志就只会输出该级别和更高级别的日志信息。SpringBoot默认设置的是info级别。

将com.example包里的程序日志级别都调到trace，其他包没有指定级别的默认采用info级别：

```properties
# applicaion.properties
logging.level.com.example=trace
```

logging.path和logging.file:

```properties
# application.properties
# 没有指定路径，所以logging.file=springboot.log在当前项目下产生springboot.log日志
logging.file=springboot.log 
# 或者
# 指定了完整路径
logging.file=G:/springboot.log
```

**logging.path和logging.file不能同时使用。**

```properties
# application.properties
# 在当前磁盘根目录路径下创建spring/log/文件夹，在文件夹中使用spring.log作为日志文件
logging.path=/spring/log
```

规定格式：

```properties
# application.properties
# 在控制台中输出的日志格式
logging.pattern.console=%d{yyyy-MM-dd} [%thread] %-5level %logger{50} - %msg%n
# 在指定文件中日志输出的格式
logging.pattern.file=%d{yyyy-MM-dd} === [%thread] ====%-5level === %logger{50} === %msg%n
```

![2018-08-03_140534.png](/assets/images/spring-boot-develop/2018-08-03_140534.png)

### 2.指定配置

在类路径下放上每个日志框架自己的配置文件即可，SpringBoot就自动忽略默认配置而加载自定义的配置文件：

![2018-08-08_210011](/assets/images/spring-boot-develop/2018-08-08_210011.png)

loback.xml是自定义的日志框架的配置文件，直接放在类路径下就会自动生效。

![2018-08-08_205513](/assets/images/spring-boot-develop/2018-08-08_205513.png)

如果我们的日志框架是`Logbakc`,那么它自定义的配置文件名应为`logback-spring.xml`，`logback-spring.groovy`, `logback.xml`或者`logback.groovy`等，其余的类似。

SpringBoot推荐带有`-spring`的配置文件，譬如，推荐使用`logback-spring.xml`而不是`logback.xml`。如果使用`logback.xml`,那就会直接被日志框架识别了，而使用`logback-spring.xml`，日志框架不直接加载日志的配置项，而由SpringBoot解析日志配置，这样，我们能在该配置文件使用一些SpringBoot的高级springProfile功能：

```xml
<springProfile name="staging">
	<!--这个配置可以指定某段配置只在某个环境生效-->
</springProfile>
```

而如果不加`-spring`而直接使用`<springProfile></springProfile>`的话就会报错。

## 5.切换日志框架

譬如要将现在的日志框架切换为`log4j2`，只需要在原先的的pom.xml排除掉`logging`的`starter`,换为`log4j2`的`starter`即可。

同理，切换日志框架只需在`pom.xml`里更换依赖即可，注意如果原先有自定义的配置文件，需将它移除，再写切换后的日志框架对应的配置文件。