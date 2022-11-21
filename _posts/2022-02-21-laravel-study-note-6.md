---
layout: post
category: [Larave学习笔记]
tag: [Larave, 学习笔记] 
title: Larave学习笔记6
---


#### 2.发送邮件

![1534343099473](/assets/images/laravel-develop-study/1534343099473.png)

![1534343121043](/assets/images/laravel-develop-study/1534343121043.png)

	配置文件：

{% raw %}
```php
// config/mail.php
<?php
return [
	// 支持："smtp", "sendmail", "mailgun", "mandrill", "ses","sparkpost", "log", "array"
    'driver' => env('MAIL_DRIVER', 'smtp'),
    'host' => env('MAIL_HOST', 'smtp.mailgun.org'),
    'port' => env('MAIL_PORT', 587),
    'from' => [ // 全局的发件人邮件地址以及名称
        'address' => env('MAIL_FROM_ADDRESS', 'hello@example.com'),
        'name' => env('MAIL_FROM_NAME', 'Example'),
    ],
	// 协议
    'encryption' => env('MAIL_ENCRYPTION', 'tls'),
	// STMP的账号密码
    'username' => env('MAIL_USERNAME'),
    'password' => env('MAIL_PASSWORD'),
    'sendmail' => '/usr/sbin/sendmail -bs',
    'markdown' => [
        'theme' => 'default',
        'paths' => [
            resource_path('views/vendor/mail'),
        ],
    ],
];
```
{% endraw %}

1. 在`.env`中进行配置：

{% raw %}
```properties
MAIL_DRIVER=smtp # 使用的服务
MAIL_HOST=smtp.mailtrap.io # 服务器地址
MAIL_PORT=2525 # 服务器端口
MAIL_USERNAME=jim # 账号
MAIL_PASSWORD=passowrd
MAIL_ENCRYPTION=ssl # 协议
```
{% endraw %}

1. 控制器以及路由

{% raw %}
```php
Route::any('mail', ['uses' => 'StudentController@mail']);
```
{% endraw %}

控制器：

- 以`raw`方式发送邮件：

{% raw %}
```php
// StudentController.php
<?php
namespace App\Http\Controllers;
use App\Student;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Mail;
use Illuminate\Support\Facades\Session;
use Illuminate\Support\Facades\Storage;
class StudentController extends Controller
{
   public function mail() {
        Mail::raw("邮件内容", function($message) {
            $message->from('546546@qq.com', 'jim');
            $message->subject('邮件主题');
            $message->to('4649464@qq.com');
       });
   }
}
```
{% endraw %}

- 以`html`方式发送邮件：

创建一个`html`文件，即视图：

{% raw %}
```php
<!--resources/views/student/mail.blade.php-->
<!DOCTYPE html>
<html>
<head>
    <title>标题</title>
</head>
<body> <!--$name由控制器注入进来-->
<h1>Hello {{ $name }}</h1>
</body>
</html>
```
{% endraw %}

	控制器：

{% raw %}
```php
// StudentController.php
<?php
namespace App\Http\Controllers;
use App\Student;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Mail;
use Illuminate\Support\Facades\Session;
use Illuminate\Support\Facades\Storage;
class StudentController extends Controller
{
   public function mail() {
       // 指定要发送的html文件，向该文件注入数据
        Mail::send("student.mail", ['name' => 'jim'], function($message) {
            $message->to('4649464@qq.com');
       });
   }
}
```
{% endraw %}

#### 3.缓存使用

![1534344890615](/assets/images/laravel-develop-study/1534344890615.png)

![1534344915362](/assets/images/laravel-develop-study/1534344915362.png)

![1534344930819](/assets/images/laravel-develop-study/1534344930819.png)

配置文件：

{% raw %}
```php
// config/cache.php
<?php
return [
	// 支持"apc", "array", "database", "file", "memcached", "redis"，默认是file,即文件缓存
    'default' => env('CACHE_DRIVER', 'file'),
	// 缓存配置
    'stores' => [
        'apc' => [
            'driver' => 'apc', // 驱动是apc
        ],
        'array' => [
            'driver' => 'array',
        ],
        'database' => [
            'driver' => 'database',
            'table' => 'cache',
            'connection' => null,
        ],
        'file' => [
            'driver' => 'file',
            'path' => storage_path('framework/cache/data'),
        ],
        'memcached' => [
            'driver' => 'memcached',
            'persistent_id' => env('MEMCACHED_PERSISTENT_ID'),
            'sasl' => [
                env('MEMCACHED_USERNAME'),
                env('MEMCACHED_PASSWORD'),
            ],
            'options' => [
                // Memcached::OPT_CONNECT_TIMEOUT  => 2000,
            ],
            'servers' => [
                [
                    'host' => env('MEMCACHED_HOST', '127.0.0.1'),
                    'port' => env('MEMCACHED_PORT', 11211),
                    'weight' => 100,
                ],
            ],
        ],
        'redis' => [
            'driver' => 'redis',
            'connection' => 'default',
        ],
    ],
	// 缓存前缀
    'prefix' => 'laravel',
];
```
{% endraw %}

控制器：

{% raw %}
```php
// Controllers/StudentController.php
<?php
namespace App\Http\Controllers;
use App\Student;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Mail;
use Illuminate\Support\Facades\Session;
use Illuminate\Support\Facades\Storage;
class StudentController extends Controller
{
    public function cache1() {
        // 保存对象到缓存中,10是对象的保存时间
        Cache::put('key1', 'val1', 10);
    }
    public function cache2() {
        // 获取缓存中的对象，返回一个值，即对象
        $val = Cache::get('key1', 'val1');
    }
}
```
{% endraw %}

	`add()`:添加。

{% raw %}
```php
public function cache1() {
    // add(),如果对象已经存在,就添加失败，如果对象不存在，添加成功
    // 返回一个bool值,10是时间
    $bool = Cache::add('key1', 'val1', '10');
}
```
{% endraw %}

	`forever()`：永久的保存对象到缓存中。	

{% raw %}
```php
public function cache1() {
    Cache::forever('key1', 'val1');
}
```
{% endraw %}

	`has()`:判断缓存中的一个`key`值存不存在。

{% raw %}
```php
public function cache1() {
    if (Cache::has('key')) {
        $val = Cache::get('key')
    } else {
        echo "No"
    }
}
```
{% endraw %}

	`pull`:取缓存中的`key`值，然后删了这个`key`。

{% raw %}
```php
public function cache1() {
    $val = Cache::pull('key');
}
```
{% endraw %}

	`forget()`:从缓存中删除对象，删除成功返回`true`，返回一个`bool`值。

{% raw %}
```php
public function cache1() {
    $bool = Cache::forget('key');
}
```
{% endraw %}

#### 4.错误和日志

![1535095566213](/assets/images/laravel-develop-study/1535095566213.png)

![1535095599480](/assets/images/laravel-develop-study/1535095599480.png)

1. `debug`模式：开发模式，调试模式。

可在`.env`里开启和调试：

{% raw %}
```properties
APP_NAME=Laravel
APP_ENV=local
APP_KEY=base64:KyJsuwkhScgKGjZ2cUJrt3annTBQkSBVDTq7wUXtvqo=
APP_DEBUG=true # 默认开启调试模式
APP_LOG_LEVEL=debug
APP_URL=http://localhost
DB_CONNECTION=mysql
DB_HOST=127.0.0.1
DB_PORT=3306
DB_DATABASE=student
DB_USERNAME=root
DB_PASSWORD=
BROADCAST_DRIVER=log
CACHE_DRIVER=file
SESSION_DRIVER=file
QUEUE_DRIVER=sync
REDIS_HOST=127.0.0.1
REDIS_PASSWORD=null
REDIS_PORT=6379
MAIL_DRIVER=smtp
MAIL_HOST=smtp.mailtrap.io
MAIL_PORT=2525
MAIL_USERNAME=jim
MAIL_PASSWORD=passowrd
MAIL_ENCRYPTION=ssl
PUSHER_APP_ID=
PUSHER_APP_KEY=
PUSHER_APP_SECRET=
```
{% endraw %}

	默认是开启调试模式的，如果发生错误，`laravel`会在网页打印出错误栈。
	
	**上线了一定要关闭调试模式！！**

1. `http`异常

![1535096147008](/assets/images/laravel-develop-study/1535096147008.png)

自定义`http`异常：

{% raw %}
```php
<?php
namespace App\Http\Controllers;
use App\Student;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Mail;
use Illuminate\Support\Facades\Session;
use Illuminate\Support\Facades\Storage;
class StudentController extends Controller
{
    public function error() {
        $val = null;
        if ($val == null) {
            // 自定义http异常,抛出503异常
            abort('503'); 
        }
    }
}
```
{% endraw %}

`http`异常的视图位置：

`vendor\laravel\framework\src\Illuminate\Foundation\Exceptions\views`:

![1535098035926](/assets/images/laravel-develop-study/1535098035926.png)

1. 日志

![1535098224286](/assets/images/laravel-develop-study/1535098224286.png)

`config/app.php`：

{% raw %}
```php
<?php
return [
    ...
    // 日志定义的位置
	// 支持"single", "daily", "syslog", "errorlog"模式，默认是single模式
    'log' => env('APP_LOG', 'single'), 
    'log_level' => env('APP_LOG_LEVEL', 'debug'),
    ...
];
```
{% endraw %}

	配置日志模式：

{% raw %}
```php
# 在.env中进行配置
# APP_LoG原本的.env里是没有的，是自己添加的，只能配置"single", "daily", "syslog", "errorlog"这几种模式
APP_LoG=single 
APP_LOG_LEVEL=debug
```
{% endraw %}

	这样是会在![1535098804878](/assets/images/laravel-develop-study/1535098804878.png)这里生成日志文件:`laravel.log`。
	
	使用日志：

{% raw %}
```php
// Controllers/StudentController.php
<?php
namespace App\Http\Controllers;
use App\Student;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Log;
use Illuminate\Support\Facades\Mail;
use Illuminate\Support\Facades\Session;
use Illuminate\Support\Facades\Storage;
class StudentController extends Controller
{
    public function log() {
        // 这里使用的是single的log模式
        // use Illuminate\Support\Facades\Log;
        Log::info("这是一个info级别的日志");
        Log::warning("这是一个warning级别的日志");
        // Log::error可以传进一个对象或者数组，它会自动在日志文件里序列化成
        // 一个json格式的数据
        Log::error("这是一个error级别的日志",
                ['name' => 'jim', 'age' => 18]);
    }
}
```
{% endraw %}

	`daily`的`log`模式，会每天生成一个日志：

![1535099439063](/assets/images/laravel-develop-study/1535099439063.png)


