---
layout: post
category: [SprintBoot教程笔记]
tag: [SpringBoot, 学习笔记] 
title: 一、Spring Boot入门（Spring Boot教程笔记1）
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

{% raw %}
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
{% endraw %}

![1532069222354](/assets/images/spring-boot-develop/1532069222354.png)

### 3.在src.main.java中添加包：com.jim.controller

{% raw %}
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
{% endraw %}

{% raw %}
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
{% endraw %}

![1532069406540](/assets/images/spring-boot-develop/1532069406540.png)

***确认Tomato 端口没有被占用（在cmd中）：***

{% raw %}
```vim
- netstat -ano | findstr "8080" # 查看8080端口，发现进程号3548占用
- tasklist | findstr "3548" # 查看进程号3548对应a进程
- taskkill /f /t /im a.exe # 关闭a进程
```
{% endraw %}

### 4.直接运行HelloWorldMainApplication中的Main函数

![1532069845274](/assets/images/spring-boot-develop/1532069845274.png)

## 4.部署（超级简单）

### 1.添加这个插件到pom.xml中：

{% raw %}
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
{% endraw %}

![1532071766467](/assets/images/spring-boot-develop/1532071766467.png)

### 2.打包![1532071923753](/assets/images/spring-boot-develop/1532071923753.png)

### 3.查看打包位置

![1532072029278](/assets/images/spring-boot-develop/1532072029278.png)

### 4.打开该jar所在文件夹，里面的这个jar就可以用来部署了

{% raw %}
```vim
java -jar *.jar # 在部署的服务器上启动jar包，即启动该应用的命令
```
{% endraw %}

![1532072232356](/assets/images/spring-boot-develop/1532072232356.png)

***该应用自带Tomato，故不要求服务器一定要装Tomato。***


