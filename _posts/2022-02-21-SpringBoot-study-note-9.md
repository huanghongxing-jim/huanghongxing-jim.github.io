---
layout: post
category: [SprintBoot教程笔记]
tag: [SpringBoot, 学习笔记] 
title: 五、开发笔记（Spring Boot教程笔记9）
---


## 5.Restful

1. RestfulCRUD:CRUD满足Rest风格。

   URI：/资源名称/资源标识	HTTP请求方式区分对资源CRUD操作

|      | 普通CRUD(uri来区分)       | RestfulCRUD        |
| ---- | ------------------------- | ------------------ |
| 查询 | getEmp                    | emp --> GET        |
| 添加 | addEmp?xxx                | emp --> POST       |
| 修改 | updateEmp?id=xxx&xxx=xxxx | emp/{id} --> PUT   |
| 删除 | deleteEmp?id=1            | emp/{id} -->DELETE |

1. 自定义的请求架构

|                                      | 请求URI  | 请求方式 |
| ------------------------------------ | -------- | -------- |
| 查询所有员工                         | emps     | GET      |
| 查询某个员工（来到修改页面）         | emp/{id} | GET      |
| 来到添加页面                         | emp      | GET      |
| 添加员工                             | emp      | POST     |
| 来到修改页面（查出员工进行信息回显） | emp{id}  | GET      |
| 修改员工                             | emp      | PUT      |
| 删除员工                             | emp/{id} | DELETE   |

1. 员工控制器

{% raw %}
```java
// EmployeeController.java
package com.jimcom.springboot.controller;
import com.jimcom.springboot.dao.EmployeeDao;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
public class EmployeeController {
    // 将员工信息自动注入进来
    @Autowired
    EmployeeDao employeeDao;
    // 查询所有员工返回列表页面
    @GetMapping("/emps")
    public String list(Model model) {
        Collection<Employee> employees = employeeDao.getAll();
        // 将员工列表信息放在请求域中
        model.addAttribute("emps", employees);
        return "emp/list";
    }
}
```
{% endraw %}

​	位置：

![1534138300937](/assets/images/spring-boot-develop/1534138300937.png)

1. `thymeleaf`公共页面元素抽取

   1. 抽取公共片段

{% raw %}
```html
      <div th:fragment="footer-copy">
          &copy; 2011
      </div>
```
{% endraw %}

   2. 引入公共片段

{% raw %}
```html
      <div th:insert="~{footer::footer-copy}"></div>
      	写法：
      		~{templatename::selector}	模板名::选择器
      		~{templatename::fragmentname}	模板名::片段名
      		templatename::selector/templatename::fragmentname	不用写~{}
      	注：行内写法要加上~{}: [(!{xxx})] [[~{xxx}]]
```
{% endraw %}

   3. 三种引入功能片段的`th`属性：`th:insert`, `th:replace`, `th:include`.

{% raw %}
```html
      <div th:fragment="footer-copy">
          &copy; 2011
      </div>
      引入方式：
      <div th:insert="footer::footer-copy"></div>
      <div th:replace="footer::footer-copy"></div>
      <div th:include="footer::footer-copy"></div>
      效果：
      insert：将公共片段整个插入到声明引入的元素中
      replace：将声明引入的元素替换为公共片段
      include：将被引入的片段的内容包含进这个标签中
```
{% endraw %}

# 六、[教程整合篇](https://www.bilibili.com/video/av23284778/)


