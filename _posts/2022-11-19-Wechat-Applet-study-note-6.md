---
layout: post
category: [微信小程序]
tag: [微信小程序, 学习笔记]
title: 微信小程序学习笔记6
---

## 九、发布
#### 1. [用户体验](https://developers.weixin.qq.com/ebook?action=get_post_info&docid=0002ac4c980cb0bb0086b37695b80a#_ftn3)
* 导航清晰
* 流程明确
* 重点突出
* 符合预期
* 等待与反馈
* 异常处理
* 内容和文案准确友好
* 和谐统一
* 平台适配
#### 2. 发布模式（全量发布和分阶段发布）
#### 3. 运营
> 运营数据分析 ==> 面向产品
运维中心 ==> 面向开发
1. 运营数据中心（运营者）：小程序管理平台 ==> （左侧）“数据分析”菜单
2. 运维中心（开发者）：小程序管理平台 ==> “运维中心”。查看错误日志，监控告警功能，自行开发监控系统（小程序逻辑代码加上对应的错误数据上报）。
## 十、性能优化
![e4dbdfe195e274d4267a10a68d37b524.png](/assets\images\wechat-applet-study-note\Image34.png)
#### 1. 代码包下载
优化方法：
* 精简代码
* 减少在代码包中直接嵌入的资源文件
* 压缩图片，使用适当的图片格式
* 分包下载
#### 2. 数据通信
优化方法：
* 页面初始化的时间大致由页面初始数据通信时间和初始渲染时间两部分构成。其中，数据通信的时间指数据从逻辑层开始组织数据到视图层完全接收完毕的时间，**减少逻辑层的data的数据量**。
* 不频繁调用setData。
* setData数据量少一些。
* 与界面渲染无关的数据最好不要设置在data中，可以考虑设置在page对象的其他字段下。
{% raw %}
```javascript
Page({
  onShow: function() {
    // 不要频繁调用setData
    this.setData({ a: 1 })
    this.setData({ b: 2 })
    // 绝大多数时候可优化为
    this.setData({ a: 1, b: 2 })
    // 不要设置不在界面渲染时使用的数据，并将界面无关的数据放在data外
    this.setData({
      myData: {
        a: '这个字符串在WXML中用到了',
        b: '这个字符串未在WXML中用到，而且它很长…………………………'
      }
    })
    // 可以优化为
    this.setData({
      'myData.a': '这个字符串在WXML中用到了'
    })
    this._myData = {
      b: '这个字符串未在WXML中用到，而且它很长…………………………'
    }
  }
})
```
{% endraw %}
* 视图层会接受用户事件，如点击事件、触摸事件等，再反馈给逻辑层。**去掉不必要的事件绑定（WXML中的bind和catch），从而减少通信的数据量和次数**。
* 事件绑定时需要传输target和currentTarget的dataset，因而不要在节点的data前缀属性中放置过大的数据。
#### 3. 视图层渲染
优化方法：
* 减少WXML节点数量。
* 每次setData都会重新渲染视图，**尽量少用setData**。
* 原生组件用context来更新组件而不用setData。
![fb11049738b292494d1c5c5bbe84c1c3.png](/assets\images\wechat-applet-study-note\Image35.png)
## 十一、[小程序基础库](https://developers.weixin.qq.com/ebook?action=get_post_info&docid=000288319f40c0eb00860cd135100a)
## 十二、微信开发者工具
**功能：代码开发、编译运行、界面和逻辑调试、真机预览和提交发布版本等。**
通过编译过程将WXML文件和WXSS文件都处理成JS代码，使用script标签注入在一个空的html文件中（我们称为：page-frame.html）；我们将所有的JS文件编译成一个单独的app-service.js。
在小程序运行时，逻辑层使用JsCore直接加载app-service.js，渲染层使用WebView加载page-frame.html，在确定页面路径之后，通过动态注入script的方式调用WXML文件和WXSS文件生成的对应页面的JS代码，再结合逻辑层的页面数据，最终渲染出指定的页面。
开发者工具使用一个隐藏着的<webview/>标签来模拟JSCore作为小程序的逻辑层运行环境，通过将JSCore中不支持的BOM对象局部变量化，使得开发者无法在小程序代码中正常使用BOM，从而避免不必要的错误。
在开发者工具底层有一个HTTP服务器来处理来自WebView的请求，并将开发者代码编译处理后的结果作为HTTP请求的返回，WebView按照普通的网页进行渲染。
开发者工具利用BOM、node.js以及模拟的UI和交互流程实现对大部分客户端API的支持。同时开发者工具底层维护着一个WebSocket服务器，用于在WebView与开发者工具之间建立可靠的消息通讯链路，使得接口调用，事件通知，数据交换能够正常进行，从而使小程序模拟器成为一个统一的整体。
微信开发者工具使用webview.showDevTools 打开Chrome Devtools调试逻辑层WebView的JS代码，同时开发了Chrome Devtools插件 WXML 面板对渲染层页面WebView进行界面调试。
WXML面板对渲染层WebView中真实的DOM树做了一个最小树算法的裁剪之后，呈现出与WXML源码一致的节点树列表。
## 补充
#### 1. wxml的data-\*属性
{% raw %}
```html
<view id="tapTest" data-hi="WeChat" bindtap="tapName"> Click me! </view>
```
{% endraw %}
{% raw %}
```javascript
Page({
  tapName: function(event) {
    console.log(event)
  }})
 // 输出：
{
  "type":"tap",
  "timeStamp":895,
  "target": {
    "id": "tapTest",
    "dataset":  { // 数据集
      "hi":"WeChat"
    }
  },
  "currentTarget":  {
    "id": "tapTest",
    "dataset": {
      "hi":"WeChat"
    }
  },
  "detail": {
    "x":53,
    "y":14
  },
  "touches":[{
    "identifier":0,
    "pageX":53,
    "pageY":14,
    "clientX":53,
    "clientY":14
  }],
  "changedTouches":[{
    "identifier":0,
    "pageX":53,
    "pageY":14,
    "clientX":53,
    "clientY":14
  }]}
```
{% endraw %}
横转大，大转小：
![8ef22a36c47e2b96a7504163dd5b085f.png](/assets\images\wechat-applet-study-note\Image36.png)
#### 2. pageX和clientX的区别
{% raw %}
```html
<!--indwx.wxml-->
<view catchtap="click"></view>
```
{% endraw %}
{% raw %}
```javascript
Page({
    click: function(event) {
        event.touches[0].clientX;
        event.touches[0].pageX;
    }
})
```
{% endraw %}
![3156eff3d67b50047c07041655d0b468.png](/assets\images\wechat-applet-study-note\Image37.png)
#### 3. 数组的forEach终止
**通过异常来终止。**
{% raw %}
```javascript
var array = [1, 2, 3];
try {    
    array.forEach(function(item, index){
        if ( item == 3 ) {
            throw new Error("stopLoop");
        }
        console.log( item + ' ' + index );
    });
} catch(e) {
    if( e.message != "stopLoop" ) { // 如果循环里仍然有错误，依然可以抛出来 
        throw e;
    }
}
```
{% endraw %}
测试了一下，如果数组的数据量不大的话，不用通过异常来终止，处理异常要花的时间也是很多的：
{% raw %}
```javascript
var array = [1, 2, 3];
array.forEach(function(item, index) {
    if ( item != 3 ) {
        console.log( item + ' ' + index );
    }
});
```
{% endraw %}
#### 4. bindtap事件与bindtouchstart和bindtouchend冲突
**tap,touchstart,touchend的事件触发顺序为start→end→tap。问题在于catchtouchstart,catchtouchend后事件被阻止了，tap捕获不到。**
想要实现点击“X”号后删除该组价的效果：
![b2fb8097c535b5ddda89c7545a3ac6b6.png](/assets\images\wechat-applet-study-note\Image38.png)
{% raw %}
```html
<view class="big" catchtap="click3">
  <view class="mid" catchtouchstart="click2">
    <view class="small" catchtouchstart="click1"></view>
  </view>
</view>
```
{% endraw %}
在small组件立即捕获touchstart事件就好了，不用tap。
#### 5. 获取某个节点的信息
{% raw %}
```javascript
const query = wx.createSelectorQuery()
query.select('#the-id').boundingClientRect()
query.selectViewport().scrollOffset()
query.exec(function(res){
  res[0].top       // #the-id节点的上边界坐标
  res[1].scrollTop // 显示区域的竖直滚动位置})
```
{% endraw %}
**不能声明两次。**
#### 6. wx.chooseImage()是个异步接口
{% raw %}
```javascript
click: function(e){
    wx.chooseImage({ 
      count: 5,
      sizeType: ['original'],
      sourceType: ['album', 'camera'],
      success: function(res) {
        imgList = res.tempFilePaths;
      }, 
      complete: function(){
        console.log('complete arr:' + imgList.join(',')); // 要实现同步就要在complete中
      }
    });
    console.log('main arr:' + imgList.join(',')); // 这里的imgList数组为空，因为wx.chooseImage()异步，所以上面的wx.chooseImage()还没有执行完就执行这个语句了，这时候imgList还是空的
}
```
{% endraw %}
#### 7. 字符串格式化
{% raw %}
```javascript
let a = 'Hello', b = 'world';
let str = `这是一个测试的字符串：${a} ${b}`;
console.log(str); // 这是一个测试的字符串：Hello world
```
{% endraw %}
**注意str里是反引号 `。**
#### 8.组件穿透
{% raw %}
```css
pointer-events: none;
```
{% endraw %}
#### 8. scroll-view组件的滑动问题
> scroll-y="false" 这个"false"是字符串，要把scroll-y设置成false，**可以使用scroll-y="{{false}}"**，这样子这个scroll-y的值才是布尔值，才能不滑动。
比较：`scroll-y="false"`和`scroll-y="{{false}}"`。

