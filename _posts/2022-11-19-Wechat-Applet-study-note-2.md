---
layout: post
category: [微信小程序]
tag: [微信小程序, 学习笔记, JavaScript]
title: 微信小程序学习笔记2
---

# 三、HTML DOM（文档对象模型）
**js能够改变html文档所有元素。**
![ca1030ddd921f48fff965d7486716e0a.png](/assets/images/wechat-applet-study-note/Image7.png)
1. DOM方法
![f10a153ac91f591f20b292542580e940.png](/assets/images/wechat-applet-study-note/Image8.png)
![75ea407f96ca53a9ebb5a20c0e6b43bc.png](/assets/images/wechat-applet-study-note/Image9.png)
![944d122af74d2eede0332e53ece54690.png](/assets/images/wechat-applet-study-note/Image10.png)
![415fa81d6fa864019345fb817380033c.png](/assets/images/wechat-applet-study-note/Image11.png)
HTML对象：
![8c04ebaf6d1f7749b4c23980924e5e5a.png](/assets/images/wechat-applet-study-note/Image12.png)
2. 改变元素属性
{% raw %}
```javascript
document.getElementById("myImage").src = "landscape.jpg";
```
{% endraw %}
3. 改变CSS
{% raw %}
```javascript
document.getElementById("p2").style.color = "blue";
```
{% endraw %}
4. DOM事件（任何元素都可以添加）
onclick, onload, onunload(离开页面), onmouseover, onmouseout, onmousedown, onmouseup。
{% raw %}
```javascript
// 事件监听器
document.getElementById("myBtn").addEventListener("click", displayDate);
element.addEventListener(event, function, useCapture);
// 第三个参数是布尔值，指定使用事件冒泡还是事件捕获。此参数是可选的
// 第一个参数："click" "mouseout" "mouseover"等
// 也可以给window添加监听器
window.addEventListener("resize", function(){
    document.getElementById("demo").innerHTML = sometext;
});
// 移除事件监听器
element.removeEventListener("mousemove", myFunction);
```
{% endraw %}
5. DOM节点
![387d651023f65fc1558aa668fa9ac940.png](/assets/images/wechat-applet-study-note/Image13.png)
parentNode，childNodes[nodenumber]，firstChild，lastChild，nextSibling，reviousSibling。
{% raw %}
```javascript
var myTitle = document.getElementById("demo").firstChild.nodeValue;
// 创造新节点
var para = document.createElement("p");
var node = document.createTextNode("这是新文本。");
para.appendChild(node);
var element = document.getElementById("div1");
element.appendChild(para);
// 创造新html元素
var para = document.createElement("p");
var node = document.createTextNode("这是新文本。");
para.appendChild(node);
var element = document.getElementById("div1");
var child = document.getElementById("p1");
element.insertBefore(para, child);
// 删除html元素
var parent = document.getElementById("div1");
var child = document.getElementById("p1");
parent.removeChild(child);
// 替换html元素
var para = document.createElement("p");
var node = document.createTextNode("这是新文本。");
para.appendChild(node);
var parent = document.getElementById("div1");
var child = document.getElementById("p1");
parent.replaceChild(para, child);
```
{% endraw %}
6. HTML DOM集合
{% raw %}
```javascript
var myCollection = document.getElementsByTagName("p"); // 返回HTMLCollection对象
myCollection.length;
myCollection[0];
// HTMLCollection不是数组，无法使用数组方法：valueOf(), pop(), push(), join()。
```
{% endraw %}

