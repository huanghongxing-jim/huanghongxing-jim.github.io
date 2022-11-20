---
layout: post
category: [微信小程序]
tag: [微信小程序, 学习笔记, JavaScript]
title: 微信小程序学习笔记3
---
{% raw %}
# 四、BOM
浏览器对象模型（Browser Object Model (BOM)）允许 JavaScript 与 浏览器 对话。
DOM ==> 文档
BOM ==> 浏览器
1. Window(代表浏览器的窗口)
```javascript
// document是window属性
window.document.getElementById("header");
==>
document.getElementById("header");
// 尺寸
window.innerHeight
window.innerWidth
```
![731b7b3b009163dba8aefc3b4bc2331d.png](/assets/images/wechat-applet-study-note/Image14.png)
2. Screen（用户屏幕信息）
screen == window.screen
```javascript
screen.width
screen.height
screen.availWidth
screen.availHeight
screen.colorDepth
screen.pixelDepth
```
3. Location(页面URL)
location == window.location
![bc0988dafff80a5cb9f41a22d5c8070e.png](/assets/images/wechat-applet-study-note/Image15.png)
4. History
history == window.history
```javascript
history.back(); // 浏览器后退
history.forward(); // 浏览器前进
```
5. navigator(访问者的信息)
navigator == window.navigator
```javascript
navigator.appName // 浏览器名称
navigator.appCodeName // 浏览器代码名称
navigator.platform // 浏览器的操作系统
navigator.appVersion // 浏览器版本
navigator。product // 浏览器引擎的产品名称
navigator.cookieEnabled // 是否有cookie
navigator.userAgent // 浏览器发送到服务器的用户代理报头（user-agent header）
navigator.language // 浏览器语言
navigator.onLine // 浏览器是否在线
navigator.javaEnabled // java是否启用
```
6. 弹出框
```javascript
// 警告
window.alert("...");
// 确认
var r = confirm("请按按钮");
if (r == true) {
    x = "您按了确认！";
} else {
    x = "您按了取消！";
}
// 提示
var person = window.prompt("请输入您的姓名", "比尔盖茨");
if (person != null) {
  document.getElementById("demo").innerHTML = "你好 " + person + "！今天过的怎么样？";
}
// 换行
alert("Hello\nHow are you?");
```
7. 定时
`window.setTimeout(function, milliseconds)`：在等待指定的毫秒数后执行函数，一次。
`windows.setInterval(function, milliseconds)`：等同于 setTimeout()，但持续重复执行该函数。
```javascript
// 停止执行
myVar = setTimeout(function, milliseconds);
clearTimeout(myVar);
myVar = setInterval(function, milliseconds);
clearInterval(myVar);
```
8. Cookie（在网页中存储用户信息）
```javascript
// 创建cookie
document.cookie = "username=John Doe; expires=Sun, 31 Dec 2017 12:00:00 UTC";
```
# 五、JSON
```javascript
// 使用jason方法，不用导包
var myObj = { name:"Bill Gates",  age:62, city:"Seattle" };
var myJSON =  JSON.stringify(myObj);
window.location = "demo_json.php?x=" + myJSON;
// myObj是对象，JSON.stringify()将这个对象转化为json对象
// 解析json对象为JavaScript对象
var myJSON = '{ "name":"Bill Gates",  "age":62, "city":"Seattle" }';
var myObj =  JSON.parse(myJSON);
document.getElementById("demo").innerHTML = myObj.name;
// 将 对象数据 存储在本地中
myObj = { name:"Bill Gates",  age:62, city:"Seattle" };
myJSON =  JSON.stringify(myObj);
localStorage.setItem("testJSON", myJSON);
// 从本地存储的json数据中获取数据
text = localStorage.getItem("testJSON");
obj =  JSON.parse(text);
document.getElementById("demo").innerHTML = obj.name;
```
{% endraw %}  