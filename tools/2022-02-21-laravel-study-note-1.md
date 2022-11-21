---
layout: post
category: [SprintBoot教程笔记]
tag: [SpringBoot, 学习笔记] 
title: 二、配置文件（Spring Boot教程笔记3）
---
{% raw %}

# 二、配置文件

## 1、配置文件

全局配置文件（/src/main/resources/）：

* application.properties

* application.yml

  ***YAML:和json和xml一样的配置文件，但比他们更合适做配置文件。***

  ```yml
  # 例子:
  server:
    port: 8081
  ```

## 2、YAML 语法

### 1.基本语法

key:(空格)value：表示一对键值对（一定要有空格）。

以**空格** 的缩进来控制层级关系，左对齐的一列数据都是同一层级的。

属性和值都是大小写敏感的。

```yml
server:
  port: 8081
  path: /hello
```

### 2.值的写法

* #### 字面量：

  ***字符串默认不用加上单引号和双引号。***

  “”：双引号不会转义字符串里面的特殊字符。

  ‘’：单引号会转义。

* #### 对象、Map（属性和值）（键值对）：

  key: value：在下一行来写对象的属性和值的关系，注意缩进。

  ```yml
  friends:
    lastName: zhangshan
    age: 20
  ```

  行内写法：

  ```yml
  friends: {lastName: zhangshan,age: 18}
  ```

* #### 数组（List， set)

  ```yml
  pets:
   - cat
   - dog
   - pig
  ```

  行内写法：

  ```yml
  pets: [cat,dog,pig]
  ```

  

## 3.配置文件值注入

#### 1. 配置文件内容(application.yml)：

```yml
# application.yml
person:
  lastName: zhangshan
  age: 23
  boss: false
  birth: 2017/3/2
  maps: {k1: v1,k2: 23}
  lists:
   - lisi
   - zhaoliu
  dog:
   name: 小狗
   age: 2
```
#### 2. javaBean：

目录层级结构：

----com.jim

   +---- bean

   +---+---- Dog  // 因为Person里面有个Dog对象

   +---+---- Person

   +---- MainApplition.java

```java
// /src/main/java/com/jim/bean/Person.java
/**
 * 将配置文件中配置的每一个属性的值，都映射到这个组件中。
 * @CongigurationProperties: 告诉SpringBoot将本类中的所有属性与配置文件相关配置进行绑定。
 *      prefix = "person": 配置文件中哪个下面的所有属性进行一一映射
 * 只有这个组件是容器中的组件，才能使用容器提供的@ConfigurationProperties功能，故还要加上@Component
 */
@Component
@ConfigurationProperties(prefix = "person")
public class Person {
    private String lastName;
    private Integer age;
    private Date birth;
    private Boolean boss;

    private Map<String, Object> maps;
    private List<Object> lists;
    private Dog dog;
```

***在IDEA中，Alt+Insert可以快速添加set/get方法和toSring方法。***

#### 3. 在pom.xml中添加配置文件处理器（添加依赖），才能让配置文件与类进行绑定：

```xml
       <!--配置文件处理器，将配置文件与类进行绑定-->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-configuration-processor</artifactId>
            <optional>true</optional>
        </dependency>
```

#### 4. 目录结构：

![1532170206750](/assets/images/spring-boot-develop/1532170206750.png)

#### 5. 测试类

1. 目录结构

   ![1532170349436](/assets/images/spring-boot-develop/1532170349436.png) 


2. SpringBoot单元测试，可以在测试期间很方便的类似编码一样进行自动注入

   ```java
   // /src/test/java/com/jim/MainApplicationTests.java
   package com.jim;
   
   import org.junit.runner.RunWith;
   import org.springframework.boot.test.context.SpringBootTest;
   import org.springframework.test.context.junit4.SpringRunner;
   
   @RunWith(SpringRunner.class) // 告诉Spring用SpringRunner引擎启动
   @SpringBootTest // 告诉Spring这是SpringBoot测试用的
   public class HelloWorldMainApplicationTests {
       @Autowired // 1. 将person注入进来，我们要测试person是什么东西
       Person person;
   
       @Test
       public void contentLoads() {
           System.out.println(person); // 2. 在控制台将person打印出来
       }   // System.out.println()在IDEA中快捷键是sout
   }
   ```

   ***如果写RunWith或SpringBootTest或SpringRunner提示没有这个，那就是说没有注入进来，按Alt+Enter让Spring自己导入进来（它自己会添加依赖，然后将包导入进来）。***

####  6. 用application.properties做配置

```properties
# 配置person的值
person.last-name=zhangshan # last-name == lastName
person.age=23
person.birth=2017/2/13
person.maps.k1=v1
person.maps.k2=21
person.lists=a,b,c
person.dog.name=小狗
person.dog.age=2
```

**注：**（解决中文乱码）SpringBoot默认将application.properties用ascii编码，而IDEA用utf-8将application.properties编码，故在IDEA中 File --> settings --> Editor --> File Encoding --> Properties Files(*.properties) , 将文件编码弄成utf-8并打钩。

![1532171968061](/assets/images/spring-boot-develop/1532171968061.png)

#### 7.用@Value（）注入，从配置文件获取值

```java
// @ConfigurationProperties()和@Value()两种注入方法二选一，下面选了@Value()方法，故需要将@ConfigurationProperties()注释掉
// @ConfigurationProperties(prefix = "person") 
public class Person {
    
    @Value("${person.last-name}") // 将配置文件中的person.last-name值赋给lastName
    private String lastName;
    
    @Value("#{11*2}") // #{}是Spring的表达，#{} = ${}
    private Integer age;
    
    @Value("true")
    private Boolean boss;
```

#### 8.@Value()和@ConfigurationProperties()两者获取配置文件的值比较  

|                               | @ConfigurationProperties() | @Value()                     |
| ----------------------------- | :------------------------- | ---------------------------- |
| 功能                          | 批量注入配置文件中的属性   | 需要一个个指定               |
| 松散绑定（松散语法）          | 支持                       | 不支持                       |
| SpEL                          | 不支持                     | 支持                         |
| JSR303                        | 支持                       | 不支持                       |
| 复杂类型封装(Map, List, 对象) | 支持                       | 不支持，只能取出基本类型数据 |

* ***松散绑定：譬如，认为lastName==last-name是一样的为支持松散绑定，反之不支持。***

* ***SpEL：譬如，@Value("#{11\*2}")，Spring是可以算出值出来的，但是如果你在配置文件里写上：person.age=#{11\*2}就会报错，所以@ConfigurationProperties()不支持SpEL。***

* ***JSR303数据校验：***

  ```java
  // @ConfigurationProperties(prefix = "person")
  @Validated
  public class Person {
      //@Value("${person.last-name}")
      @Email
      private String lastName;
  ```

  * ***@Validated表明这个类需要校验，@Email是lastName的一个检验规则(lastName是否为一个邮箱格式)***

  * ***只有@ConfigutationProperties()支持数据检验***

    ```java
    @ConfigurationProperties(prefix = "person")
    @Validated
    public class Person {
        
        @Email
        private String email;
    ```

  **如果说我们只是在业务逻辑中需要获取一下配置文件的某项值，不需要将配置文件的某一个大类全部导入，那么就用@Value()。**

  **如果我们专门写了一个可重用组件（Java里叫JavaBean)来和配置文件进行映射，就直接使用@ConfigurationProperties()，就像和数据库连接取数据一样。**

#### 9.@PropertySource和@ImportResource

​ 1. @ConfigutationProperties()只能将全局配置文件（application.properties或者application.yml）将类进行绑定，而@PropertySource能加载指定的配置文件。

```java
// /src/main/java/com/jim/bean/Person.java
@Component
// @ConfigurationProperties(prefix = "person")
@PropertySource(value = {"classpath:person.properties"})
public class Person {
```

​ 配置文件在resources里：person.propeties。

```yml
# /src/main/resources/person.properties
person.last-name=zhangshan
person.age=23
person.birth=2017/2/13
person.maps.k1=v1
person.maps.k2=21
person.lists=a,b,c
person.dog.name=小狗
person.dog.age=2
```

​ 2. @ImportResource()

```java
// /src/main/java/com/jim/HelloMain.java
@ImportResource(locations = {"classpath:beans.xml"})
@SpringBootApplication
public class HelloMain {
```

​ beans.xml是我们自定义的一个Spring配置文件，放在resources下，我们想让它导入进来并生效，得在**一个配置类**上标注@ImportResource(locations = {"classpath:beans.xml"})，上述例子是标注在主程序（主配置类）上。

 3. SpringBoot推荐给容器添加组件的方式是采用全注解，即配置类==Spring自定义配置文件，使用@Bean给容器中添加组件。

    ```java
    // /src/main/java/com/jim/config/MyAppConfig.java
    package com.jim.config;
    
    import com.jim.service.HelloService;
    import org.springframework.context.annotation.Bean;
    import org.springframework.context.annotation.Configuration;
    
    /**
     * @Configutation: 指明当前类是一个配置类，能替代之前的自定义的Spring配置文件
     */
    @Configuration
    public class MyAppConfig {
        
        // 将方法的返回值添加到Spring容器中，容器中的HelloService组件默认的id就是方法名helloService
        @Bean
        public HelloService helloService() {
            // 如果容器中有HelloService这个组件，那就能new，返回true
            return new HelloService();
        }
    }
    ```

    * 这是自定义的一个配置类：com.jim.config.MyAppConfig.java。

    * **将一个组件添加到Sping中，譬如，我有个组件service下的HelloService组件，那么，我就要在我的MyAppConfig配置类里写上一个方法，这个方法要有@Bean标注，因为这个标注能将该方法的返回值添加到Spring容器中，这样，我只要在该方法中return new HelloService();就好了。**

![1532195706379](/assets/images/spring-boot-develop/1532195706379.png)

{% endraw %}  