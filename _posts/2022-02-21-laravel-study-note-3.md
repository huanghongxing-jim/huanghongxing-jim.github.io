---
layout: post
category: [Larave学习笔记]
tag: [Larave, 学习笔记] 
title: Larave学习笔记3
---


# 二、laravel表单

## 1.request

{% raw %}
```php
<?php
namespace App\Http\Controllers;
use App\Student;
use Illuminate\Http\Request;
class StudentController
{
    public function request(Request $request) { // 这个$request是Illuminate\Http\Request的
        // 1.取值
        $request->input('name');
        $request->input('name', '未知'); // 如果name值不存在，则输出未知
        $request->has('name'); // 判断有无该属性
        $request->all(); // 取出请求中所有属性，以数组的方式列出来
        // 2.判断请求类型
        $request->method();
        $request->ismethod('GET'); // 判断请求是否用GET方法
        $request->ajax(); // 判断是否ajax请求
        // 3.判断请求是否满足特定格式
        $request->is('student/*'); // 判断是不是student这个url路径下的，即是否请求路径的前缀为：http://<ip addr>/student/
        $request->url(); // 请求的路径
    }
}
```
{% endraw %}

## 2.session

session的配置文件在config/session.php中。

使用session的三种方法：

* HTTP request类的session()方法
* session()辅助函数
* Session facade

config/session.php部分解析：

{% raw %}
```php
<?php
return [
	// 默认使用file驱动，支持："file", "cookie", "database", "apc", "memcached", "redis", "array"
    'driver' => env('SESSION_DRIVER', 'file'), 
    // session有效期
    'lifetime' => 120,
    'expire_on_close' => false,
    'encrypt' => false,
    'files' => storage_path('framework/sessions'),
    'connection' => null,
    // 使用数据库驱动的话，默认的表是sessions
    'table' => 'sessions',
    'store' => null,
    'lottery' => [2, 100],
    'cookie' => env(
        'SESSION_COOKIE',
        str_slug(env('APP_NAME', 'laravel'), '_').'_session'
    ),
    'path' => '/',
    'domain' => env('SESSION_DOMAIN', null),
    'secure' => env('SESSION_SECURE_COOKIE', false),
    'http_only' => true,
    'same_site' => null,
];
```
{% endraw %}

**先在路由表中添加要使用session()的路由的web中间件：**

{% raw %}
```php
// routes/web.php
Route::group(['middleware' => ['web']], function (){ // 用路由组的方式同时给session1和session2两个路由添加webs中间价
    Route::any('session1', ['uses' => 'StudentController@session1']);
    Route::any('session2', ['uses' => 'StudentController@session2']);
});
```
{% endraw %}

1.HTTP request的session()

先访问session1方法，会往session放入一个key，然后访问session2方法，会从session中取出key值。

{% raw %}
```php
class StudentController
{
    public function session1(Request $request) {
        $request->session()->put('key', 'value'); // 用put往session放入一个key属性，值为value
    }
    public function session2(Request $request) {
        $val = $request->session()->get('key'); // 用get从session取出key值
    }
}
```
{% endraw %}

2.直接session()

{% raw %}
```php
class StudentController
{
    public function session1(Request $request) {
        session()->put('key', 'value'); // 用put往session放入一个key属性，值为value
    }
    public function session2(Request $request) {
        session()->get('key'); // 用get从session取出key值
    }
}
```
{% endraw %}

3.Session facade

{% raw %}
```php
class StudentController
{
    public function session1(Request $request) { // 这里的Session导入的是Illuminate\Support\Facades\Session
        Session::put('key', 'value'); // 用put往session放入一个key属性，值为value
    }
    public function session2(Request $request) {
        Session::get('key'); // 用get从session取出key值
        Session::get('key', 'default'); // 用get从session取出key，如果没有，则为'default'
    }
}
```
{% endraw %}

其他用法：

{% raw %}
```php
// 以数组形式存储数据
Session::put(['key' => 'value']);
// 把数据放到Session的数组中，这里同时将'a', 'b'同时存进'student'中，所以'student'就会是个数组
Session::push('student', 'a');
Session::push('student', 'b');
// 从session中取出'student'，然后就把它从session删除
Session::pull('student', 'default');
// 取出所有的值,返回一个数组
$res = Session::all();
// 判断key值存不存在，返回一个bool值
$bool = Session::has('key')；
// 删除session中的key值
Session::forget('key');
// 清空session中所有的数据
Session::flush();
// 暂存数据，只有第一次访问的时候存在
class StudentController
{
    public function session1(Request $request) {
        Session::flash('key', 'value'); // 暂存'key'属性，其值为'value'
    }
    public function session2(Request $request) {
        Session::get('key'); // 第一次访问session2的时候能打印出'key'值，一刷新，即第二次访问session2就没有了
    }
}
```
{% endraw %}

## 3.response

响应的类型：字符串， 视图， Json， 重定向。

1. Json

{% raw %}
```php
public function response() {
    // 响应Json
    $data = [
        'errCode' => 0,
        'errMsg' => 'Error'
    ];
    // 将数据以json形式传过去
    return response()->json($data);
}
```
{% endraw %}

2. 重定向

{% raw %}
```php
class StudentController
{
    public function session(Request $request) {
        // 带数据的重定向其实也是用Session的flash(),故取数据时用get就可以了，但只能取一次
        return Session::get('msg', 'default msg');
    }
    public function response() {
//        return redirect('session'); // 不带数据的重定向
        return redirect('session')->with('msg', '我是快闪数据'); // 带数据的重定向
    }
}
```
{% endraw %}

	或者：
	
	action(), 控制器+方法

{% raw %}
```php
class StudentController
{
    public function session(Request $request) {
        return Session::get('msg', 'default msg');
    }
    public function response() {
        return redirect()
            ->action('StudentController@session') // 重定向的是控制器
            ->with('msg', '我是快闪数据'); // 可带重定向数据也可以不带
    }
}
```
{% endraw %}

	或者：
	
	route(), 路由别名

{% raw %}
```php
class StudentController
{
    public function session(Request $request) {
        return Session::get('msg', 'default msg');
    }
    public function respose() {
        return redirect()
            ->route('session') // 通过路由别名重定向
            ->with('msg', '我是快闪数据'); // 可带重定向数据也可以不带
    }
}
```
{% endraw %}

	或者：
	
	back(),返回上一个页面

{% raw %}
```php
class StudentController
{
    public function response() {
        redirect()->back();
    }
}
```
{% endraw %}

## 4.Middleware

Laravel中间件提供了一个方便的机制来过滤进入应用程序的HTTP请求。

假设一个场景：有一个活动，指定日期开始前只能访问宣传页面，活动开始日期后才可以访问活动页面。

1. 新建控制器方法

{% raw %}
```php
<?php
namespace App\Http\Controllers;
use App\Student;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Session;
class StudentController
{
    public function activity_advertise() {
        return '活动宣传页面';
    }
    public function activity_running() {
        return '活动进行中';
    }
}
```
{% endraw %}

2. 新建中间件

![2018-08-06_213029](/assets/images/laravel-develop-study/2018-08-06_213029.png)

{% raw %}
```php
<?php
namespace App\Http\Middleware;
class Activity
{
    public function handle($request, \Closure $next) { // 函数名是固定的
                                    // 这里的$next是个方法，如果看'\Closure $next'不爽，可以在头部添加'use Closure'，
                                    //  这样，这里就可以写成：public function handle($request, Closure $next)
        if (time() < strtotime('2018-08-07')) { // strtotime()将'yyyy-MM-dd'格式的日期转为一个时间戳
            return redirect('activity_advertise');
        }
        return $next($request); // $next是个方法，将$request请求扔进这个方法里
    }
}
```
{% endraw %}

	在Kernel.php中注册中间件:

![2018-08-06_213247](/assets/images/laravel-develop-study/2018-08-06_213247.png)

{% raw %}
```php
    protected $routeMiddleware = [
        'auth' => \Illuminate\Auth\Middleware\Authenticate::class,
        'auth.basic' => \Illuminate\Auth\Middleware\AuthenticateWithBasicAuth::class,
        'bindings' => \Illuminate\Routing\Middleware\SubstituteBindings::class,
        'can' => \Illuminate\Auth\Middleware\Authorize::class,
        'guest' => \App\Http\Middleware\RedirectIfAuthenticated::class,
        'throttle' => \Illuminate\Routing\Middleware\ThrottleRequests::class,
        'activity' => \App\Http\Middleware\Activity::class, // 注册在这里，值为中间件路径
    ];
```
{% endraw %}

	如果想注册全局中间件，则在Kernel.php里的这里注册：

{% raw %}
```php
protected $middleware = [
    \Illuminate\Foundation\Http\Middleware\CheckForMaintenanceMode::class,
    \Illuminate\Foundation\Http\Middleware\ValidatePostSize::class,
    \App\Http\Middleware\TrimStrings::class,
    \Illuminate\Foundation\Http\Middleware\ConvertEmptyStringsToNull::class,
    \App\Http\Middleware\TrustProxies::class,
];
```
{% endraw %}

3. 使用中间件(在路由文件中)

{% raw %}
```php
// 访问活动页面就会跳入这个中间件
Route::group(['middleware' => ['activity']], function () {
    Route::any('activity_running', ['uses' => 'StudentController@activity_running']);
});
// 然后中间件根据判断就会重定向到这个路由
Route::any('activity_advertise', ['uses' => 'StudentController@activity_advertise']);
```
{% endraw %}

4. 其他

中间件有前置操作和后置操作。

{% raw %}
```php
// 后置操作
<?php
namespace App\Http\Middleware;
use Closure;
class Activity
{
    public function handle($request, Closure $next) {
        $response = $next($request);
        echo $response;
    }
}
```
{% endraw %}

{% raw %}
```php
// 前置操作
<?php
namespace App\Http\Middleware;
use Closure;
class Activity
{
    public function handle($request, Closure $next) {
        echo 'Jim';
        return $next($request);
    }
}
```
{% endraw %}


