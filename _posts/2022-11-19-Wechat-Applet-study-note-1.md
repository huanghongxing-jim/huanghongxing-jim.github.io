---
layout: post
category: [微信小程序]
tag: [微信小程序, 学习笔记, JavaScript]
title: 微信小程序学习笔记1
---

# 一、语法
```javascript
document.getElementById("demo").innerHTML = "Hello JavaScript";
// 单引号和双引号一起用
document.getElementById("demo").innerHTML = 'Hello JavaScript'; 
document.getElementById("demo").style.fontSize = "25px";
// 元素的显示隐藏
document.getElementById("demo").style.display="none";
document.getElementById("demo").style.display="block";
```
1. 形式：
```javascript
// 1. 格式：
<script type="text/javascript">
document.getElementById("demo").innerHTML = "我的第一段 JavaScript";
</script>
// 2. 调用方式：
<!DOCTYPE html>
<html>
<head>
<script>
function myFunction() {
    document.getElementById("demo").innerHTML = "段落被更改。";
}
</script>
</head>
<body>
<h1>一张网页</h1>
<p id="demo">一个段落</p>
<button type="button" onclick="myFunction()">试一试</button>
</body>
</html>
3. 外部脚本
<script src="myScript.js"></script>
```
2. 输出：
![344586a87711ec714e775ebf39f4c26b.png](/assets/images/wechat-applet-study-note/Image1.png)
3. JavaScript关键词：
* break, continue, do...while, for, if...else, return, switch, try...catch
* **debugger(停止执行 JavaScript，如果调用函数可用，调用调试函数）**，function，var
4. JavaScript大小写敏感。
5. JavaScript变量 ==> 数值和字符串
```javascript
var pi = 3.14;
var person = "Bill Gates";
var answer = 'How are you!';
var person = "Bill Gates", carName = "porsche", price = 15000;
```
**注：**
```javascript
// 1. undefined
var a;
// 此时a没有被赋值，但是他仍然是有值的，值是 undefined
// 2. 重复声明不受影响
var carName = "porsche";
var carName; 
// carName仍然有值 ==> "porsche"
// 3. 文本值可以和数值混用
var x = "8" + 3 + 5;
// 区别：
var x = 911 + 7 + "Porsche"; // 输出：918Porsche
var x = "Porsche" + 911 + 7; // 输出：Porsche9117
```
6. 运算符：+，-， *， /，%，++，--，**\*\***
\===：等值等型
\!==：不等值或不等型
**typeof**，**instanceof（返回true）**
7. 数据类型
原始：string，number，boolean，null，undefined。
```javascript
var b = true; // 布尔型
var length = 7; // 数字
var lastName = "Gates"; // 字符串
var cars = ["Porsche", "Volvo", "BMW"]; // 数组
var x = {firstName:"Bill", lastName:"Gates"}; // 对象 
// 变量数据类型可以动态变化
var x; // 现在 x 是 undefined
var x = 7; // 现在 x 是数值
var x = "Bill"; // 现在 x 是字符串值
```
8. undefined, 空值""，null
* 可以通过设置值为undefined清空对象。
* undefined与null的值相等，但类型不相等。
9. 函数
```javascript
function myFunction(p1, p2) {
    return p1 * p2;      
}
```
10. 对象
```javascript
var car = {type:"porsche", model:"911", color:"white"};
var person = {
  firstName: "Bill",
  lastName : "Gates",
  id       : 678,
  fullName : function() {
    return this.firstName + " " + this.lastName;
  }
};
```
11. 事件 

![a216544a53ab2b95e99d7aa1747aa6d4.png](/assets/images/wechat-applet-study-note/Image2.png)
{% raw %}
```html
// 用法：
<element event='一些 JavaScript'>
// 例子：
<button onclick='document.getElementById("demo").innerHTML=Date()'>现在的时间是？</button>
```
{% endraw %}
12.字符串
```javascript
var s = “abcdefg”;
s.length; // 长度
s.indexof("abc"); // 找不到：-1
s.indexof("abc", 3); 
s.lastIndexOf("fg");
s.search("abc"); // 可以正则
s.replace("abc", "dfd"); // 替换一次，可以用正则
str = "Please visit Microsoft!";
var n = str.replace(/MICROSOFT/i, "W3School"); // 替换的时候要对大小写不敏感
var n = str.replace(/Microsoft/g, "W3School"); // 替换所有
// 提取字符串：
s.slice(start, end)
s.substring(start, end)
s.substr(start, length)
// 转换大小写
s.toUpperCase();
s.toLowerCase();
var text1 = "Hello";
var text2 = "World";
text3 = text1.concat(" ",text2);
s.trim(); // 删除字符串两端的空白符
s.charAt(0); // 输出：a
s.charCodeAt(0); // 输出：a的unicode编码
// 字符串转数组
var txt = "a,b,c,d,e"; // 字符串
txt.split(","); // 用逗号分隔
txt.split(" "); // 用空格分隔
txt.split("|"); // 用竖线分隔
txt.split(""); // 分隔为字符
```
1.  数字
```javascript
// 科学计数法
var x = 123e5; // 12300000
var y = 123e-5; // 0.00123
// js会尝试将字符串转换为数字
var x = "100";
var y = "10";
var z = x / y; // z 将是 10
var x = 100 / "10"; // x 将是 10
// 区别：
var x = "100";
var y = "10";
var z = x + y; // z 不会是 110（而是 10010）
// NaN ==> 非数值
var x = 100 / "Apple"; ==> x ==NaN
// 判断某个值是数
isNaN(x)
// Infinity 和 -Infinity ==> 超出最大可能数范围时返回的值，最大值，无穷大
var myNumber = 2;
while (myNumber != Infinity) { // 执行直到 Infinity
    myNumber = myNumber * myNumber;
}
// 数值转字符串
var x = 23;
x.toString(n); // 转换为n进制的字符串
x.toExponential(n); // 返回保留n个小数点后数字的科学计数法
x.toFixed(n); // 保留n个小数点后数字
x.toPrecision(n); // 返回字符串，该字符串保留n个数字
// 变量转数值(直接使用，不用导包）
Number(x);
parseFloat(x);
parseInt(x);
```
14. 数组
```javascript
var arr = new Array(1, 2, 3);
var arr = [];
```
数组是对象。
```javascript
// 数组属性
arr.length;
arr[arr.length-1]; // 最后一个元素值
// 遍历数组
var fruits, text;
fruits = ["Banana", "Orange", "Apple", "Mango"];
text = "<ul>";
fruits.forEach(myFunction);
text += "</ul>";
function myFunction(value) {
  text += "<li>" + value + "</li>";
}
// 以arr为基础创建新数组
var numbers1 = [45, 4, 9, 16, 25];
var numbers2 = numbers1.map(myFunction);
function myFunction(value, index, array) {
  return value * 2;
}
// 数组方法
arr.push("Lemon"); // 返回新数组长度
arr.pop(); // 返回被弹出的值
arr.toString(); // 逗号分开
arr.join(" "); // 数组转换为字符串，空格分开
arr.shift(); // 弹出第一个数组元素，并重新分配索引
arr.unshift("Lemon"); // 添加元素，返回新长度值
delete arr[3]; // arr[3]置为undefined
arr.splice(2, 0, "Lemon", "Kiwi", "j"); // 在2个位置开始，删除0个元素，然后插入“Lemon”和“Kiwi”等新元素
arr.splice(0, 1); // 删除从索引0开始，往后一共1个元素
arr.indexOf("Apple");
arr.indexOf("Apple", 3); // 从第3个索引元素开始
arr.lastIndexOf();
var arr2 = arr.concat(arr1, arr3, arr4);
var arr1 = arr.slice(2); // 返回arr的第2个元素开始的后面所有元素
var arr2 = arr.slice(2, 4); // 第2个参数是个数
arr.sort();
arr.reverse();
arr.sort(function(a, b){return b - a}); // 参数是函数，函数定制，返回值 负值, 0, 正值
arr.sort(function(a, b){return 0.5 - Math.random()});  // 打乱
Math.max.apply(null, arr); // 返回最大值
Math.min.apply(null, arr); // 返回最小值
// 判断是数组(不用导包）
Array.isArray(arr);
arr instanceof Array; // 返回true或者false
// 数组筛选
var numbers = [45, 4, 9, 16, 25];
var over18 = numbers.filter(myFunction);
function myFunction(value, index, array) {
  return value > 18;
}
// 逐个元素积累操作
var numbers1 = [45, 4, 9, 16, 25];
var sum = numbers1.reduce(myFunction);
function myFunction(total, value, index, array) {
  return total + value;
}
// 相似：
reduceRight()
// 检验每个元素
var numbers = [45, 4, 9, 16, 25];
var allOver18 = numbers.every(myFunction);
function myFunction(value, index, array) {
  return value > 18;
}
var someOver18 = numbers.some(myFunction);
function myFunction(value, index, array) {
  return value > 18;
}
 
// 数组搜索（只返回第一个的值）
var numbers = [4, 9, 16, 25, 29];
var first = numbers.find(myFunction);
function myFunction(value, index, array) {
  return value > 18;
}
```
15. 日期
```javascript
// 创建
new Date();
new Date(year, month, day, hours, minutes, seconds, milliseconds); // 可以只指定 年、月、日
new Date(milliseconds);
new Date(dateString); ==> 
// 例子
var d = new Date("October 13, 2014 11:13:00");
new Date("2015-03");
new Date("2018");
new Date("2018-02-19T12:00:00");
new Date("02/19/2018");
// 显示
d.toString();
d.toUTCString();
d.toDateString();
// 获取方法，对应都有set方法
getDate();
getDay();
getFullYear();
getHours();
getMilliseconds();
getMinutes();
getMonth();
getSeconds();
getTime(); // 返回自1970年1月1日以来的毫秒数
getUTC*();
// 日期可以进行比较
var today, someday, text;
today = new Date();
someday = new Date();
someday.setFullYear(2049, 0, 16);
if (someday > today) {
  text = "今天在 2049 年 1 月 16 日之前";
} else {
  text = "今天在 2049 年 1 月 16 日之后";
}
```
16. 数学（不用导包）
```javascript
Math.round() // 四舍五入
Math.pow() // 幂
Math.sqrt()
Math.abs()
Math.ceil()
Math.floor()
Math.sin()
Math.cos()
Math.min() // 可以多参
Math.max()
Math.random() // 0~1
Math.acos()
Math.asin()
Math.atan()
Math.atan2()
Math.exp()
Math.log()
Math.tan()
Math.PI
Math.E // 返回欧拉指数（Euler's number）
Math.PI // 返回圆周率（PI）
Math.SQRT2 // 返回 2 的平方根
Math.SQRT1_2 // 返回 1/2 的平方根
Math.LN2 // 返回 2 的自然对数
Math.LN10 // 返回 10 的自然对数
Math.LOG2E // 返回以 2 为底的 e 的对数（约等于 1.414）
Math.LOG10E // 返回以 10 为底的 e 的对数（约等于0.434）
```
**JavaScript可以使用三元运算符？进行操作。**
17. switch
**使用严格比较\=\=\=。**
18. for/in
```javascript
var person = {fname:"Bill", lname:"Gates", age:62}; 
var text = "";
var x;
for (x in person) {
    text += person[x];
}
```
19. 正则
* 只适用于字符串的两个方法：`search()`和`replace()`。
* 修饰符：
![8c1c47d4be3e9b7e57ab5822c9134c89.png](/assets/images/wechat-applet-study-note/Image3.png)
```javascript
var res = str.replace(/microsoft/i, "W3School"); 
var res = str.replace(/microsoft/g, "W3School"); 
var res = str.replace(/microsoft/m, "W3School"); 
```
* 方法：
```javascript
// 是否有e
var patt = /e/;
patt.test("The best things in life are free!"); // 输出：true
==> 
/e/.test("The best things in life are free!");
// 搜索匹配文本
/e/.exec("The best things in life are free!"); // 输出：e
```
20. 异常
```javascript
try {
}
 catch(err) { // err是参数，不用声明
} 
finally {
}
throw "Too big";    // 抛出文本
throw 500;          //抛出数字
```
21. 作用域
**为尚未声明的变量赋值，此变量会自动成为全局变量。**
```javascript
function myFunction() {
    carName = "porsche";
}
// 函数myFunction没有声明carName就使用这个变量，这个变量直接成为全局变量
```
JavaScript可以先使用变量之后再声明 ==> 提升(hoisting)
**用 let 或 const 声明的变量和常量不会被提升。**
```javascript
// let 声明的是块作用域
{ 
  let x = 10;
  var y = 3;
}
// x 不是全局变量
// y 是全局变量
```
**声明：const、let、var。**
22. 严格模式（开头声明）
```javascript
"use strict";
x = 3.14; 
```
23. this
* 指 该对象
* 单独使用 ==> 全局对象[object Window]
```javascript
function myFunction() {
  return this;
}
```
* 指的是接收此事件的 HTML 元素
```javascript
<button onclick="this.style.display='none'">  点击来删除我！</button>
```
* 显式邦定（ call() 和 apply() ）
```javascript
var person1 = {
  fullName: function() {
    return this.firstName + " " + this.lastName;
  }
}
var person2 = {
  firstName:"Bill",
  lastName: "Gates",
}
person1.fullName.call(person2);  // 会返回 "Bill Gates"
```
24. 调试
`debugger`是设置断点的效果。
```javascript
var x = 15 * 5;
debugger;
document.getElementbyId("demo").innerHTML = x; 
```
25. 风格习惯
*  在运算符（ = + - * / ）周围以及逗号之后添加空格
* 对象：
```javascript
var person = {
    firstName: "Bill",
    lastName: "Gates",
    age: 50,
    eyeColor:  "blue"
};
```
* 常量大写
* 避免全局变量、new、===、eval()
26. 性能
![c12fc24f93a77735e05e1b3625db85a2.png](/assets/images/wechat-applet-study-note/Image4.png)
```javascript
var obj;
obj = document.getElementById("demo"); // 将DOM元素存储为变量
obj.innerHTML = "Hello"; 
```
js脚本放底部。
27. json
```javascript
{
}"employees":[
    {"firstName":"Bill", "lastName":"Gates"}, 
    {"firstName":"Steve", "lastName":"Jobs"},
    {"firstName":"Alan", "lastName":"Turing"}
]
}
// JSON不需要导包
var j = JSON.parse(jsonText);
j.employees[1].firstName;
```
28. 表单
```html
<form name="myForm" action="/action_page_post.php" onsubmit="return validateForm()" method="post">
姓名：<input type="text" name="fname">
<input type="submit" value="Submit">
</form>
<script>
function validateForm() {
    var x = document.forms["myForm"]["fname"].value;
    if (x == "") {
        alert("必须填写姓名");
        return false;
    }
}
</script>
```
input输入验证：
* input本身属性
```javascript
// input的required属性保证一定有值
 <input type="text" name="fname" required>
```
![85f8973c76d47ec6001382403fd4347e.png](/assets/images/wechat-applet-study-note/Image5.png)
* 本身属性 搭配 来自DOM的方法![df00c3d67c6e60d96d9f2e7a847a7db7.png](/assets/images/wechat-applet-study-note/Image6.png)
```html
<input id="id1" type="number" min="100" max="300" required>
<button onclick="myFunction()">OK</button>
<p id="demo"></p>
<script>
 function myFunction() {
    var inpObj = document.getElementById("id1");
    if (inpObj.checkValidity() == false) {    document.getElementById("demo").innerHTML = inpObj.validationMessage;
    }
}
</script>
```
# 二、对象
1. 访问属性
```javascript
objectName.property // person.age
objectName["property"] // person["age"]
objectName[expression] // x = "age"; person[x]
for (variable in object) {
    // 要执行的代码，遍历对象的属性
}
// 例子
var person = {fname:"Bill", lname:"Gates", age:62}; 
for (x in person) {
    txt += person[x];
}
// 添加新属性
person.nationality = "English"; // nationality是新属性
// 删除属性
delete person.age; // 或 delete person["age"];
```
2. 方法
```javascript
var person = {
  firstName: "Bill",
  lastName : "Gates",
  id       : 648,
  fullName : function() {
    return this.firstName + " " + this.lastName;
  }
};
```
3. 对象访问器（ Getter 和 Setter ）
用处：自定义如何 访问 和 设置 对象的属性。
```javascript
// 创建对象：
var person = {
  firstName: "Bill",
  lastName : "Gates",
  language : "en",
  get lang() {
    return this.language;
  },
  set lang(l) {
    this.language = l;
  }
};
// 使用 getter 来显示来自对象的数据：
person.lang = "zh";
document.getElementById("demo").innerHTML = person.lang;
```
4. 对象构造器（有点像 类）
```javascript
function Person(first, last, age, eyecolor) {
    this.firstName = first;
    this.lastName = last;
    this.age = age;
    this.eyeColor = eyecolor;
    this.name = function() {return this.firstName + " " + this.lastName;};
}
var myMother = new Person("Steve", "Jobs", 56, "green");
// Person是对象构造器，无法直接添加新属性
Person.nationality = "English"; // 这是错误的
Person.prototype.nationality = "English"; // 正确做法
Person.prototype.name = function() {
    return this.firstName + " " + this.lastName;
};
```
5. 值传递 和 引用传递
函数参数里，对象通过引用传递，值通过值传递。
