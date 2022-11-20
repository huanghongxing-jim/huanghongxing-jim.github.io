---
layout: post
category: [SprintBoot教程笔记]
tag: [SpringBoot, 学习笔记] 
title: 四、Web开发（Spring Boot教程笔记7）
---
{% raw %}

## 4.SpringBootMVC自动配置原理

查看[官网](https://docs.spring.io/spring-boot/docs/1.5.10.RELEASE/reference/htmlsingle/):

Spring Boot自动配置好了SpringMVC，以下是SpringBoot对Spring的默认配置：

- Inclusion of `ContentNegotiatingViewResolver` and `BeanNameViewResolver` beans.
  - 自动配置好了`ViewResolver`（视图解析器：根据方法的返回值得到视图对象（View），视图对象觉得如何渲染（渲染：转发或者重定向）。
  - `ContentNegotiatingViewResolver`：在SpringMVC中组合所有的视图解析器。
  - 因为`ContentNegotiatingViewResolver`会在SpringMVC中组合所有的视图解析器，所以定制时只需要给容器中添加一个视图解析器即可，SpringMVC会自动将其组合进来。
- 支持静态资源文件夹和webjars
- 支持静态首页访问
- 支持`favicon.ico`
- 自动注册了`Converter`, `GenericConverter`, `Formatter` 组件
  - `Converter`：转换器：转换类型
  - `Formatter`：格式化器，譬如，将”2017.02.10“或者"2014/2/1"都格式化为Date
  - 可以在配置文件中配置日期格式化的规则：`spring.mvc.date-format`
  - 自己添加的格式化器或者转换器放在容器中即可生效

- 支持 `HttpMessageConverters` .
  -  `HttpMessageConverters` ：消息转化器，SpringMVC用来转化HTTP请求和响应的
  -  `HttpMessageConverters` 是自己从容器中确定的，获取所有的 `HttpMessageConverter` 
  - 自己给容器中添加 `HttpMessageConverter` ，只需将自己的组件注册进容器即可（通过`@Bean`或者`@Compent`）
- 自动注册 `MessageCodesResolver` ==>定义错误代码生成规则的
- Automatic use of a `ConfigurableWebBindingInitializer` bean.
  - 我们可以配置一个`ConfigurableWebBindingInitializer` 来替换默认的，只需将我们制作的`ConfigurableWebBindingInitializer` 添加到容器中即可
  - `ConfigurableWebBindingInitializer` 作用：初始化`WebDateBinder`,`WebDateBinder`可以将请求数据和`JavaBean`进行绑定

web的所有场景：`org.springframework.boot.autoconfigure.web`。

扩展SprintMVC：

​	编写一个配置类（有`@Configuration`），是`WebMvcConfigurerAdapter`类型，不能有`@EnableWebMvc`注解:

```java
// /src/java/com.jimcom.springboot/config/MyConfig.java
package com.jimcom.springboot.config;

import org.springframework.context.annotation.Configuration;
import org.springframework.web.servlet.config.annotation.ViewControllerRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurerAdapter;

@Configuration
public class MyConfig extends WebMvcConfigurerAdapter {
    // 在IDEA中可以先Ctrl+O查看可以重写哪些方法，即可添加哪些配置
    @Override
    public void addViewControllers(ViewControllerRegistry registry) {
//        super.addViewControllers(registry);
        // 浏览器发送/jim请求，请求来到success页面
        registry.addViewController("/jim").setViewName("success");
    }
}
```

​	位置：

![1534078641011](/assets/images/spring-boot-develop/1534078641011.png)

​	原理：

**`WebMvcAutoConfiguration`是SpringMVC的自动配置类，在做其他自动导入时候会导入`@EnableWebMvcConfiguration.class`，这个能将容器中所有的`WebMvcConfigurer`的相关配置一起起作用。**

 ***在配置类中添加`@EnableWebMvc`就能全面接管SpringMVC：SpringBoot对SpringMVC的自动配置都失效了，所有的都是自己配的。***

## 5.修改SpringBoot的默认配置

1. SpringBoot在自动配置很多组件的时候，先看容器中有没有用户自己配置（`@Bean`，`@Component`），如果有就用用户自己配置的，如果没有，才自动配置，如果有些组件可以有多个（譬如`ViewResolver`），就将用户配置的和自己默认的组合起来。
2. 在SprintBoot中有非常多的`xxxConfigurer`帮助我们进行扩展配置。

{% endraw %}  