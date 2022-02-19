---
layout: post
title: Spring Boot教程笔记--二、配置文件
---
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

## 4. 配置文件占位符

1. 随机数

   ```java
   ${random.value}, ${random.int}, ${random.long}, ${random.int(10)}, ${random.int[1024, 65536]}
   ```

2. 占位符获取之前配置的值，如果没有可以使用“：”指定的默认值

   ```yml
   person.last-name=zhangshan${random.int}
   person.age=23
   person.birth=2017/2/13
   person.maps.k1=v1
   person.maps.k2=21
   person.lists=a,b,c
   # 获取之前配置的person.last-name的值,如果没有,person.dog.name默认等于"a"
   person.dog.name=${person.last-name:a} 
   person.dog.age=2 
   ```

## 5.Profile 

Profile是Spring对不同环境提供不同配置功能的支持，比如说我开发时用开发环境，我测试时用测试环境，可以通过在配置文件指定参数等方式快速切换环境。

### 1. 多Profile文件

格式：application-{profile}.properties或者applicaiton-{profile}.yml

譬如，我配置文件有三份：

![1532248133899](/assets/images/spring-boot-develop/1532248133899.png)

application-dev.properties是dev环境的配置文件，application-prod.properties是prod环境的配置文件。

默认使用application.properties的配置。

### 2. yml支持多文档块方式

.yml可以用“---”划分文档块，每一份文档块的名字就是Spring下profiles的值，在主文档块是用spring->profiles->active指定激活哪个环境，这时候，resources里的配置文件只需要该.yml格式的配置文件就好。

```yml
# application.yml

# 主配置环境
server:
  port: 8081
spring:
  profiles:
    active: dev
    
---
# dev环境
server:
  port: 8082
spring:
  profiles: dev
  
---
# prod环境
server:
  port: 8083
spring:
  profiles: prod 
```



### 3. 激活指定的profile

#### 1.在主配置文件中指定要切换到哪个环境 

```properties
# /resources/application.properties
# 指定激活dev环境（同路径下还有application-dev.properties配置文件,就是激活这一份配置文件）
spring.profiles.active=dev
```

#### 2. 命令行参数

```shell
--spring.profiles.active=dev  # 指定用dev环境
```

![1532249242826](/assets/images/spring-boot-develop/1532249242826.png)

**如果已经打包了，怎么指定环境？**

在jar包里用命令行: java -jar spring-boot-02-config-0.01-SNAPSHOT.jar --spring.profiles.active=dev指定。

![1532249678070](/assets/images/spring-boot-develop/1532249678070.png)

#### 3. jvm参数

-DSpring.profiles.active=dev

![1532249776262](/assets/images/spring-boot-develop/1532249776262.png)

  #### 命令行参数和jvm参数指定环境的优先级比主配置文件高，就是说主配置文件的spring.profiles.active激活dev，但是命令行参数激活prod环境，那么最终是系统运行在prod环境下的。

## 6. 配置文件加载位置

Spring Boot启动会扫描以下位置的application.properties或application.yml文件作为Spring Boot的默认配置文件。

```shell
- file:./config/ # 文件路径下的config文件夹下
- file:./    # 文件路径下的
- classpath:/config/ # 类路径下的config文件夹下
- classpath:/   # 类路径下的
```

以上是按照优先级从高到低的顺序进行加载配置，所有位置的文件都会被加载，**互补配置**。

![1532251045420](/assets/images/spring-boot-develop/1532251045420.png)

**通过spring.config.location改变配置文件位置**。项目打包好之后，可以通过命令行参数的形式，启动项目的时候来指定配置文件的新位置，指定的这个配置文件会和默认加载的配置文件共同起作用形成互补配置。

![1532251517801](/assets/images/spring-boot-develop/1532251517801.png)

--spring.config.location=G:/application.properties, 指定新的配置文件位置是G盘下的application.properties。*如果G:\application.properties的话，\a是转义字符，所以得改成G:/application.properties。*

## 7. 外部配置加载顺序

**Spring Boot可以从以下位置加载配置，优先级从高到低，高优先级覆盖低优先级配置，所有配置会形成互补配置。**

1. 命令行参数

   ```shell
   # --配置项=值，多个配置用空格分开
   java -jar spring-boot.jar --server.port=8080 --server.context-path=/abc
   ```

2. 来自java:comp/env的NDI属性

3. Java系统属性（System.getProperties())

4. 操作系统环境变量

5. RandomValuePropertySource配置的random.*属性值

6. **由jar包外向jar包内寻找，优先加载profile。**

   * jar包外部的application-{profile}.properties或application.yml(带spring.profile)配置文件。
   * jar包内部的application-{profile}.properties或application.yml(带spring.profile)配置文件。
   * jar包外部的application-{profile}.properties或application.yml(不带spring.profile)配置文件。
   * jar包内部的application-{profile}.properties或application.yml(不带spring.profile)配置文件。

*SpringBoot项目jar包和我们自己自定义的外部application.properties放在同一路径下，然后启动项目jar包，该配置文件会生效。*

7. @Configutation注解类上的@PropertySource
8. 通过SpringApplication.setDefaultProperties指定的默认属性

## 8. 自动配置原理

[配置文件能配置的属性参照](https://docs.spring.io/spring-boot/docs/1.5.9.RELEASE/reference/htmlsingle/#common-application-properties)

1. SpringBoot启动的时候加载主配置类，开启了自动配置功能@EnableAutoConfiguration

2. @EnableAutoConfiguration作用：

   * 利用EnableAutoConfigurationImportSelector给容器导入了一些组件，导入的组件内容可以看selectImports()方法。

   * List<String> configurations = getCandidateConfigurations(annotationMetadata, attributes);获取候选的配置。原理：

     * ```yava
       /**
       * 扫描所有jar包类路径下的META-INF/spring.factories，
       * 然后把扫描到的内容包装成properties对象。
       * 从properties中获取到EnableAutoConfiguration.Class类（类名）对应的值，
       * 然后将他们添加在容器中。
       */
       SpringFactoriesLoader.loadFactoryNmaes()
       ```

     **将类路径下META-INF/spring.factories里面配置的所有EnableAutoConfiguration的值加入到了容器中。**

     * 来到Maven：org.springframework.boot:spring-boot-autoconfigure:1.5.14.RElEASE的jar包中，在里面的META-INF里找到spring.factories中有：

       ```java
       # Auto Configure
       org.springframework.boot.autoconfigure.EnableAutoConfiguration=\
       ```

       **将类路径下META-INF/spring.factories里面配置的所有EnableAutoConfiguration的值加入到容器中。**

       ```java
       # Auto Configure
       org.springframework.boot.autoconfigure.EnableAutoConfiguration=\
       # 底下就全是EnableAutoConfiguration的值
       org.springframework.boot.autoconfigure.admin.SpringApplicationAdminJmxAutoConfiguration,\
       org.springframework.boot.autoconfigure.aop.AopAutoConfiguration,\
       org.springframework.boot.autoconfigure.amqp.RabbitAutoConfiguration,\
       org.springframework.boot.autoconfigure.batch.BatchAutoConfiguration,\
       ......
       ```

       每一个xxxAutoConfiguration类都是容器中的一个组件，都加入到容器中，用他们来做自动配置。

     * 每一个配置类进行自动配置功能。

       以**HttpEncodingAutoConfiguration（Http自动编码配置）**为例解释自动配置原理：

       ***IDEA全局搜索类：Ctrl+N。***

       ```java
       @Configuration // 这是一个配置类，跟配置文件一样，也可以给容器中添加组件。
       @EnableConfigurationProperties(HttpEncodingProperties.class) // 启动指定类的ConfigurationProperties功能(解释在下面)
       @ConditionalOnWebApplication // Spring底层的@Conditional注解，根据不同条件，如果满足指定条件，整个配置类里面的配置就会生效。@ConditionalOnWebApplication ==> 判断当前应用是否是Web应用
       @ConditionalOnClass(CharacterEncodingFilter.class) // 判断当前项目有没有CharacterEncodingFilter这个类
       @ConditionalOnProperty(prefix = "spring.http.encoding", value = "enabled", matchIfMissing = true) // 判断配置文件中是否存在spring.http.encoding.enabled这个配置（prefix = "spring.http.encoding", value = "enabled"），如果配置文件中没有该配置，那么spring.http.encoding.enabled默认为true（matchIfMissing）。
       public class HttpEncodingAutoConfiguration {
           
           // 表示已经和SpringBoot的配置文件映射了，故properties就能取到封装好的配置文件里的配置
           private final HttpEncodingProperties properties;
           
           // 这个类只有一个有参构造器，在只有一个有参构造器的情况下，参数的值就会从容器中拿，因为有前面的@EnableConfigurationProperties(HttpEncodingProperties.class)这个注解，所以能拿到，这个注解还能将HttpEncodingProperties加入到ioc容器中
        public HttpEncodingAutoConfiguration(HttpEncodingProperties properties) {
          this.properties = properties;
        }
       
        @Bean // 给容器中添加characterEncodingFilter组件，这个组件的某些值需要从properties中获取
        @ConditionalOnMissingBean(CharacterEncodingFilter.class) // 判断出容器中没有CharacterEncodingFilter这个组件，才可以将该组件添加到容器里
        public CharacterEncodingFilter characterEncodingFilter() {
          CharacterEncodingFilter filter = new OrderedCharacterEncodingFilter();
          filter.setEncoding(this.properties.getCharset().name());
          filter.setForceRequestEncoding(this.properties.shouldForce(Type.REQUEST));
          filter.setForceResponseEncoding(this.properties.shouldForce(Type.RESPONSE));
          return filter;
        }
       ```

       @ConditionalOnWebApplication, @ConditionalOnClass(CharacterEncodingFilter.class), @ConditionalOnProperty(prefix = "spring.http.encoding", value = "enabled", matchIfMissing = true) ==> 根据当前不同的条件判断，决定这个HttpEncodingAutoConfiguration配置类是否生效。

       一旦这个配置类生效，这个配置类就会给容器添加各种组件，这些组件的属性是从对应的xxxxProperties类中获取的，这些类里面的每一个属性又是和配置文件中对应的配置绑定的。

       ```java
       // 解释上面的@EnableConfigurationProperties(HttpEncodingProperties.class)这个注解
       @ConfigurationProperties(prefix = "spring.http.encoding") // 从配置文件中获取指定的值和Bean的属性进行绑定。由prefix = "spring.http.encoding"可看成，我们配置文件可以配spring.http.encoding这个属性，可以配什么值，需要看HttpEncodingProperties这个类有什么值可以配。
       public class HttpEncodingProperties {
       ```

       **所有在配置文件中能配置的属性都是在xxxxProperties类中封装着，配置文件能配置什么就可以参照某个功能对应的这个xxxxProperties类。**

**注：**

1. **SpringBoot启动会加载大量的自动配置类，我们看我们需要的功能SpringBoot有没有默认写好的自动配置类，如果写好了，我们再来看这个自动配置类中配置了哪些组件，只要我们要用的组件存在，我们就不用再来配置了，如果没有，就得写一个配置类，将我们的组件配过去。**

2. **给容器中自动配置类添加组件的时候，会从properties类中获取某些属性，而这些属性的值，我们就可以在配置文件中指定。**

   ```java
   xxxxAutoConfiguration：自动配置类，给容器中添加组件
   xxxxProperties：封装配置文件中相关的属性
   ```

## 9.自动配置类是否启用

### 1. @Conditional派生注解

作用：必须是@Conditional指定的条件成立，才给容器中添加组件，配置类里面的所有内容才生效。

| @Conditional拓展注解            | 作用（判断是否满足当前指定条件）                 |
| ------------------------------- | ------------------------------------------------ |
| @ConditionalOnJava              | 容器中的java版本是否符合要求                     |
| @ConditionalOnBean              | 容器中存在指定Bean                               |
| @ConditionalOnMissingBean       | 容器中不存在指定Bean                             |
| @ConditionalOnExpression        | 满足SpEL表达式指定                               |
| @ConditionalOnClass             | 容器中有指定的类                                 |
| @ConditionalOnMissingClass      | 容器中没有指定的类                               |
| @ConditionalOnSingleCandidate   | 容器中只有一个指定的Bean，或者这个Bean是首选Bean |
| @ConditionalOnProperty          | 容器中指定的属性是否有指定的值                   |
| @ConditionalOnResource          | 类路径下是否存在指定的资源文件                   |
| @ConditionalOnWebApplication    | 当前是Web环境                                    |
| @ConditionalOnNotWebApplication | 当前不是Web环境                                  |
| @ConditionalOnJndi              | JNDI存在指定项                                   |

### 2. 自动配置类必须在一定的条件下才能生效

可以通过在application.properties里添加配置debug=true，然后运行系统，系统就会在在控制台里打印“自动配置报告”。

```properties
# application.properties
debug=true # 开启SringBoot的Debug模式
```

```shell
# 自动配置报告
=========================
AUTO-CONFIGURATION REPORT
=========================

Positive matches: # 匹配上的，启用的自动配置类
-----------------

   DispatcherServletAutoConfiguration matched:
      - @ConditionalOnClass found required class 'org.springframework.web.servlet.DispatcherServlet'; @ConditionalOnMissingClass did not find unwanted class (OnClassCondition)
      - @ConditionalOnWebApplication (required) found StandardServletEnvironment (OnWebApplicationCondition)
......

Negative matches: # 没有匹配上的，没启用的自动配置类
-----------------

   ActiveMQAutoConfiguration:
      Did not match:
         - @ConditionalOnClass did not find required classes 'javax.jms.ConnectionFactory', 'org.apache.activemq.ActiveMQConnectionFactory' (OnClassCondition)
......
```
