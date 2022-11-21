---
layout: post
category: [微信小程序]
tag: [微信小程序, 学习笔记]
title: 微信小程序学习笔记4
---

**小程序的主要开发语言是 JavaScript，jq等js库无法在小程序中运行。**
## 一、框架
* .json 后缀的 JSON 配置文件
* .wxml 后缀的 WXML 模板文件，静态配置
* .wxss 后缀的 WXSS 样式文件
* .js 后缀的 JS 脚本逻辑文件
#### 1. JSON配置
1. 根目录的app.json 和 project.config.json，每个页面(pages/index)page.json。
2. app.json:全局配置，**小程序的所有页面路径(第一项默认为首页)**、界面表现、网络超时时间、底部 tab等。
3. project.config.json:针对`微信开发者工具`这个软件的个性化配置。
#### 2. WXML
1. 组件：<view>, <button>, <text>, <map>等。
2. 逻辑: `{{ msg }}`, `wx:if`等。
3. 样式WXSS。
4. JS逻辑
![6b0de2edf072d09ae602be25c3b72827.png](/assets\images\wechat-applet-study-note\Image16.png)
#### 3. 运行框架
![b3ac0760adf1b37ed0576006a5abac13.png](/assets\images\wechat-applet-study-note\Image17.png)
生成页面顺序：page.json ==> page.wxml + page.wxss ==> page.js
{% raw %}
```javascript
// page.js
Page({
  data: { // 参与页面渲染的数据
    logs: []
  },
  onLoad: function () {
    // 页面渲染后 执行
  }})
// Page()是个页面构造器（相当于类）
```
{% endraw %}
![28c6252652d34f76b8ed3a6cb522963d.png](/assets\images\wechat-applet-study-note\Image18.png)
## 二、协同工作
小程序开发成员：运营者、开发者、数据分析者。
运营数据查看：[小程序管理后台](https://mp.weixin.qq.com/) 和 小程序数据助手（也是一个小程序）。
## 三、WXML模板
1. 数据绑定（ js 与 wxml ）
{% raw %}
```javascript
// 动态绑定
// 1. wxml
<text data-test="{{test}}"> hello world</text>
// 2. js
Page({
    data: {
        test: (new Date()).toString()
    },
})
```
{% endraw %}
**没有被定义的变量的或者是被设置为 undefined 的变量不会被同步到 wxml 中。**
{% raw %}
```html
<block wx:if="{{true}}">
  <view> view1 </view>
  <view> view2 </view>
</block>
// 列表渲染
<!-- array 是一个数组 -->
<view wx:for="{{array}}">
  {{index}}: {{item.message}}
</view>
<!-- 对应的脚本文件
Page({
  data: {
    array: [{
      message: 'foo',
    }, {
      message: 'bar'
    }]
  }
})
-->
wx:for-item, wx:for-index
```
{% endraw %}
2. 模板
{% raw %}
```html
<template name="msgItem">
  <view>
    <text> {{index}}: {{msg}} </text>
    <text> Time: {{time}} </text>
  </view>
</template>
<!-- is可以动态决定具体需要渲染哪个模板 -->
<block wx:for="{{[1, 2, 3, 4, 5]}}">
  <template is="{{item % 2 == 0 ? 'even' : 'msgItem'}}"/>
</block>
<import src="item.wxml"/>
<template is="item" data="{{text: 'forbar'}}"/>
<!-- include --> 
<!-- index.wxml -->
<include src="header.wxml"/>
<view> body </view>
<include src="footer.wxml"/>
<!-- header.wxml -->
<view> header </view>
<!-- footer.wxml -->
<view> footer </view>
```
{% endraw %}
3. wxml标签共同属性
![2765055242f6c35355874f2b3e957ddc.png](/assets\images\wechat-applet-study-note\Image19.png)
## 四、WXSS
两种wxss：app.wxss（根目录）和page.wxss（每个页面的wxss）
1. 样式的引用
{% raw %}
```css
@import url('./test_0.css')
@import './test_0.wxss'
```
{% endraw %}
2. 用`rpx`。
3. 动态的内联样式
{% raw %}
```html
<!--index.wxml-->
<!--可动态变化的内联样式-->
<!--
{
  eleColor: 'red',
  eleFontsize: '48rpx'
}
-->
<view style="color: {{eleColor}}; font-size: {{eleFontsize}}"></view>
```
{% endraw %}
4. [官方样式库](
https://github.com/Tencent/weui-wxss)
## 五、JavaScript脚本
![50dc7677d0ca33a0030e75bb4a2cc528.png](/assets\images\wechat-applet-study-note\Image20.png)
1. 模块化
小程序中可以将任何一个JavaScript 文件作为一个模块，通过module.exports 或者 exports 对外暴露接口。
![ea9ec55a9212e1434214b1d5005310ca.png](/assets\images\wechat-applet-study-note\Image21.png)
2. 作用域
在文件中声明的变量和函数只在该文件中有效，不同的文件中可以声明相同名字的变量和函数，不会互相影响。
当需要使用全局变量的时，通过使用全局函数 getApp() 获取全局的实例，并设置相关属性值，来达到设置全局变量的目的
{% raw %}
```javascript
// 访问全局变量
var global = getApp()
console.log(global.globalValue) // 输出 globalValue
```
{% endraw %}
## 六、程序（代码层面的小程序）
#### 1. 程序构造器App()
* 在`app.js`里
* 其他js里：`getApp()`
* 构造器：
{% raw %}
```javascript
App({
  onLaunch: function(options) {},
  onShow: function(options) {},
  onHide: function() {},
  onError: function(msg) {},
  globalData: 'I am global data'
})
```
{% endraw %}
* ![6edce8af3c39f05a1e35d4702656b9e0.png](/assets\images\wechat-applet-study-note\Image22.png)
* 小程序的JS脚本是运行在同一个JsCore的线程里，小程序的每个页面各自有一个WebView线程进行渲染，所以小程序切换页面时，小程序逻辑层的JS脚本运行上下文依旧在同一个JsCore线程中。所有页面的脚本逻辑都跑在同一个JsCore线程，页面使用setTimeout或者setInterval的定时器，然后跳转到其他页面时，这些定时器并没有被清除，需要开发者自己在页面离开的时候进行清理。
#### 2. 页面（界面、配置和逻辑）
1. 一个页面，wxml、js必须，json、wxss可选，都在同一文件夹下。
2. 根目录 ==> App.js ==> App() ; 每个页面目录 ==> page.js ==> Page()。
{% raw %}
```javascript
Page({
  data: { text: "This is page data." },
  onLoad: function(options) { }, 
  onReady: function() { },
  onShow: function() { },
  onHide: function() { },
  onUnload: function() { },
  onPullDownRefresh: function() { }, 
  onReachBottom: function() { },
  onShareAppMessage: function () { },
  onPageScroll: function() { }
})
```
{% endraw %}
![09ba87035b42143952e16be4066aa302.png](/assets\images\wechat-applet-study-note\Image23.png)
![ee41f52a098c9339af508b966debdd22.png](/assets\images\wechat-applet-study-note\Image24.png)
点击商品列表页的项目进入商品详情页：
{% raw %}
```javascript
// pages/list/list.js 表示商品详情页
// 列表页使用navigateTo跳转到详情页
wx.navigateTo({ url: 'pages/detail/detail?id=1&other=abc' })
// pages/detail/detail.js
Page({
  onLoad: function(option) { console.log(option.id) console.log(option.other)
  }
})
// onLoad里的函数有个option参数，就是来接收来自其他页面的数据的
```
{% endraw %}
和网页URL一样，页面URL上的value如果涉及特殊字符（例如：&字符、?字符、中文字符等 ），需要采用UrlEncode后再拼接到页面URL上: `'pages/detail/detail?id=1&other=abc'`。
3. setData()
{% raw %}
```javascript
// page.js
Page({
  onLoad: function(){
    this.setData({
      text: 'change data'
    }, function(){
      // 在这次setData对界面渲染完毕后触发
    })
  }
})
```
{% endraw %}
4. 小程序宿主环境提供了四个和页面相关的用户行为回调：
1）下拉刷新 onPullDownRefresh
监听用户下拉刷新事件，需要在app.json的window选项中或页面配置page.json中设置enablePullDownRefresh为true。`{"enablePullDownRefresh": true }。`当处理完数据刷新后，wx.stopPullDownRefresh可以停止当前页面的下拉刷新。
2）上拉触底 onReachBottom
监听用户上拉触底事件。可以在app.json的window选项中或页面配置page.json中设置触发距离onReachBottomDistance。在触发距离内滑动期间，本事件只会被触发一次。当界面的下方距离页面底部距离小于100像素时触发回调：`page.json:
{"onReachBottomDistance": 100 }`。
3）页面滚动 onPageScroll
监听用户滑动页面事件，参数为 Object，包含 scrollTop 字段，表示页面在垂直方向已滚动的距离（单位px）。
4）用户转发 onShareAppMessage
只有定义了此事件处理函数，右上角菜单才会显示“转发”按钮，在用户点击转发按钮的时候会调用，此事件需要return一个Object，包含title和path两个字段，用于自定义转发内容。
{% raw %}
```javascript
// page.js
Page({
onShareAppMessage: function () {
 return {
   title: '自定义转发标题',
   path: '/page/user?id=123'
 }
}
})
```
{% endraw %}
5. 页面栈
> [ pageA, pageB, pageC ]，其中pageA在最底下，pageC在最顶上，也就是用户所看到的界面
`wx.navigateTo`推入一个新的页面，`wx.redirectTo({ url: 'pageE' })`是替换当前页变成pageE。
{% raw %}
```javascript
// app.json定义小程序原生底部tab
{
  "tabBar": {
    "list": [
      { "text": "Tab1", "pagePath": "pageA" },
      { "text": "Tab1", "pagePath": "pageF" },
      { "text": "Tab1", "pagePath": "pageG" }
    ]
  }
}
```
{% endraw %}
每个tab对应一个页面栈，使用`wx.switchTab({ url: 'pageF' })`，此时原来的页面栈会被清空，然后会切到pageF所在的tab页面，页面栈变成 [ pageF ]，但是如果切回原来的tab页面，该页面的onLoad不会被触发。
**wx.navigateTo和wx.redirectTo只能打开非TabBar页面，wx.switchTab只能打开Tabbar页面。**
还可以使用 wx. reLaunch({ url: 'pageH' }) 重启小程序，并且打开pageH，此时页面栈为 [ pageH ]。
![a370ec3878ce913a5aff8e61280643b5.png](/assets\images\wechat-applet-study-note\Image25.png)
![d2c94106207c9702fe6f32ef85854b02.png](/assets\images\wechat-applet-study-note\Image26.png)
#### 3. [组件](https://developers.weixin.qq.com/miniprogram/dev/component/)
[scroll-view组件](https://mp.weixin.qq.com/debug/wxadoc/dev/component/scroll-view.html)
#### 4. [API](https://mp.weixin.qq.com/debug/wxadoc/dev/api/)
`wx`对象实际上就是小程序的宿主环境所提供的全局对象，几乎所有小程序的API都挂载在`wx`对象底下（除了`Page/App`等特殊的构造器）。
几大功能API：网络、媒体、文件、数据缓存、位置、设备、界面、界面节点信息还有一些特殊的开放接口。
1. wx.on\*：监听。
2. API接口，异步，参数为一个对象，对象有success、fail、complete三个回调函数。
3. wx.get\*：获取宿主环境数据。
4. wx.set\*：写入数据到宿主环境。
{% raw %}
```javascript
wx.request({
url: 'test.php',
data: {},
header: { 'content-type': 'application/json' },
success: function(res) {
 // 收到https服务成功后返回
 console.log(res.data)
},
fail: function() {
 // 发生网络错误等情况触发
},
complete: function() {
 // 成功或者失败后触发
}
})
```
{% endraw %}
![d5358bd107dc841b9d892cf48cf9f80e.png](/assets\images\wechat-applet-study-note\Image27.png)
5. 事件
![555b79dbf26433f80a70720edcdf8854.png](/assets\images\wechat-applet-study-note\Image28.png)
{% raw %}
```html
<!-- 触发顺序：4-2-3-1 -->
<view
  id="outer"
  bind:touchstart="handleTap1"
  capture-bind:touchstart="handleTap2"
>
  outer view
  <view
    id="inner"
    bind:touchstart="handleTap3"
    capture-bind:touchstart="handleTap4"
  >
    inner view
  </view>
</view>
```
{% endraw %}
catch事件绑定可以阻止冒泡事件向上冒泡: 将handleTap2的capture-bind改为capture-catch，将只触发handleTap2(capture-catch将中断捕获阶段和取消冒泡阶段)，handleTap4, handleTap3, handleTap1不会被触发。
**自定义事件如无特殊声明都是非冒泡事件，如<form/>的submit事件，<input/>的input事件，<scroll-view/>的scroll事件。**

