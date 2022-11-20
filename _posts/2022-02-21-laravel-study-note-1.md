---
layout: post
category: [Larave学习笔记]
tag: [Larave, 学习笔记] 
title: Larave学习笔记1
---
{% raw %}

# 一、laravel基础

****

**设置数据库编码, 更改数据库的编码为utf8mb4:***

***修改mysql配置文件(Linux为my.cnf, windows为my.ini, my.cnf一般在etc/mysql/my.cnf位置)。***

```mysql
# 找到后在以下三部分里添加如下内容：  
[client]  
default-character-set = utf8mb4  
[mysql]  
default-character-set = utf8mb4  
[mysqld]  
character-set-client-handshake = FALSE  
character-set-server = utf8mb4  
collation-server = utf8mb4_unicode_ci  
init_connect='SET NAMES utf8mb4' 
```

***mysql查询该表的所有列：***

```mysql
show columns from <table name>;
```

## 1. 路由和MVC

### 1. 核心目录

```php
app:应用程序核心代码，自定义的业务逻辑，app->http->controller。
bootstrap：框架启动，自动加载
config：所有应用程序的配置
database：数据库迁移和填充
public：项目静态资源
resources：视图，resources->views。
storage：编译后的文件，storage->logs。
tests：单元测试目录，测试代码
vendor：依赖模块
```

### 2. 路由

1. laravel的请求对应的是`路由`。
2. 请求类型get, post, put, patch, delete。
3. 多请求路由

```php
Route::match(['get', 'post'], 'multy', function() {
    return 'multy';
}); // 相应指定请求类型的请求

Route::any('multy', function() {
    return 'multy';
}); // 响应所有类型请求
```

4. 路由参数

   ```php
   Route::get('user/{id}', function($id) {
       return 'User'.$id;
   }); // 参数一定要有
   Route::get('user/{name?}', function($name = null) {
       return 'User'.$name;
   }); // 可选参数,默认为null
   Route::get('user/{name?}', function($name = null) {
       return 'User'.$name;
   })->where('name', '[A-Za-z]+'); // 后面可以跟正则表达式验证这个参数
   Route::get('user/{id}/{name?}', function($id, $name = null) {
       return 'User'.$name.$id;
   })->where(['id' => '[0-9]+', 'name' => '[A-Za-z]+']); // 验证多参数
   ```

5. 路由别名

   ```php
   // 给路由给别名，这个别名可以在路由、控制器中用，另外如果以后想改url，有了别名，那么其他地方就不用改了
   Route::get('user/center', ['as' => 'center', function() {
       return 'center';
   }]); 
   // 如果以后我想改一下url，将'user/center'改成'men-user/center', 那么我就只改那里就行了，其他的地方因为用的都是路由别名，只要别名不改，那么其他地方也不用改
   ```

6. 路由群组

   ```php
   Route::group(['prefix' => 'member'], funciton() {
       Route::get('user/center', ['as' => 'center', function() {
       return 'center';
   }]); 
       Route::get('user/{id}/{name?}', function($id, $name = null) {
       return 'User'.$name.$id;
   })->where(['id' => '[0-9]+', 'name' => '[A-Za-z]+']);
   });
   // 将两个路由放到了一个路由群组里面，并且给两个路由加了一个前缀，访问member/user/center或者member/usr/3/才能真正访问到上面的两个路由，就是说给两个路由的url前加了'member/'
   ```

7. 路由中输出视图

   ```php
   Route::get('view', function() {
       return view('Hello!');
   });
   ```

### 3.控制器

1. 项目中，路由只是来接受请求，然后转给控制器中的方法进行处理。

2. 新建控制器

   ```php
   // /App/Http/Controllers/MemberController.php
   <?php
   namespace App\Http\Controllers; // 写命名空间
   class MemberController extends Controller
   {
       public function info() {
           return 'member-info';
       }
   }
   ```

3. 控制器与路由关联

   ```php
   // 方法一
   Route::get('member/info', 'MemberController@info');
   // 方法二
   Route::get('member/info', ['uses' => 'MemberController@info']);
   // 起别名的路由
   Route::get('member/info', ['uses' => 'MemberController@info', 'as' => 'memberinfo']);
   // 控制器中：
   // class MemberController extends Controller
   // {
   //     public function info() {
   //         return route('memberinfo'); 
   //     } // 'memberinfo'是路由的别名，路由传进到控制器里面来了
   // }
   ```

4. 关联控制器后，使用路由器

   ```php
   // 参数绑定
   Route::get('member/{id}', ['uses' => 'MemberController@info']);
   // 控制器中：
   // class MemberController extends Controller
   // {
   //     public function info($id) {
   //         return $id; // 参数id传进去控制器里了
   // }
   ```

### 4. 视图(输出视图)


* 控制器中直接view（'<视图名称>');

```php
// APP/Http/HomeController.php
public function index()
{
return view('home');
}
// 在views中有home.blade.php。
```

* 一般来说一个控制器要对应一个视图里的文件夹

```php
// APP/Http/HomeController.php,这个是home控制器
public function index()
{
return view('home/index'); // 不要忘记加"home/"
}
// 那么就有views/home/index.blade.php，上面的home.blade.php中的模板内容被放在了views视图目录里的home文件里，变成了index.blade.php这个文件
```

* 模板带变量

```php
// APP/Http/HomeController.php
public function index()
{
return view('home/index', [
'name' => 'Jim',
'age' => 18
]);
}
```

```php
// 模板中获取变量
// views/home/index.blade.php
{{ $name }} {{ $age }}
```

### 5. 模型

1. 新建模型

   ```php
   // App/Aritcle.php,在App目录下新建模型的php文件
   <?php
   
   namespace App;
   use Illuminate\Database\Eloquent\Model;
   
   class Article extends Model
   {	// 这是一个静态方法，所以控制器里用Article::info();
       public static function info() 
       {
           return "this a article model."
       }
   }
   ```

2. 使用模型

   ```php
   // APP/Http/ArticleController.php，在控制器里使用模型
   <?php
   
   namespace App\Http\Controllers;
   use App\Article;
   use Illuminate\Http\Request;
   
   class ArticleController extends Controller
   {
       public function show(){
   		return Article::info();
       }
   }
   ```

{% endraw %}   