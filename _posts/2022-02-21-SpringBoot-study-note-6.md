---
layout: post
category: [SprintBoot教程笔记]
tag: [SpringBoot, 学习笔记] 
title: 四、Web开发（Spring Boot教程笔记6）
---
{% raw %}

# 四、Web开发

SpringBoot开发步骤：

1. 创建SpringBoot应用，选中我们需要的模块
2. 在配置文件中指定少量的配置
3. 自己编写业务代码

**需要考虑：这个场景SpringBoot帮我们配置了什么？能不能修改？能修改哪些配置？能不能拓展？**

清楚两个点：

```shell
1. xxxxAutoConfiguration:帮我们给容器中自动配置了组件
2. xxxxProperties：封装了配置文件的配置类
```

## 1.SpringBoot对静态资源的映射规则

1. 所有的静态资源资源都以jar包的形式存在，都在`/webjars/`下面，而`/webjars/**`，都去`classpath:/META-INF/resources/webjars/`找资源。`webjars`：以jar包的形式引入静态资源。参考：[webjar网址](https://www.webjars.org/),所以，加入要引入`jquery.js`这个静态资源，只需在`webjar`这个网址查找对应的依赖，加入`pom.xml`即可。

   在`pom.xml`中添加依赖：

   ```xml
   <!--引入jquery-->
   <dependency>
       <groupId>org.webjars</groupId>
       <artifactId>jquery</artifactId>
       <version>3.3.1</version>
   </dependency>
   ```

2. 静态资源文件夹：

   ```java
   classpath:/META-INF/resources/
   classpath:/resources/
   classpath:/static/
   classpath:/public/
   ```

   可以用`localhost:8080/static_file`访问静态资源文件，首先这个静态资源文件是放在上面四个地方其中一个的。`resources`就是`classpath`：![2018-08-08_222440](/assets/images/spring-boot-develop/2018-08-08_222440.png)

   在类路径的`static`文件夹下放了自定义的`javascrpt.js`文件：![2018-08-08_222623](/assets/images/spring-boot-develop/2018-08-08_222623.png)

   启动项目，可以用`localhost:8080/javascript.js`访问到该文件，因为系统会扫描上述的的静态资源文件夹，如果有`javascript.js`的话，就返回。

3. 首页：静态资源文件夹下的所有`index.html`页面,都被`/**`映射。也就是，访问`/`，譬如：`localhost:8080`，系统会自动搜索类路径的静态资源文件夹下的`index.html`当成它的首页。

4. 自定义图标：将图标命名为`favicon.ico`放在上述静态资源文件夹即可。

5. 更改静态资源文件夹：

   ```properties
   # application.properties
   spring.resources.static-locations=classpath:/hello/,classpath:/com/
   # 这是个数组，这样配置后classpath:/hello/和classpath:/com/就成了新的静态资源文件夹
   ```

## 2.模板引擎

JSP、Velocity、Freemarker、Thymeleaf。

模板引擎原理：

![2018-08-08_233950](/assets/images/spring-boot-develop/2018-08-08_233950.png)

SpringBoot推荐使用Thymeleaf模板引擎。

### 1.引入Thymeleaf

在`pom.xml`中添加依赖：

```xml
<dependency>
	<groupId>org.springframework.boot</groupId>
	<artifactId>spring-boot-starter-thymeleaf</artifactId>
</dependency>
```

默认引入的Thymeleaf版本是2.1.6，如果想用最新版的Thymeleaf，需在`pom.xml`中添加`property`：

```xml
<properties>
    <thymeleaf.version>3.0.9.RELEASE</thymeleaf.version> <!--Thymeleaf主程序-->
    <thymeleaf-layout-dialect.version>2.2.2</thymeleaf-layout-dialect.version> <!--布局功能-->
</properties>
```

`Thymeleaf3`对应`layout2`,`Thymeleaf2`对应`layout1`。

`pom.xml`样子：

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
	xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
	<modelVersion>4.0.0</modelVersion>

	<groupId>com.jimcom</groupId>
	<artifactId>spring-boot-01-web-restfulcrud</artifactId>
	<version>0.0.1-SNAPSHOT</version>
	<packaging>jar</packaging>

	<name>spring-boot-01-web-restfulcrud</name>
	<description>Demo project for Spring Boot</description>

	<parent>
		<groupId>org.springframework.boot</groupId>
		<artifactId>spring-boot-starter-parent</artifactId>
		<version>2.0.4.RELEASE</version>
		<relativePath/> <!-- lookup parent from repository -->
	</parent>

	<properties>
		<project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
		<project.reporting.outputEncoding>UTF-8</project.reporting.outputEncoding>
		<java.version>1.8</java.version>
		<thymeleaf.version>3.0.9.RELEASE</thymeleaf.version>
		<thymeleaf-layout-dialect.version>2.2.2</thymeleaf-layout-dialect.version>
	</properties>

	<dependencies>
		<dependency>
			<groupId>org.springframework.boot</groupId>
			<artifactId>spring-boot-starter-web</artifactId>
		</dependency>

		<dependency>
			<groupId>org.springframework.boot</groupId>
			<artifactId>spring-boot-starter-test</artifactId>
			<scope>test</scope>
		</dependency>

		<!--引入jquery-->
		<dependency>
			<groupId>org.webjars</groupId>
			<artifactId>jquery</artifactId>
			<version>3.3.1</version>
		</dependency>

		<dependency>
			<groupId>org.springframework.boot</groupId>
			<artifactId>spring-boot-starter-thymeleaf</artifactId>
		</dependency>
	</dependencies>

	<build>
		<plugins>
			<plugin>
				<groupId>org.springframework.boot</groupId>
				<artifactId>spring-boot-maven-plugin</artifactId>
			</plugin>
		</plugins>
	</build>
</project>
```

### 2.Thymeleaf的使用和语法

Thymeleaf的默认规则都在`ThymeleafPropertiese`这个里面封装着。

```java
@ConfigurationProperties(prefix = "spring.thymeleaf")
public class ThymeleafProperties {

	private static final Charset DEFAULT_ENCODING = StandardCharsets.UTF_8;

	public static final String DEFAULT_PREFIX = "classpath:/templates/";
	// 只要将HTML页面放在classpath:/templates/,Thymeleaf就会自动渲染
	public static final String DEFAULT_SUFFIX = ".html";
```

`Thymeleaf`语法具体看[Thymeleaf官网](https://www.thymeleaf.org/)。

#### 1.使用

导入`thymeleaf`的名称空间：`xmlns:th="http://www.thymeleaf.org"`。

```html
// classpath:/templates/success.html
<!DOCTYPE html>
<html lang="en" xmlns:th="http://www.thymeleaf.org">
<head>
    <meta charset="UTF-8">
    <title>success</title>
</head>
<body>
    <!--th:text 将div里面的文本信息设置为传入的信息-->
    <div th:text="${hello}">
        这是欢迎信息。
    </div>
</body>
</html>
```

控制器：

```java
// com.jimcom.springboot.controller.HelloController.java
package com.jimcom.springboot.controller;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.ResponseBody;

import java.util.Map;

@Controller
public class HelloController {

    @ResponseBody
    @RequestMapping("/hello")
    public String hello() {
        return "Hello World";
    }

    @RequestMapping("/success")
    public String success(Map<String, Object> map) {
        map.put("hello", "你好");
        return "success";
    }
}
```

#### 2.语法规则

1. th:text 改变当前元素里面 文本内容

   th:attr attr代表任意html属性，可来替换原先属性的值

解析优先级：

![2018-08-09_115536](/assets/images/spring-boot-develop/2018-08-09_115536.png)

1. 表达式

```properties
Simple expressions:
    Variable Expressions: ${...}：获取变量值，OGNL
    	1. 获取对象的属性、调用方法
    	2. 使用内置的基本对象：
    		#ctx: the context object.
			#vars: the context variables.
			#locale: the context locale.
			#request: (only in Web Contexts) the HttpServletRequest object.
			#response: (only in Web Contexts) the HttpServletResponse object.
			#session: (only in Web Contexts) the HttpSession object.
			#servletContext: (only in Web Contexts) the ServletContext object.
		3. 使用内置的工具对象：
			#execInfo: information about the template being processed.
			#messages: methods for obtaining externalized messages inside variables expressions, in the same way as they would be obtained using #{…} syntax.
			#uris: methods for escaping parts of URLs/URIs
			#conversions: methods for executing the configured conversion service (if any).
			#dates: methods for java.util.Date objects: formatting, component extraction, etc.
			#calendars: analogous to #dates, but for java.util.Calendar objects.
			#numbers: methods for formatting numeric objects.
			#strings: methods for String objects: contains, startsWith, prepending/appending, etc.
			#objects: methods for objects in general.
			#bools: methods for boolean evaluation.
			#arrays: methods for arrays.
			#lists: methods for lists.
			#sets: methods for sets.
			#maps: methods for maps.
			#aggregates: methods for creating aggregates on arrays or collections.
			#ids: methods for dealing with id attributes that might be repeated (for example, as a result of an iteration).
    Selection Variable Expressions: *{...}：选择表达式，和${}功能上一样
    	补充：配合 th:object=进行使用
    	  <div th:object="${session.user}">
              <p>Name: <span th:text="*{firstName}">Sebastian</span>.</p>
              <p>Surname: <span th:text="*{lastName}">Pepper</span>.</p>
              <p>Nationality: <span th:text="*{nationality}">Saturn</span>.</p>
          </div> <!--*代表前面的th:object-->
    Message Expressions: #{...}：获取国际化内容
    Link URL Expressions: @{...}：定义url链接
    	@{/order/process(execId=${execId},execType='FAST')}
    Fragment Expressions: ~{...}：片段引用表达式
    	<div th:insert="~{commons :: main}">...</div>
    	
Literals:字面量
    Text literals: 'one text', 'Another one!',…
    Number literals: 0, 34, 3.0, 12.3,…
    Boolean literals: true, false
    Null literal: null
    Literal tokens: one, sometext, main,…
Text operations:文本操作
    String concatenation: +
    Literal substitutions: |The name is ${name}|
Arithmetic operations:数学运算
    Binary operators: +, -, *, /, %
    Minus sign (unary operator): -
Boolean operations:布尔运算
    Binary operators: and, or
    Boolean negation (unary operator): !, not
Comparisons and equality:比较运算
    Comparators: >, <, >=, <= (gt, lt, ge, le)
    Equality operators: ==, != (eq, ne)
Conditional operators:条件运算，三元运算符
    If-then: (if) ? (then)
    If-then-else: (if) ? (then) : (else)
    Default: (value) ?: (defaultvalue)
Special tokens:特殊操作
	No-Operation: _ 没有操作
```

例子：

控制器：往视图里传入值：hello, users。

```java
@Controller
public class HelloController {
    @RequestMapping("/success")
    public String success(Map<String, Object> map) {
        map.put("hello", "你好");
        map.put("users", Arrays.asList("a", "b", "c"));
        return "success";
    }
}
```

success.html：使用传进来的值。

```html
<!DOCTYPE html>
<html lang="en" xmlns:th="http://www.thymeleaf.org">
<head>
    <meta charset="UTF-8">
    <title>success</title>
</head>
<body>

<!--每次遍历都会生成当前这个标签，遍历传进来的users，每次遍历取得的值是user-->
<h1 th:th="${user}" th:each="user:${users}"></h1>

<h1> <!--[[...]]是行内写法，还有[()]。[[]]转义，[()]不转义-->
    <span th:each="user:${users}">[[${user}]]</span>
</h1>
</body>
</html>
```

{% endraw %}  