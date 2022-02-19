---
layout: post
title: Spring Boot教程笔记--一、Spring Boot入门
---
# 一、Spring Boot入门

## 1. Spring Boot简介

>简化Spring应用开发的一个框架；
>
>整个Spring技术栈的一个大整合；
>
>J2EE开发的一站式解决方案；

## 2.微服务

2014， Martin Fowler提出（论文形式）

微服务：架构风格（服务微化）  

一个应用应该是一组小型服务；可以通过HTTP的方式互通；  
单体应用：all in one  
微服务：每一个功能元素最终都是一个可独立替换和独立升级的软件单元。  

1. 学习Spring Boot的基础：  
  * Spring框架的使用经验（Spring4）
  * 熟练使用Maven进行项目构建和依赖管理  
  * 熟练使用Eclipse或者IDEA  
2. 学习环境：
  * jdk1.8
  * Maven 3.x
  * IDEA2017
  * Spring Boot 1.5.9.RELEASE  

## 3.快速入手开发

### 1.IDEA创建Maven项目

![1532068956252](/assets/images/spring-boot-develop/1532068956252.png)

### 2.在项目根目录中的pom.xml中写入以下代码（告诉Maven添加什么依赖）

```xml
    <parent>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-parent</artifactId>
        <version>1.5.9.RELEASE</version>
    </parent>

    <dependencies>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
        </dependency>

        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-tomcat</artifactId>
        </dependency>
    </dependencies>
```

![1532069222354](/assets/images/spring-boot-develop/1532069222354.png)

### 3.在src.main.java中添加包：com.jim.controller

```java
// 路径：/src/main/java.com.jim.controller.HelloCtroller.java

package com.jim.controller;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.ResponseBody;

@Controller
public class HelloController {
    @ResponseBody
    @RequestMapping("/hello")
    public String hello() {
        return "Hello World!";
    }
   
```

```java
//路径： /src/main/java/com.jim/HelloWorldMainApplication.java

package com.jim;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

/**
 * @SpringBOotApplication 来标注一个主程序类，说明这是一个Spring Boot应用
 */
@SpringBootApplication
public class HelloWorldMainApplication {
    public static void main(String[] args) {
        // Spring Boot启动起来
        SpringApplication.run(HelloWorldMainApplication.class, args);
    }
}
```

![1532069406540](/assets/images/spring-boot-develop/1532069406540.png)

***确认Tomato 端口没有被占用（在cmd中）：***

```vim
- netstat -ano | findstr "8080" # 查看8080端口，发现进程号3548占用
- tasklist | findstr "3548" # 查看进程号3548对应a进程
- taskkill /f /t /im a.exe # 关闭a进程
```

### 4.直接运行HelloWorldMainApplication中的Main函数

![1532069845274](/assets/images/spring-boot-develop/1532069845274.png)

## 4.部署（超级简单）

### 1.添加这个插件到pom.xml中：

```xml
    <!--这个插件，可将应用打包成一个可执行的jar包-->
    <build>
        <plugins>
            <plugin>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-maven-plugin</artifactId>
            </plugin>
        </plugins>
    </build>
```

![1532071766467](/assets/images/spring-boot-develop/1532071766467.png)

### 2.打包![1532071923753](/assets/images/spring-boot-develop/1532071923753.png)

### 3.查看打包位置

![1532072029278](/assets/images/spring-boot-develop/1532072029278.png)

### 4.打开该jar所在文件夹，里面的这个jar就可以用来部署了

```vim
java -jar *.jar # 在部署的服务器上启动jar包，即启动该应用的命令
```

![1532072232356](/assets/images/spring-boot-develop/1532072232356.png)

***该应用自带Tomato，故不要求服务器一定要装Tomato。***

##  5.Hello World探究

### 1.POM文件

#### 1.父项目

```xml
    <parent>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-parent</artifactId>
        <version>1.5.9.RELEASE</version>
    </parent>
```

这个的**父项目**是Spring Boot的版本仲裁中心，里面定义了各个场景的**版本号**，所以我们导入依赖默认是不需要写版本的（没有在其**父项目**的dependencies里面管理的依赖自然需要声明版本号）。

#### 2.导入的依赖

```xml
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
        </dependency>
```

**spring-boot-starter**-web : 

* spring-boot-starter : spring-boot场景启动器，帮我们导入了web模块正常运行所依赖的组件。
* web： Spring-boot的一个功能场景。

**要用什么功能就导入什么样的场景启动器**：***Spring Boot将所有的功能场景都抽取出来，做成一个个的starters（启动器），只需要在项目里面引入这些starters相关场景（譬如：spring-boot-starters-web，导入web启动器场景)，所有依赖都会自己跟过来。***

[Spring Boot v1.5.9的各类场景启动器](https://docs.spring.io/spring-boot/docs/1.5.9.RELEASE/reference/htmlsingle/#using-boot-starter)

### 2. 主程序类，主入口

```java
/**
 * @SpringBOotApplication 来标注一个主程序类，说明这是一个Spring Boot应用
 */
@SpringBootApplication
public class HelloWorldMainApplication {
    public static void main(String[] args) {
        // Spring Boot启动起来
        SpringApplication.run(HelloWorldMainApplication.class, args);
    }
}
```

**@SpringBootApplication:** Spring Boot 应用标注在某个类上说明这个类是Spring Boot的主配置类，Spring Boot就应该运行这个类的main方法来启动Spring Boot应用。

进一步查看知道，@SpringBootApplication也是由很多组件构成的。

```java
// 这是SpringBootApplication这个类的开头注解
@Target(ElementType.TYPE)
@Retention(RetentionPolicy.RUNTIME)
@Documented
@Inherited
@SpringBootConfiguration
@EnableAutoConfiguration
@ComponentScan(excludeFilters = {
    @Filter(type = FilterType.CUSTOM, classes = TypeExcludeFilter.class),
    @Filter(type = FilterType.CUSTOM, classes = AutoConfigurationExcludeFilter.class) })
public @interface SpringBootApplication {
```

* **@SpringBootConfiguration**  

   @SpringBootConfiguration是SpringBoot的配置类，标注在某个类上，表示这是一个Spring Boot的配置类。  

  @Configuration标注在某个类上，表示这是个Spring的配置类（底层）。  

  配置类 == 配置文件，配置类也是容器中的一个组件（@Component）。

* **@EnableAutoConfiguration**

  开启自动配置功能（以前需要我们配置的东西，现在开启这个，Spring Boot就会帮我们自动配置）。

  原理：

  ```java
  // @EnableAutoConfiguration的注解
  @AutoConfigurationPackage
  @Import(EnableAutoConfigurationImportSelector.class)
  public @interface EnableAutoConfiguration {
  ```

   1. @AutoConfigurationPackage：自动配置包 。  

      原理：

      ```java
      @Import(AutoConfigurationPackages.Registrar.class)
      public @interface AutoConfigurationPackage {
      ```

      ***@AutoConfigurationPackage利用@Import指定Register给容器中导入了一些组件。***这些组件就是主配置类（@SpringBootApplication标注的类）的所在包及下面所有子包里面的所有组件，@AutoConfigurationPackage都将其扫描到Spring容器中。  

      2. @Import(EnableAutoConfigurationImportSelector.class)：组件选择器。

         ***将所有需要导入的组件以全类名的方式返回，这些组件会被添加到容器中。***

         ***结果就是会给容器中导入非常多的自动配置类（XXXAutoConfiguration），就是给容器导入这个场景需要的所欲组件，并配置好这些组件。***

  

  ***Spring Boot在启动的时候从类路径下的META-INF/Spring.factories中获取EnableAutoConfigutation制定的值，将这些值作为自动配置类导入到容器中，自动配置类就生效了，帮我们进行自动配置工作。***

  J2EE的整体整合解决方案和自动配置都在spring-boot-autoconfigure-1.5.9.RELEASE.jar这个jar包中。

**注**：

* groupId：是你公司的名称，譬如，com.jimCom

* artififactId：是项目在你公司里的唯一标识号，譬如，spring-boot-project-01

* project name：是给人看的项目名字，譬如，spring-boot-hello-world

  (*包名一般是grouId+artifactId：com.jimCom.spring-boot-project-01*)

## 6.Spring Boot应用

```java
// com.jim.controller.HelloCotroller.java

@ResponseBody // 写在这里表明这个类的所有方法返回的数据直接写给浏览器(如果是对象转为json数据)
@Controller
public class HelloCotroller {
    @RequestMapping("/hello")
    public String hello() {
        return "Hello World!";
    }
}
```

* @ResponseBody + @Controller == @RestController 
* 使用Spring Initializer快速创建Spring Boot项目（一定要联网）
  * resources文件夹中的 目录结构：
    * static：保存所有静态资源，js， css， images；
    * templates：保存所有的模板页面，默认是jar包方式（里面有嵌入式的Tomato，默认不支持jsp页面，但是可以使用模板引擎：freemarker、thymeleaf）；
    * application.properties：Spring Boot的配置文件。虽说Spring Boot的所有都是自动配置的，但是自己可以通过这里来改动Spring Boot的默认配置。
  * ecplise中创建的方式是：File -> New -> Spring Starter Project 或者 File -> new -> Other -> Spring Starter Project。
