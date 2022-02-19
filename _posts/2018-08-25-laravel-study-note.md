---
layout: post
title: Laravel学习笔记
---
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
\{{ $name \}} \{{ $age \}}
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

## 2.数据库操作

**Laravel提供了DB facade（原始查找）、查询构造器和Eloquent ORM三种操作数据库的方式。**

### 1.连接数据库(config/database.php + .env)

打开config/database.php,找到：

```php
// 表示默认要连接的数据库是mysql
'default' => env('DB_CONNECTION', 'mysql'),
```

再往下找到：

```php
// 下面的env(..., ...)其实就是根目录的.env文件里的信息
'mysql' => [
    'driver' => 'mysql',
    'host' => env('DB_HOST', '127.0.0.1'),
    'port' => env('DB_PORT', '3306'),
    'database' => env('DB_DATABASE', 'forge'),
    'username' => env('DB_USERNAME', 'forge'),
    'password' => env('DB_PASSWORD', ''),
    'unix_socket' => env('DB_SOCKET', ''),
    'charset' => 'utf8mb4',
    'collation' => 'utf8mb4_unicode_ci',
    'prefix' => '', // 表前缀
    'strict' => true,
    'engine' => null,
],
```

打开.env,找到:

```php
DB_CONNECTION=mysql
DB_HOST=127.0.0.1
DB_PORT=3306
DB_DATABASE=laravel5
DB_USERNAME=root
DB_PASSWORD=
```

数据库连接完成。

### 2.使用DB facade实现CURD

CURD：增删改查

```php
// App/Http/Controllers/ArticleController.php，控制器里操作数据库
<?php

namespace App\Http\Controllers;
use App\Article;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\DB;

class ArticleController extends Controller
{
    public function operate(){
        // 插入
        $bool = DB::insert('insert into student(name, age) value(?, ?)', ['Jim', 18]);
        var_dump($bool); // 返回插入成不成功的值，true或false
        
        // 更新
        $num = DB::update('update student set age = ? where name = ?', [20, 'Jim']);
        var_dump($num); // 返回修改的行数
        
        // 查询
        $students = DB::select('select * from student where id > ?', [1001]);
        dd($students); // 返回查询结果，是个数组
        
        // 删除
        $num = DB::delete('delete from student where id > ?', [1001]);
        var_dump($num); // 返回被删除的行数

    }
}
```

var_dump(), dd()，都是调试代码，都能将()里的东西打印出来。

### 3.查询构造器

#### 1.新增数据

```php
// App/Http/Controllers/HomeController.php
public function query(){
        // 插入成功返回一个布尔值
        $bool = DB::table('student')->insert(
            ['name' => 'Jim', 'age' =>  18]
        );
        // 插入成功返回插入的id
        $id = DB::table('student')->insertGetId(
            ['name' => 'Jim', 'age' => 18]
        );
        // 插入多条数据
        $id = DB::table('student')->insert(
            ['name' => 'name1', 'age' => 18],
            ['name' => 'name2', 'age' => 18],
            ['name' => 'name3', 'age' => 18],
            ['name' => 'name4', 'age' => 18]
        );
    }
```

#### 2.更新数据

```php
// App/Http/Controllers/HomeController.php   
public function query(){
        // 将student表中id=2的元组中的age更新为30，返回的是受影响的行数
        $num = DB::table('student')
            ->where('id', 12) // 更新数据一定要带条件
            ->update(['age' => 30]);
        // 自增和自减
        $num = DB::table('student')->increment('age'); // 默认自增1
        $num = DB::table('student')->increment('age', 3); // 自增3
        $num = DB::table('student')->decrement('age'); // 默认自减1
        $num = DB::table('student')->decrement('age', 3); // 自减3
        // 将student表中id=12的元组的age自增3，同时name改为Jim
        $num = DB::table('student')
            ->where('id', 12)
            ->decrement('age', 3, ['name' => 'Jim']);
    }
```

#### 3.删除数据 

```php
// App/Http/Controllers/HomeController.php    
public function query(){
        // 删除student表中id=12的元组，返回受影响的行数
        $num = DB::table('student')
            ->where('id', 12)
            ->delete();
        // 删除student表中id>=12的元组，返回受影响的行数
        $num = DB::table('student')
            ->where('id', '>=', 12)
            ->delete();
        // 删除表，不返回任何东西
        DB::table('student')->truncate();
    }
```

#### 4.查询数据

get(), first(), where(), pluck(), lists(), select(), chunk().

```php
// App/Http/Controllers/HomeController.php  
public function query(){
        // get(),返回的是所有的表数据，一个列表
        $student = DB::table('student')->get();
        // first(),返回的是第一条记录
        $student = DB::table('student')->first();
        $student = DB::table('student') // 以student表的id进行倒序排序，获取第一条数据
            ->orderBy('id','desc')
            ->first();
        // where()
        $student = DB::table('student')
            ->where('id', '>=', 122)
            ->get();
        $student = DB::table('student') // 加多个条件查询
            ->whereRaw('id >= ? and age > ?', [122, 34])
            ->get();
        // pluck(),返回字段,是个列表
        $student = DB::table('student') // 返回student表的name字段
        ->pluck('name');
        // lists(),返回字段
        $student = DB::table('student') // 返回student表的name字段
        ->lists('name');
        $student = DB::table('student') // 返回student表的name字段
        ->lists('name', 'id');          // 但是这个列表中的索引用的是id
        // select()，返回的是指定的字段
        $name = DB::table('student')
            ->select('id', 'name', 'age')
            ->get();
        // chunk()，有时候数据太多，一次性获取会太慢，所以就要分段进行获取
        $name = DB::table('student')->chunk(50, function ($student){ // 每次获取50条元组，这50条元组赋值给闭包中的$student
            if( <条件> ){       // 当满足条件的时候，就会返回false，一旦返回false，程序就停止查询，所以可以通过设定条件让程序只查询几次就可以了
                return false;
            }
        });
    }
```

#### 5.聚合函数

count(), avg(), max(), sum(), min().

```php
// App/Http/Controllers/HomeController.php 
public function query(){
        // 返回元组的个数
        $sum = DB::table('student')->count();
        // 返回student表中age字段的最大值
        $sum = DB::table('student')->max('age');
        // 返回student表中age字段的最小值
        $sum = DB::table('student')->min('age');
        // 返回student表中age字段的值的平均值
        $sum = DB::table('student')->avg('age');
        // 返回student表中age字段的值的总和
        $sum = DB::table('student')->sum('age');
    }
```

### 4.Eloauent ORM

在laravel中用model跟数据库中的表进行交互，laravel自带的Eloquent ORM用来实现数据库操作。

#### 1.创建model

在App下面创建一个Student的model类：

```php
<?php

namespace App;

use Illuminate\Database\Eloquent\Model;

class Student extends Model
{
    // 指定表名，没有指定的话，默认为该模型的复数即students
    protected $table = 'student';

    // 指定主键，默认是表中的id字段
    protected $primaryKey = 'id';

}
```

这样，一个model就创建好了。

#### 2.使用model

在model对应的controller中使用model。

```php
<?php

namespace App\Http\Controllers;

class StudentController
{
    public function orm() {
        // all(),查询表的所有记录，返回一个集合collection
        $students = Student::all();
        // 返回id为12的元组
        $student = Student::find(12);
        // findOrFail(),根据指定查找，如果没有找到，返回异常
        $student = Student::findOrFail(12); // id为12的元组找不到就报错
    }
}
```

在ORM中使用查询构造器：

```php
<?php

namespace App\Http\Controllers;

class StudentController
{
    public function orm() {
        // 查询所有，返回一个集合collection
        $student = Student::get();
        
        $student = Student::where('id', '>', '34')
            ->orderBy('age', 'desc')
            ->first();
        
        Student::chunk(2, function($stuent){
            var_dump($student);
        });
        
        $num = Student::count();
        
        $max = Student::where('id', '>', 1002)->max('age');
              
    }
}
```

#### 3. 自定义时间戳及批量赋值

```php
// Student model
// App/Student.php
<?php

namespace App;


use Illuminate\Database\Eloquent\Model;

class Student extends Model
{
    // 指定表名，没有指定的话，默认为该模型的复数即students
    protected $table = 'student';

    // 指定主键，默认是表中的id字段
    protected $primaryKey = 'id';

    // 一般情况下模型对象向数据库增加数据时还会附加一个时间戳，
    // 如果不想要，在这里将$timestamps设置为false即可
    protected $timestamps = true;
    // 该函数与上面的$timestamps=true结合在一起给增添的字段附加一个时间戳
    protected function getDateFormat()
    {
        return time(); // 返回给我们的时间将会是格式化好的
    }
    // 如果我们不想格式化，让模型给我们返回一个时间戳（我们自己之后利用
    // 这个时间戳做自己想做的事。用下面这个函数：
    protected function asDateTime($value)
    {
        return $value;
    }
}
```

```php
// 在StudentConller这个控制器中操纵Student这个model
// App/Http/Controllers/StudentConller.php
<?php

namespace App\Http\Controllers;


class StudentController
{
    public function orm() {

        $student = new Student();
        $student->name = 'Jim';
        $student->age = 12;
        $bool = $student->save(); // 保存数据到数据库直接这样就行，返回一个bool
        // $student->created_at会返回一个时间戳，这个已经在Student这个model设置好了
        // 然后我们用这个时间戳自己再来格式化并打印
        echo data('Y-m-d H:i:s', $student->created_at);
    }
}
```

批量赋值数据：

```php
// App/Http/Controllers/StudentConller.php
<?php

namespace App\Http\Controllers;


class StudentController
{
    public function orm() {
		// 使用create()新增数据
        $student = Student::create(
        	['name' => 'Jim', 'age' => 23]
        );
    }
}
```

```php
// App/Student.php
<?php

namespace App;

use Illuminate\Database\Eloquent\Model;

class Student extends Model
{    // 指定允许批量赋值的model的字段，然后controller里就可以
    // 用model的create()批量赋值数据
    protected $fillable = ['name', 'age'];

    // 指定不允许批量赋值的model的字段
    protected $guarded = [];
}
```

其他新增数据的方法：

```php
// 以字段查找某个元组，如果没有那就创建
$student = Student::firstOrCreate(
    ['name' => 'Jim']
);

// 以字段查找某个元组，如果没有那就创建
$student = Student::firstOrNew(
    ['name' => 'Jim']
);
// firstOrNew是不会将数据保存数据库的，如果需要保存，
// 则自己编写以下的保存代码,返回是个bool，即保存成不成功
$bool = $student->save();
```

#### 4.修改数据

```php
// App/Http/Controllers/StudentConller.php
<?php

namespace App\Http\Controllers;

use App\Student;

class StudentController
{
    public function orm() {
        // 1.通过模型更新数据，返回的$bool代表保存得成不成功
        $student = Student::find(2021);
        $student->name = 'Jim';
        $bool = $student->save();
        // 2.利用查询语句来更新数据
        $num = Student::where('id', '>', 120)
            ->update(
                ['age' => 23]
            );
    }
}
```

#### 5.删除数据

```php
public function orm() {
    // 1.通过模型删除,返回一个代表删除成不成功的$bool
    $student = Student::find(201);
    $bool = $student->delete(); // 删除不到这个元组就会报错

    // 2.通过主键删除,返回删除的行数，即一个删除了几行
    $num = Student::destroy(1021);
    // 删除多个id的元组：
    $num = Student::destroy(1021, 33);
    // 或者：
    $num = Student::destroy([2021, 33]);

    // 3.通过查询语句删除,返回删除的行数
    $num = Student::where('id', '>', 23)->delete();
}
```

## 3.Blade模板

### 1.模板继承

![20180805224923.png](/assets/images/laravel-develop-study/20180805224923.png)

父模板(views.layouts)：

```php
// resources/views/layouts.blade.php
\{{--@section,展示片段内容--\}}
@section('header')
    头部
@show

@section('sidebar')
    侧边栏
@show

\{{--@yield，展示字符串内容--\}}
@yield('content', '主要内容')
```

子模板(views.student.child):

```php
// resources/views/student/child.blade.php
\{{--1.继承哪个模板--\}}
@extends('layouts')

\{{--2.替换父模板中@section的header内容，输出父模板对应地方的父内容--\}}
@section('header')
    @parent
    header
@stop
\{{--或者--\}}
\{{--重写父模板中@section的sidebar内容，不会输出父模板对应地方的父内容--\}}
@section('sidebar')
    sidebar
@stop

\{{--3.替换父模板中@yield的content内容--\}}
@section('content')
    content
@stop
```

controller中访问的是子模板：

```php
// App/Http/Controllers/StudentController.php
<?php

namespace App\Http\Controllers;


use App\Student;

class StudentController
{
    public function view() {
        return view('student.child'); // 访问views目录底下的student/child.blade.php
    }
}
```

### 2.基础语法：

```php
\{{--resources/views/student/child.blade.php--\}}
\{{--1.模板中输出PHP变量，该变量由控制器传入--\}}
\{{ $name \}}

\{{--2.模板中调用PHP代码,$name和$arr两个变量都由控制器中传进来--\}}
\{{ time() \}}
\{{ date('Y-m-d H:i:s', time()) \}}
\{{--判断$arr数组中是否有$name,有返回true，没有返回false--\}}
\{{ in_array($name, $arr) ? 'ture': 'false' \}}
\{{--判断$name是否存在,有返回$name值，没有返回字符串'default'--\}}
\{{ isset($name) ? $name: 'default' \}}
\{{--或者--\}}
\{{ $name or 'default' \}}

\{{--3.原样输出，视图渲染时输出\{{ $name \}}--\}}
@\{{ $name \}}

\{{--4.模板注释--\}}
\{{--xxxx--\}}

\{{--5.子模板中引入子视图--\}}
@include('student.common')
\{{--子视图中有占位符$msg,在这里将msg赋值并传给子视图--\}}
@include('student.common', ['msg' => 'error'])
```

控制器传入值：

```php
class StudentController
{
    public function view() {
        $name = 'Jim';
        $arr = ['a', 'b'];
        return view('student.child', [
            'name' => $name, // 传入值
            'arr' =>$arr, // 传入数组
        ]);
    }
}
```

子视图：

```php
\{{--resources/views/student/common.blade.php--\}}
\{{--$msg是个占位符，等着别处传过来值给它赋值--\}}
\{{ $msg \}}
```

### 3.模板中流程控制

```php
\{{--resources/vies/student/child.blade.php--\}}

\{{--if--\}}
@if ($name == 'Jim')
    Jim
@elseif($name == 'a')
    a
@else
    b
@endif

\{{--unless,相当于if的取反--\}}
@unless( $name == 'Jim' )
    output Jim
@endunless

\{{--for--\}}
@for ($i=0; $i<2; $i++)
    <p>\{{ $i \}}</p>
@endfor

\{{--foreach,遍历对象列表或者数组--\}}
@foreach($students as $student) \{{--该$student对象列表由控制器传入--\}}
    <p>\{{ $student->name \}}</p> \{{--返回$student对象的name属性--\}}
@endforeach

\{{--forelse--\}}
@forelse($students as $student)
    <p>\{{ $student->name \}}</p>
@empty\{{--如果对象列表为空--\}}
    <p>null</p>
@endforelse
```

控制器中将对象数组传给视图：

```php
<?php

namespace App\Http\Controllers;

use App\Student;

class StudentController
{
    public function view() {
        $students = Student::get(); // 从model中获取所有的元组对象，组成一个对象列表
        $name = 'Jim';
        return view('student.child', [
            'name' => $name,
            'students' => $students,
        ]);
    }
}
```

### 4.模板中url

路由：

```php
// 路由名字：urlTest， 路由别名：urlAlias， 控制器及方法：StudentController@urlTest 
Route::any('urlTest', ['as' => 'urlAlias', 'uses' => 'StudentController@urlTest']);
```

模板中生成url：

```php
\{{--resources/views/student/child.blade.php--\}}
\{{--1.指定的路由名字--\}}
<a href="\{{ url('urlTest') \}}">This is url.</a>
\{{--2.控制器+方法名--\}}
<a href="\{{ action('StudentController@urlTest') \}}">This is url.</a>
\{{--3.路由的别名--\}}
<a href="\{{ route('urlAlias') \}}">This is url.</a>
```

# 二、laravel表单

## 1.request

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

## 2.session

session的配置文件在config/session.php中。

使用session的三种方法：

* HTTP request类的session()方法
* session()辅助函数
* Session facade

config/session.php部分解析：

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

**先在路由表中添加要使用session()的路由的web中间件：**

```php
// routes/web.php
Route::group(['middleware' => ['web']], function (){ // 用路由组的方式同时给session1和session2两个路由添加webs中间价
    Route::any('session1', ['uses' => 'StudentController@session1']);
    Route::any('session2', ['uses' => 'StudentController@session2']);
});
```

1.HTTP request的session()

先访问session1方法，会往session放入一个key，然后访问session2方法，会从session中取出key值。

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

2.直接session()

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

3.Session facade

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

其他用法：

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

## 3.response

响应的类型：字符串， 视图， Json， 重定向。

1. Json

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

2. 重定向

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

	或者：
	
	action(), 控制器+方法

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

	或者：
	
	route(), 路由别名

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

	或者：
	
	back(),返回上一个页面

```php
class StudentController
{
    public function response() {
        redirect()->back();
    }
}
```

## 4.Middleware

Laravel中间件提供了一个方便的机制来过滤进入应用程序的HTTP请求。

假设一个场景：有一个活动，指定日期开始前只能访问宣传页面，活动开始日期后才可以访问活动页面。

1. 新建控制器方法

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

2. 新建中间件

![2018-08-06_213029](/assets/images/laravel-develop-study/2018-08-06_213029.png)

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

	在Kernel.php中注册中间件:

![2018-08-06_213247](/assets/images/laravel-develop-study/2018-08-06_213247.png)

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

	如果想注册全局中间件，则在Kernel.php里的这里注册：

```php
protected $middleware = [
    \Illuminate\Foundation\Http\Middleware\CheckForMaintenanceMode::class,
    \Illuminate\Foundation\Http\Middleware\ValidatePostSize::class,
    \App\Http\Middleware\TrimStrings::class,
    \Illuminate\Foundation\Http\Middleware\ConvertEmptyStringsToNull::class,
    \App\Http\Middleware\TrustProxies::class,
];
```

3. 使用中间件(在路由文件中)

```php
// 访问活动页面就会跳入这个中间件
Route::group(['middleware' => ['activity']], function () {
    Route::any('activity_running', ['uses' => 'StudentController@activity_running']);
});
// 然后中间件根据判断就会重定向到这个路由
Route::any('activity_advertise', ['uses' => 'StudentController@activity_advertise']);
```

4. 其他

中间件有前置操作和后置操作。

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

## 5.表单案例笔记

1.静态资源路径：`\{{ asset() \}}`

```php
    <link href="\{{ asset('static/css/bootstrap.min.css') \}}" rel="stylesheet">
```

这个路径是相对于public文件夹下的，也就是文件位置：![2018-08-07_134524](/assets/images/laravel-develop-study/2018-08-07_134524.png)

2. 表单分页

   控制器下用`Student::paginate(num)`取得所有的数据，然后将数据再传给视图。

```php
<?php

namespace App\Http\Controllers;


use App\Student;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Session;

class StudentController extends Controller
{
    public function index() {
        $students = Student::paginate(3); // '3'表示每页显示3条记录

        return view('student.index', [
            'students' => $students,
        ]);
    }
}
```

	在需要用到分页的视图里，直接` \{{ $students->render() \}}`就行了，这条语句会自动生成含有`ul`和`li`的分页信息的。

```php
<!--student.index视图的分页内容-->
	<!--分页-->
    <div class="pull-right">
        \{{ $students->render() \}}
    </div>
```

3. 默认选中项

```php
<ul class="nav nav-pills nav-stacked">
<li role="presentation" class="\{{ Request::getPathInfo() == '/student/index' ? 'active' : '' \}}"><a href="\{{ url('student/index') \}}">学生列表</a></li>
<li role="presentation" class="\{{ Request::getPathInfo() == '/student/create' ? 'active' : '' \}}"><a href="\{{ url('student/create') \}}">新增学生</a></li>
</ul>
```

用`Request::getPathInfo()`判断当前路径是否`/student/index`或者`/student/create`，是的话那就`active`,表示选中，不然就为空` `，不选中。注意`/student/index`和`/student/create`最前面的`/`是要有的。

4. 表单提交

* 提交到`save()`:

```php
<form action="\{{ url('student/save') \}}" method="POST"> 
    <!-- 1.设置action路径为'student/save',即提交到student/save -->

    <label for="inputName" >姓名：</label>
        <input type="text" name="Student[name]" id="inputName" placeholder="请输入姓名"> 
        <!-- 2.将各input的name属性都设为统一的数组，即统一都为Student的数组，只是下标不一样 -->

    <label for="inputAge">年龄：</label>
        <input type="text" name="Student[age]" id="inputAge" placeholder="请输入年龄">

    <div>
        <label>性别：</label>
        <div>
            <label>
                <input type="radio" name="Student[sex]" value="man">男
            </label> <!-- 3.注意radio的话可以这么设置，设两次Studnet[sex] -->
            <label>
                <input type="radio" name="Student[sex]" value="woman">女
            </label>
        </div>
    </div>
    <button type="submit">提交</button>
</form>
```

	添加一条路由：

```php
Route::any('student/save', ['uses' => 'StudentController@save']);
```

	在控制器中添加save():

```php
public function save(Request $request){
    $data = $request->input('Student');

    $student = new Student();
    $student->name = $data['name'];
    $student->age = $data['age'];
    $student->sex = $data['sex'];

    if($student->save()) {
        return redirect('student/index');
    } else {
        return redirect()->back();
    }
```

* 提交到当前页面

```php
<form action="" method="POST"> 
    <!-- 1.action没设置，默认提交到当前页面 -->

    <label for="inputName" >姓名：</label>
        <input type="text" name="Student[name]" id="inputName" placeholder="请输入姓名"> 
        <!-- 2.将各input的name属性都设为统一的数组，即统一都为Student的数组，只是下标不一样 -->

    <label for="inputAge">年龄：</label>
        <input type="text" name="Student[age]" id="inputAge" placeholder="请输入年龄">

    <div>
        <label>性别：</label>
        <div>
            <label>
                <input type="radio" name="Student[sex]" value="man">男
            </label> <!-- 3.注意radio的话可以这么设置，设两次Studnet[sex] -->
            <label>
                <input type="radio" name="Student[sex]" value="woman">女
            </label>
        </div>
    </div>
    <button type="submit">提交</button>
</form>
```

	不用添加一条路由，只是注意当前页面路由要能有POST方法：

```php
Route::any('student/create', ['uses' => 'StudentController@create']);
```

	在控制器中修改create():

```php
public function create(Request $request){
    if ($request->isMethod('POST')) { // 添加这个判断
        $data = $request->input('Student');
        if (Student::create($data)) { // 调用create()会采用批量赋值，所以要确保model中要有protected $fillable
            return redirect('student/index');
        } else {
            return redirect()->back();
        }
    }

    return view('student.create'); // 不是POST方法的话，就直接跳转到create视图中去
}
```

5. 操作提示

创建一个提示信息子视图：

```php
<!--message.blade.php-->
@if (Session::has('success'))
<!--成功提示框-->
<div class="alert alert-success alert-dismissable" role="alert">
    <button type="button" class="close" data-dismiss="alert" aria-label="Close">
        <span aria-hidden="true">&times;</span>
    </button>
    <strong>成功!!</strong>\{{ Session::get('success') \}}！
</div>
@endif
@if (Session::has('error'))
<!--失败提示框-->
<div class="alert alert-danger alert-dismissable" role="alert">
    <button type="button" class="close" data-dismiss="alert" aria-label="Close">
        <span aria-hidden="true">&times;</span>
    </button>
    <strong>失败!!</strong>\{{ Session::get('error') \}}！
</div>
@endif
```

位置：![2018-08-07_200359](/assets/images/laravel-develop-study/2018-08-07_200359.png)

哪个视图需要这个信息提示框就直接`@include('common.message')`过去。

控制器中使用：

```php
public function create(Request $request){
    if ($request->isMethod('POST')) {
        $data = $request->input('Student');
        if (Student::create($data)) {
            return redirect('student/index')->with('success', '添加成功');
            // 在控制器中调用暂存数据的方法，只能访问一次
        } else {
            return redirect()->back();
        }
    }
```

**这样，当数据保存成功然后返回的index页面时，就会向`session`中注入`success`的属性信息，当`common.message`页面中判断`session`属性存在时，就会显示信息在有`@include('common.message')`的视图里。**

记住，一定要将需要`session`的路由加进到`web`中间件中：

```php
Route::group(['middleware' => ['web']], function () {
    Route::get('student/index', ['uses' => 'StudentController@index']);
    Route::any('student/create', ['uses' => 'StudentController@create']);
    Route::post('student/save', ['uses' => 'StudentController@save']);
});
```

中间件`web`还能防止xxs攻击，所以，如果路由里有表单提交的话，一定要在表单视图中加入`\{{ csrf_field() \}}`。

```php
<!--create.blade.php-->
@section('content')
<form action="\{{ url('student/save') \}}" method="POST">

    \{{ csrf_field() \}} <!--防止xxs攻击-->

    <label for="inputName" >姓名：</label>
        <input type="text" name="Student[name]" id="inputName" placeholder="请输入姓名"> 

    <label for="inputAge">年龄：</label>
        <input type="text" name="Student[age]" id="inputAge" placeholder="请输入年龄">

    <button type="submit">提交</button>
</form>
@stop
```

6. 表单数据验证

* 控制器验证

```php
public function create(Request $request){
    if ($request->isMethod('POST')) {

        $this->validate($request, [
            'Student.name' => 'required|min:2|max:5',// 数组形式要写成这样子Student.name <= Student[name]
            'Student.age' => 'required|integer|max:2',
            'Student.sex' => 'required|integer'
        ], [
            'required' => ':attribute 为必选项',
            'min' => ':attribute 长度不符合要求',
            'integer' => ':attribute 必须为整数',
            'max' => ':attribute 长度不符合要求',
        ], [
            'Student.name' => '姓名',
            'Student.age' => '年龄',
            'Student.sex' => '性别',
        ]);


        $data = $request->input('Student');
        if (Student::create($data)) { // 调用create()会采用批量赋值，所以要确保model中要有protected $fillable
            return redirect('student/index')->with('success', '添加成功');
        } else {
            return redirect()->back();
        }
    }
```

验证通过是，程序将会继续往下执行，不通过时，表单将会重定向到上个页面并将错误抛给`session`，该错误属性是`$errors`，这个`$errors`是个数组，可以在全局的视图中捕获的。

然后，自定义错误内容：

```php
$this->validate($request, [
    'Student.name' => 'required|min:2|max:5',// 数组形式要写成这样子Student.name <= Student[name]
    'Student.age' => 'required|integer|max:2',
    'Student.sex' => 'required|integer'
], [
    'required' => ':attribute 为必选项', // :attribute是个占位符，表示对应的Student.name、Student.age、Student.sex
    'min' => ':attribute 长度不符合要求',
    'integer' => ':attribute 必须为整数',
    'max' => ':attribute 长度不符合要求',
], [
    'Student.name' => '姓名',
    'Student.age' => '年龄',
    'Student.sex' => '性别',
]);
```

	譬如：当因为`Student.name`的`required`不通过验证时，就会抛出`姓名 为必选项`。

![2018-08-07_210700](/assets/images/laravel-develop-study/2018-08-07_210700.png)

	如果不这样自定义的话，那抛出来的错误内容信息就是`Student.name is required.`，这个不太友好。

将用于捕获验证错误信息的程序放入一个视图：

```php
// common.validator.blade.php
@if (count($errors))
    <div class="alert alert-danger">
        <ul>
            @foreach($errors->all() as $error) // 将所有的错误都输出
            <li>\{{ $error \}}</li>
            @endforeach
        </ul>
    </div>
@endif
```

哪个视图需要输出验证错误信息的再来`@include('common.validator')`:

```php
@section('content')

    @include('common.validator') <!--需要输出验证信息的地方-->

    <form action="\{{ url('student/save') \}}" method="POST">
        \{{ csrf_field() \}}
        <label for="inputName" >姓名：</label>
            <input type="text" name="Student[name]" id="inputName" placeholder="请输入姓名"> 

        <label for="inputAge">年龄：</label>
            <input type="text" name="Student[age]" id="inputAge" placeholder="请输入年龄">

        <button type="submit">提交</button>
    </form>
@stop
```

* Validator类验证

```php
public function create(Request $request){
    if ($request->isMethod('POST')) {
        
        $validator = \Validator::make($request->input(), [
            'Student.name' => 'required|min:2|max:5',
            'Student.age' => 'required|integer|max:2',
            'Student.sex' => 'required|integer'
        ], [
            'required' => ':attribute 为必选项',
            'min' => ':attribute 长度不符合要求',
            'integer' => ':attribute 必须为整数',
            'max' => ':attribute 长度不符合要求',
        ], [
            'Student.name' => '姓名',
            'Student.age' => '年龄',
            'Student.sex' => '性别',
        ]);
        if ($validator->fails()) { // 这种方法验证也就是手动验证,在函数体里面还能做其他的事
            return redirect()->back()->withErrors($validator);
        } // 注意要用withErrors($validator)注册错误信息

        $data = $request->input('Student');
        if (Student::create($data)) { // 调用create()会采用批量赋值，所以要确保model中要有protected $fillable
            return redirect('student/index')->with('success', '添加成功');
        } else {
            return redirect()->back();
        }
    }

    return view('student.create');
}
```

在视图中调用指定的错误信息：`\{{ $errors->first('Student.name') \}}`,如果有自定义错误内容`姓名 为必选项`，则输出的是错误对应（`Student.name`）的自定义内容。

7. 数据保持

只需要在上述表单验证代码中加入`->withInput()`:

![2018-08-07_222555](/assets/images/laravel-develop-study/2018-08-07_222555.png)

`withInput()`自动默认将`$request`作为参数传进去，然后再在需要的`input`组件添加`value="\{{ old('Student')['name'] \}}"`即可：

```php
<input type="text" value="\{{ old('Student')['name'] \}}" name="Student[name]" class="form-control" id="inputName" placeholder="请输入姓名">
```

这样子，在提交表单而发生错误后，重定向到原先的表单填写页面时，它会自动补全在`input`之前填过的信息：![2018-08-07_223016](/assets/images/laravel-develop-study/2018-08-07_223016.png)

**注：**

`min:2|max:5`：
当要验证的值为数字时，那么这个数字要大于等于`2`小于等于`5`（`4`满足要求）；
当要验证的值为字符串，那么这个字符串不管是中英混合，还是全英，还是全文，它的长度要大于等于`2`小于等于`5`（`hh哈哈`长度为4，满足要求）。

8. 自定义数据库取出来的值

譬如，当存储性别时（有’未知‘，’男‘， ’女‘）,数据库真正所对应存储的是10， 20， 30。所以这时候就要自定义数据库取出来的值。

首先，在对应的model中写入一个函数：

```php
// App\Student.php
<?php

namespace App;

use Illuminate\Database\Eloquent\Model;

class Student extends Model
{
    protected $fillable = ['name', 'age', 'sex'];

    protected $table = 'student';

    public $timestamps = true;

    protected function getDateFormat()
    {
        return time();
    }
    protected function asDateTime($value)
    {
        return $value;
    }

    // 以下函数能将数字转化为对应的汉字，数字用来存储，汉字用来显示
    const SEX_UN = 10; // 定义三个常量
    const SEX_BOY = 20;
    const SEX_GIRL = 30;

    public function sex($ind = null) {
        $arr = [
            self::SEX_UN => '未知',
            self::SEX_BOY => '男',
            self::SEX_GIRL => '女',
        ];
        if ($ind !== null) { // 注意不等于是 !==
            return array_key_exists($ind, $arr) ? $arr[$ind] : $arr[self::SEX_UN];
        }
        return $arr;
    }

}
```

`Studen`这个model里有个`sex`函数，`sex()`时能将所有的性别取出来，传入相应的`index`时能取出对应的汉字性别。

接着，在控制器中将model注入到视图中去。

```php
public function create(){
    $student = new Student(); //先将model实例化
    return view('student.create', [
        'student' => $student // 然后再注入到视图里
    ]);
}
```

然后，在视图中就可以调用model的性别转化函数`sex()`。

```php
@foreach($students as $student)
    <tr>
        <td>\{{ $student->id \}}</td>
        <td>\{{ $student->name \}}</td>
        <td>\{{ $student->age \}}</td>
        <td>\{{ $student->sex($student->sex) \}}</td>
    </tr> <!--储存到model中的性别是个数字，$student->sex是个数字，$student->sex()才将这个数字转化对应性别为中文汉字-->
@endforeach
```

```php
@foreach($student->sex() as $ind=>$val)
    <label class="radio-inline"> <!--sex()返回一个数组，$ind是10,20,30,$val是未知，男，女-->
        <input type="radio" name="Student[sex]" value="\{{ $ind \}}">&nbsp;\{{ $val \}}
    </label> <!--最后提交到数据库是，如果是未知，那Student[sex]=10，男：Student[sex]=10等-->
@endforeach
```

	上面这样写就有这个效果：![2018-08-08_104915](/assets/images/laravel-develop-study/2018-08-08_104915.png)，就不必在页面上写很多个`input`标签了。

9. 遇到的坑：`App\Student::sex must return a relationship instance`

情况：

	在控制器中,当访问`student.create`时，会以这样注入一个model实例的方式：

```php
public function create(){
    $student = new Student();
    return view('student.create', [
        'student' => $student,
    ]);
}
```

	使得`create`视图里的`input`组件不用写多个，也能变成：![2018-08-08_104915](/assets/images/laravel-develop-study/2018-08-08_104915.png)

```php
@foreach($student->sex() as $ind=>$val)
    <label class="radio-inline">
    	<input type="radio" name="Student[sex]" value="\{{ $ind \}}">&nbsp;\{{ $val \}}
	</label>
@endforeach
```

	但是，`create`视图的这个部分其实也是`@include('student._form')`的，上面 的`input`标签也是放在这个通用的`_form`视图里的。所以实际上`_form.blade.php`：

```php
@foreach($student->sex() as $ind=>$val)
    <label class="radio-inline">
    	<input type="radio" name="Student[sex]" value="\{{ $ind \}}"
\{{ isset($student->sex) && ($student->sex == $ind) ? 'checked' : '' \}}
>&nbsp;\{{ $val \}}
	</label>
@endforeach	
```

`\{{ isset($student->sex) && ($student->sex == $ind) ? 'checked' : '' \}}`的意思是，如果控制器注入了一个`Student`实例，那么判断这个实例的`sex`有没有被设置，有的话，就判断`$student->sex`这个值和`$ind`相不相等，相等的话，那就这个`input`默认被选中。相当于，能指定一个`input`默认被选中。

然而，如果控制器仅仅：

```php
$student = new Student();
return view('student.create', [
    'student' => $student,
]);
```

视图直接用`$student->sex`，不管用在哪里，都会报错。故此，一定要在控制器添加：`$student->sex = null;`:

```php
$student = new Student();
$student->sex = null; // 等于不赋值给$student->sex
return view('student.create', [
    'student' => $student,
]);
```

这样，在视图：

```php
\{{ isset($student->sex) && ($student->sex == $ind) ? 'checked' : '' \}}
```

先判断`$student->sex`有没有被设置再来做其他事情。

10. 视图中url传值：

```php
\{{ url('student/update', ['id' => $student->id]) \}}
```

# 三、Laravel简单操作技巧

## 1.Composer

### 1.包管理器

![2018-08-08_164522](/assets/images/laravel-develop-study/2018-08-08_164522.png)

### 2.Composer

![2018-08-08_164723](/assets/images/laravel-develop-study/2018-08-08_164723.png)

### 3.安装

![2018-08-10_224648](/assets/images/laravel-develop-study/2018-08-10_224648.png)

![2018-08-10_224728](/assets/images/laravel-develop-study/2018-08-10_224728.png)

### 4.镜像

![2018-08-10_224851](/assets/images/laravel-develop-study/2018-08-10_224851.png)

使用[Composer中国全量镜像服务](https://www.phpcomposer.com)作为本地项目的依赖管理工具的下载中心会更快。

### 5.使用Composer

```shell
# 创建配置文件以及初始化
composer init

# 搜索某个库
composer search monolog

# 查看库的信息
composer show --all monolog/monolog
```

添加库：

在配置文件`composer.json`中添加依赖和版本：

```shell
"require": {
    "monolog/monolog": "2.21.*"
}
```

	然后用`composer install`下载依赖，之后打开`vendor`目录，库将会下载在里面。

也可以用`composer require`声明依赖，它也会自动添加、下载、安装依赖：`composer require symfony/http-foundation`。

删除依赖：只需在`composer.json`删除对应的依赖，然后执行`composer update`即可。

### 6.使用Composer安装Laravel

- `composer create-project --prefer-dist laravel/laravel <别名>`
- 先安装Laravel安装器:`composer global require "laravel/installer"`, 再通过安装器安装框架：`laravel new blog`

## 2.Artisan

![1533975220842](/assets/images/laravel-develop-study//assets/images/laravel-develop-study/1533975220842.png)

![1533975343503](/assets/images/laravel-develop-study/1533975343503.png)

![1533975353745](/assets/images/laravel-develop-study/1533975353745.png)

### 1.用户认证(Auth)

#### 1. 生成Auth所需文件

	命令：

```shell
php artisan make:auth
```

	生成的路由内容：

```php
<?php
Auth::routes();

Route::get('/home', 'HomeController@index')->name('home');
```

`Auth::routes()`位置：`\vendor\laravel\framework\src\Illuminate\Routing\Router.php`的`auth`函数：

```php
    /**
     * Register the typical authentication routes for an application.
     *
     * @return void
     */
public function auth()
{
    // Authentication Routes...
    $this->get('login', 'Auth\LoginController@showLoginForm')->name('login');
    $this->post('login', 'Auth\LoginController@login');
    $this->post('logout', 'Auth\LoginController@logout')->name('logout');

    // Registration Routes...
    $this->get('register', 'Auth\RegisterController@showRegistrationForm')->name('register');
    $this->post('register', 'Auth\RegisterController@register');

    // Password Reset Routes...
    $this->get('password/reset', 'Auth\ForgotPasswordController@showLinkRequestForm')->name('password.request');
    $this->post('password/email', 'Auth\ForgotPasswordController@sendResetLinkEmail')->name('password.email');
    $this->get('password/reset/{token}', 'Auth\ResetPasswordController@showResetForm')->name('password.reset');
    $this->post('password/reset', 'Auth\ResetPasswordController@reset');
}
```

#### 2.数据迁移 --> 在数据库生成对应的表

![1534234217992](/assets/images/laravel-develop-study/1534234217992.png)

`Mysql`语句：

```mysql
CREATE TABLE IF NOT EXISTS students(
	'id' INT AUTO_INCREMENT PRIMARY KEY,
    'name' VARCHAR(255) NOT NULL DEFAULT '' COMMENT '姓名',
    'age' INT UNSIGNED NOT NULL DEFAULT 0 COMMENT '年龄',
    'sex' INT UNSIGNED NOT NULL DEFAULT 10 COMMENT '性别',
    'created_at' INT NOT NULL DEFAULT 0 COMMENT '新增时间',
    'updated_at' INT NOT NULL DEFAULT 0 COMMENT '修改时间'
)ENGINE=InnoDB DEFAULT CHARSET=UTF8
AUTO_INCREMENT=1001 COMMENT='学生表';
```

	完善迁移文件 --> **在`up`函数中添加数据表里的字段**：

```php
<?php

use Illuminate\Support\Facades\Schema;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Database\Migrations\Migration;

class CreateStudentsTable extends Migration
{
    /**
     * Run the migrations.
     *
     * @return void
     */
    public function up()
    {
        Schema::create('students', function (Blueprint $table) {
            $table->increments('id');
            $table->string('name'); // unsigned()表示非负的意思
            $table->integer('age')->unsigned()->default(0);
            $table->integer('sex')->unsigned()->default(10);
            $table->integer('created_at')->default(0);
            $table->integer('updated_at')->default(0);
            $table->timestamps();
        });
    }

    /**
     * Reverse the migrations.
     *
     * @return void
     */
    public function down()
    {
        Schema::dropIfExists('students');
    }
}
```

	将`database/migrations`下的迁移文件做迁移：

```shell
php artisan migrate
```

**迁移步骤：**

1. 新建迁移文件：`php artisan make:model Student -m`或者`php artisan make:migration create_students_table --create=students`。
2. 完善迁移文件，即在`up`函数里添加字段。
3. 做迁移：`php artisan migrate`

#### 3.数据填充 --> 一般填充测试数据

![1534235808674](/assets/images/laravel-develop-study/1534235808674.png)

1. 创建填充文件：`php artisan make:seeder StudentTableSeeder`:

![1534236147269](/assets/images/laravel-develop-study/1534236147269.png)

`DatabaseSeeder.php`：用于批量填充文件。

`StudentTableSeeder.php`：用于单个填充文件。

1. 执行填充文件

   - 单个填充文件：

     ```php
     // \database\seeds\StudentTableSeeder.php
     <?php
     
     use Illuminate\Database\Seeder;
     use Illuminate\Support\Facades\DB;
     
     class StudentTableSeeder extends Seeder
     {
         /**
          * Run the database seeds.
          *
          * @return void
          */
         public function run()
         {   
             // 导入两条数据
             DB::table('students')->insert([
                 ['name' => 'name1', 'age' => 23],
                 ['name' => 'name2', 'age' => 24],
             ]);
         }
     }
     ```

     执行：`php artisan db:seed --class=StudentTableSeeder`

   - 批量填充文件：

     ```php
     // \database\seeds\DatabaseSeeder.php
     <?php
     
     use Illuminate\Database\Seeder;
     
     class DatabaseSeeder extends Seeder
     {
         /**
          * Run the database seeds.
          *
          * @return void
          */
         public function run()
         {	// 将多个填充文件一起执行
             $this->call(StudentTableSeeder::class);
             $this->call(ArticleTableSeeder::class);
             $this->call(CommentTableSeeder::class);
         }
     }
     ```

     执行：`php artisan db:seed`

### 2.Laravel框架常用功能

#### 1.文件上传

![1534237010212](/assets/images/laravel-develop-study/1534237010212.png)

![1534237027967](/assets/images/laravel-develop-study/1534237027967.png)

配置文件：

```php
// config/filesystems.php
<?php
return [
	// 支持"local", "ftp", "s3", "rackspace"，默认使用本地端空间
    'default' => env('FILESYSTEM_DRIVER', 'local'), 

    'cloud' => env('FILESYSTEM_CLOUD', 's3'),
    
	// 磁盘
    'disks' => [
        'local' => [ // 本地端空间磁盘,名字叫local
            'driver' => 'local', // 驱动是本地端空间
            'root' => storage_path('app'), // 目录是storage/app
        ],
        'public' => [ // 本地端空间磁盘,名字叫public，因为驱动是本地端空间，所以它是本地端空间磁盘
            'driver' => 'local',
            'root' => storage_path('app/public'),
            'url' => env('APP_URL').'/storage',
            'visibility' => 'public',
        ],
        's3' => [ // 亚马逊的配置
            'driver' => 's3',
            'key' => env('AWS_KEY'),
            'secret' => env('AWS_SECRET'),
            'region' => env('AWS_REGION'),
            'bucket' => env('AWS_BUCKET'),
        ],
    ],
];
```

使用本地端空间来让laravel有文件上传的功能：

1. 在`config/filesystems.php`创建一个本地端空间磁盘，名字叫：uploads：

   ```php
   // config/filesystems.php
   <?php
   return [
       'default' => env('FILESYSTEM_DRIVER', 'local'), 
   
       'cloud' => env('FILESYSTEM_CLOUD', 's3'),
       
   	// 磁盘
       'disks' => [
           'local' => [ 
               'driver' => 'local', 
               'root' => storage_path('app'), 
           ],
           'public' => [ 
               'driver' => 'local',
               'root' => storage_path('app/public'),
               'url' => env('APP_URL').'/storage',
               'visibility' => 'public',
           ],
           'uploads' => [ // 创建了一个本地端空间磁盘，目录是storage/app/uploads
               'driver' => 'local',
               'root' => storage_path('app/uploads') // 现在这里进行配置，这个文件夹会自己生成
           ],
           's3' => [
               'driver' => 's3',
               'key' => env('AWS_KEY'),
               'secret' => env('AWS_SECRET'),
               'region' => env('AWS_REGION'),
               'bucket' => env('AWS_BUCKET'),
           ],
       ],
   ];
   ```

   位置：

   ![1534237760826](/assets/images/laravel-develop-study/1534237760826.png)

2. 控制器和路由：

   ```php
   // StudentController.php
   <?php
   
   namespace App\Http\Controllers;
   
   use App\Student;
   use Illuminate\Http\Request;
   use Illuminate\Support\Facades\Session;
   use Illuminate\Support\Facades\Storage;
   
   class StudentController extends Controller
   {
      public function upload(Request $request) {
          if ($request->isMethod('POST')) {
              // 获取上传来的文件
              $file = $request->file('source'); 
              
              if ($file->isValid()) {
                  // 判断文件是否上传成功
                  $originaName = $file->getClientOriginalName(); // 原文件名
                  $ext = $file->getClientOriginalExtension(); // 扩展名，后缀
                  $type = $file->getClientMimeType(); // 文件类型
                  $realPath = $file->getRealPath(); // 临时绝对路径，还没手动保存之前文件存放的位置
   
                  // 这种做法保证文件名称都不相同
                  $filename = date('Y-m-d-H-i-s').'-'.uniqid().'.'.$ext;
                  // 保存文件在config/filesystems.php中设置的disk里，返回一个bool，保存得成功不成功
                  $bool = Storage::disk('uploads')->put($filename, file_get_contents($realPath));
              }
          }
   
          return view("student.upload");
      }
   }
   ```

   ```php
   // web.php
   Route::get('/home', 'HomeController@index')->name('home');
   ```

3. 视图里要提交文件的表单：

   ```php
   // resources/views/student/upload.blade.php
   <div class="panel-body">
   	\{{--enctype="multipart/form-data"必须加这个属性，表单才可以使用文件上传功能--\}}
   	<form class="form-horizontal" method="POST" action="" enctype="multipart/form-data">
   		\{{ csrf_field() \}}
       	<div>
                <label for="file" class="col-md-4 control-label">请选择文件</label>
                <div class="col-md-6">		\{{--name值是source--\}}
                   <input id="file" type="file" class="form-control" name="source" required>
                </div>
            </div>
            <div class="form-group">
                <div class="col-md-8 col-md-offset-4">
                   <button type="submit" class="btn btn-primary">
                       确认上传
                   </button>
                </div>
             </div>
        </form>
   </div>
   ```

4. 可以通过更改`config/filesystems.php`里的`uploads`磁盘的空间为`public`目录底下的`uploads`目录。

![1534342816613](/assets/images/laravel-develop-study/1534342816613.png)

#### 2.发送邮件

![1534343099473](/assets/images/laravel-develop-study/1534343099473.png)

![1534343121043](/assets/images/laravel-develop-study/1534343121043.png)

	配置文件：

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

1. 在`.env`中进行配置：

```properties
MAIL_DRIVER=smtp # 使用的服务
MAIL_HOST=smtp.mailtrap.io # 服务器地址
MAIL_PORT=2525 # 服务器端口
MAIL_USERNAME=jim # 账号
MAIL_PASSWORD=passowrd
MAIL_ENCRYPTION=ssl # 协议
```

1. 控制器以及路由

```php
Route::any('mail', ['uses' => 'StudentController@mail']);
```

控制器：

- 以`raw`方式发送邮件：

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

- 以`html`方式发送邮件：

创建一个`html`文件，即视图：

```php
<!--resources/views/student/mail.blade.php-->
<!DOCTYPE html>
<html>
<head>
    <title>标题</title>
</head>
<body> <!--$name由控制器注入进来-->
<h1>Hello \{{ $name \}}</h1>
</body>
</html>
```

	控制器：

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

#### 3.缓存使用

![1534344890615](/assets/images/laravel-develop-study/1534344890615.png)

![1534344915362](/assets/images/laravel-develop-study/1534344915362.png)

![1534344930819](/assets/images/laravel-develop-study/1534344930819.png)

配置文件：

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

控制器：

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

	`add()`:添加。

```php
public function cache1() {
    // add(),如果对象已经存在,就添加失败，如果对象不存在，添加成功
    // 返回一个bool值,10是时间
    $bool = Cache::add('key1', 'val1', '10');
}
```

	`forever()`：永久的保存对象到缓存中。	

```php
public function cache1() {
    Cache::forever('key1', 'val1');
}
```

	`has()`:判断缓存中的一个`key`值存不存在。

```php
public function cache1() {
    if (Cache::has('key')) {
        $val = Cache::get('key')
    } else {
        echo "No"
    }
}
```

	`pull`:取缓存中的`key`值，然后删了这个`key`。

```php
public function cache1() {
    $val = Cache::pull('key');
}
```

	`forget()`:从缓存中删除对象，删除成功返回`true`，返回一个`bool`值。

```php
public function cache1() {
    $bool = Cache::forget('key');
}
```

#### 4.错误和日志

![1535095566213](/assets/images/laravel-develop-study/1535095566213.png)

![1535095599480](/assets/images/laravel-develop-study/1535095599480.png)

1. `debug`模式：开发模式，调试模式。

可在`.env`里开启和调试：

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

	默认是开启调试模式的，如果发生错误，`laravel`会在网页打印出错误栈。
	
	**上线了一定要关闭调试模式！！**

1. `http`异常

![1535096147008](/assets/images/laravel-develop-study/1535096147008.png)

自定义`http`异常：

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

`http`异常的视图位置：

`vendor\laravel\framework\src\Illuminate\Foundation\Exceptions\views`:

![1535098035926](/assets/images/laravel-develop-study/1535098035926.png)

1. 日志

![1535098224286](/assets/images/laravel-develop-study/1535098224286.png)

`config/app.php`：

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

	配置日志模式：

```php
# 在.env中进行配置
# APP_LoG原本的.env里是没有的，是自己添加的，只能配置"single", "daily", "syslog", "errorlog"这几种模式
APP_LoG=single 
APP_LOG_LEVEL=debug
```

	这样是会在![1535098804878](/assets/images/laravel-develop-study/1535098804878.png)这里生成日志文件:`laravel.log`。
	
	使用日志：

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

	`daily`的`log`模式，会每天生成一个日志：

![1535099439063](/assets/images/laravel-develop-study/1535099439063.png)



















[看到这里](https://www.imooc.com/video/13341)

























---
layout: post
title: Laravel学习笔记
---
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
\{{ $name \}} \{{ $age \}}
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

## 2.数据库操作

**Laravel提供了DB facade（原始查找）、查询构造器和Eloquent ORM三种操作数据库的方式。**

### 1.连接数据库(config/database.php + .env)

打开config/database.php,找到：

```php
// 表示默认要连接的数据库是mysql
'default' => env('DB_CONNECTION', 'mysql'),
```

再往下找到：

```php
// 下面的env(..., ...)其实就是根目录的.env文件里的信息
'mysql' => [
    'driver' => 'mysql',
    'host' => env('DB_HOST', '127.0.0.1'),
    'port' => env('DB_PORT', '3306'),
    'database' => env('DB_DATABASE', 'forge'),
    'username' => env('DB_USERNAME', 'forge'),
    'password' => env('DB_PASSWORD', ''),
    'unix_socket' => env('DB_SOCKET', ''),
    'charset' => 'utf8mb4',
    'collation' => 'utf8mb4_unicode_ci',
    'prefix' => '', // 表前缀
    'strict' => true,
    'engine' => null,
],
```

打开.env,找到:

```php
DB_CONNECTION=mysql
DB_HOST=127.0.0.1
DB_PORT=3306
DB_DATABASE=laravel5
DB_USERNAME=root
DB_PASSWORD=
```

数据库连接完成。

### 2.使用DB facade实现CURD

CURD：增删改查

```php
// App/Http/Controllers/ArticleController.php，控制器里操作数据库
<?php

namespace App\Http\Controllers;
use App\Article;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\DB;

class ArticleController extends Controller
{
    public function operate(){
        // 插入
        $bool = DB::insert('insert into student(name, age) value(?, ?)', ['Jim', 18]);
        var_dump($bool); // 返回插入成不成功的值，true或false
        
        // 更新
        $num = DB::update('update student set age = ? where name = ?', [20, 'Jim']);
        var_dump($num); // 返回修改的行数
        
        // 查询
        $students = DB::select('select * from student where id > ?', [1001]);
        dd($students); // 返回查询结果，是个数组
        
        // 删除
        $num = DB::delete('delete from student where id > ?', [1001]);
        var_dump($num); // 返回被删除的行数

    }
}
```

var_dump(), dd()，都是调试代码，都能将()里的东西打印出来。

### 3.查询构造器

#### 1.新增数据

```php
// App/Http/Controllers/HomeController.php
public function query(){
        // 插入成功返回一个布尔值
        $bool = DB::table('student')->insert(
            ['name' => 'Jim', 'age' =>  18]
        );
        // 插入成功返回插入的id
        $id = DB::table('student')->insertGetId(
            ['name' => 'Jim', 'age' => 18]
        );
        // 插入多条数据
        $id = DB::table('student')->insert(
            ['name' => 'name1', 'age' => 18],
            ['name' => 'name2', 'age' => 18],
            ['name' => 'name3', 'age' => 18],
            ['name' => 'name4', 'age' => 18]
        );
    }
```

#### 2.更新数据

```php
// App/Http/Controllers/HomeController.php   
public function query(){
        // 将student表中id=2的元组中的age更新为30，返回的是受影响的行数
        $num = DB::table('student')
            ->where('id', 12) // 更新数据一定要带条件
            ->update(['age' => 30]);
        // 自增和自减
        $num = DB::table('student')->increment('age'); // 默认自增1
        $num = DB::table('student')->increment('age', 3); // 自增3
        $num = DB::table('student')->decrement('age'); // 默认自减1
        $num = DB::table('student')->decrement('age', 3); // 自减3
        // 将student表中id=12的元组的age自增3，同时name改为Jim
        $num = DB::table('student')
            ->where('id', 12)
            ->decrement('age', 3, ['name' => 'Jim']);
    }
```

#### 3.删除数据 

```php
// App/Http/Controllers/HomeController.php    
public function query(){
        // 删除student表中id=12的元组，返回受影响的行数
        $num = DB::table('student')
            ->where('id', 12)
            ->delete();
        // 删除student表中id>=12的元组，返回受影响的行数
        $num = DB::table('student')
            ->where('id', '>=', 12)
            ->delete();
        // 删除表，不返回任何东西
        DB::table('student')->truncate();
    }
```

#### 4.查询数据

get(), first(), where(), pluck(), lists(), select(), chunk().

```php
// App/Http/Controllers/HomeController.php  
public function query(){
        // get(),返回的是所有的表数据，一个列表
        $student = DB::table('student')->get();
        // first(),返回的是第一条记录
        $student = DB::table('student')->first();
        $student = DB::table('student') // 以student表的id进行倒序排序，获取第一条数据
            ->orderBy('id','desc')
            ->first();
        // where()
        $student = DB::table('student')
            ->where('id', '>=', 122)
            ->get();
        $student = DB::table('student') // 加多个条件查询
            ->whereRaw('id >= ? and age > ?', [122, 34])
            ->get();
        // pluck(),返回字段,是个列表
        $student = DB::table('student') // 返回student表的name字段
        ->pluck('name');
        // lists(),返回字段
        $student = DB::table('student') // 返回student表的name字段
        ->lists('name');
        $student = DB::table('student') // 返回student表的name字段
        ->lists('name', 'id');          // 但是这个列表中的索引用的是id
        // select()，返回的是指定的字段
        $name = DB::table('student')
            ->select('id', 'name', 'age')
            ->get();
        // chunk()，有时候数据太多，一次性获取会太慢，所以就要分段进行获取
        $name = DB::table('student')->chunk(50, function ($student){ // 每次获取50条元组，这50条元组赋值给闭包中的$student
            if( <条件> ){       // 当满足条件的时候，就会返回false，一旦返回false，程序就停止查询，所以可以通过设定条件让程序只查询几次就可以了
                return false;
            }
        });
    }
```

#### 5.聚合函数

count(), avg(), max(), sum(), min().

```php
// App/Http/Controllers/HomeController.php 
public function query(){
        // 返回元组的个数
        $sum = DB::table('student')->count();
        // 返回student表中age字段的最大值
        $sum = DB::table('student')->max('age');
        // 返回student表中age字段的最小值
        $sum = DB::table('student')->min('age');
        // 返回student表中age字段的值的平均值
        $sum = DB::table('student')->avg('age');
        // 返回student表中age字段的值的总和
        $sum = DB::table('student')->sum('age');
    }
```

### 4.Eloauent ORM

在laravel中用model跟数据库中的表进行交互，laravel自带的Eloquent ORM用来实现数据库操作。

#### 1.创建model

在App下面创建一个Student的model类：

```php
<?php

namespace App;

use Illuminate\Database\Eloquent\Model;

class Student extends Model
{
    // 指定表名，没有指定的话，默认为该模型的复数即students
    protected $table = 'student';

    // 指定主键，默认是表中的id字段
    protected $primaryKey = 'id';

}
```

这样，一个model就创建好了。

#### 2.使用model

在model对应的controller中使用model。

```php
<?php

namespace App\Http\Controllers;

class StudentController
{
    public function orm() {
        // all(),查询表的所有记录，返回一个集合collection
        $students = Student::all();
        // 返回id为12的元组
        $student = Student::find(12);
        // findOrFail(),根据指定查找，如果没有找到，返回异常
        $student = Student::findOrFail(12); // id为12的元组找不到就报错
    }
}
```

在ORM中使用查询构造器：

```php
<?php

namespace App\Http\Controllers;

class StudentController
{
    public function orm() {
        // 查询所有，返回一个集合collection
        $student = Student::get();
        
        $student = Student::where('id', '>', '34')
            ->orderBy('age', 'desc')
            ->first();
        
        Student::chunk(2, function($stuent){
            var_dump($student);
        });
        
        $num = Student::count();
        
        $max = Student::where('id', '>', 1002)->max('age');
              
    }
}
```

#### 3. 自定义时间戳及批量赋值

```php
// Student model
// App/Student.php
<?php

namespace App;


use Illuminate\Database\Eloquent\Model;

class Student extends Model
{
    // 指定表名，没有指定的话，默认为该模型的复数即students
    protected $table = 'student';

    // 指定主键，默认是表中的id字段
    protected $primaryKey = 'id';

    // 一般情况下模型对象向数据库增加数据时还会附加一个时间戳，
    // 如果不想要，在这里将$timestamps设置为false即可
    protected $timestamps = true;
    // 该函数与上面的$timestamps=true结合在一起给增添的字段附加一个时间戳
    protected function getDateFormat()
    {
        return time(); // 返回给我们的时间将会是格式化好的
    }
    // 如果我们不想格式化，让模型给我们返回一个时间戳（我们自己之后利用
    // 这个时间戳做自己想做的事。用下面这个函数：
    protected function asDateTime($value)
    {
        return $value;
    }
}
```

```php
// 在StudentConller这个控制器中操纵Student这个model
// App/Http/Controllers/StudentConller.php
<?php

namespace App\Http\Controllers;


class StudentController
{
    public function orm() {

        $student = new Student();
        $student->name = 'Jim';
        $student->age = 12;
        $bool = $student->save(); // 保存数据到数据库直接这样就行，返回一个bool
        // $student->created_at会返回一个时间戳，这个已经在Student这个model设置好了
        // 然后我们用这个时间戳自己再来格式化并打印
        echo data('Y-m-d H:i:s', $student->created_at);
    }
}
```

批量赋值数据：

```php
// App/Http/Controllers/StudentConller.php
<?php

namespace App\Http\Controllers;


class StudentController
{
    public function orm() {
		// 使用create()新增数据
        $student = Student::create(
        	['name' => 'Jim', 'age' => 23]
        );
    }
}
```

```php
// App/Student.php
<?php

namespace App;

use Illuminate\Database\Eloquent\Model;

class Student extends Model
{    // 指定允许批量赋值的model的字段，然后controller里就可以
    // 用model的create()批量赋值数据
    protected $fillable = ['name', 'age'];

    // 指定不允许批量赋值的model的字段
    protected $guarded = [];
}
```

其他新增数据的方法：

```php
// 以字段查找某个元组，如果没有那就创建
$student = Student::firstOrCreate(
    ['name' => 'Jim']
);

// 以字段查找某个元组，如果没有那就创建
$student = Student::firstOrNew(
    ['name' => 'Jim']
);
// firstOrNew是不会将数据保存数据库的，如果需要保存，
// 则自己编写以下的保存代码,返回是个bool，即保存成不成功
$bool = $student->save();
```

#### 4.修改数据

```php
// App/Http/Controllers/StudentConller.php
<?php

namespace App\Http\Controllers;

use App\Student;

class StudentController
{
    public function orm() {
        // 1.通过模型更新数据，返回的$bool代表保存得成不成功
        $student = Student::find(2021);
        $student->name = 'Jim';
        $bool = $student->save();
        // 2.利用查询语句来更新数据
        $num = Student::where('id', '>', 120)
            ->update(
                ['age' => 23]
            );
    }
}
```

#### 5.删除数据

```php
public function orm() {
    // 1.通过模型删除,返回一个代表删除成不成功的$bool
    $student = Student::find(201);
    $bool = $student->delete(); // 删除不到这个元组就会报错

    // 2.通过主键删除,返回删除的行数，即一个删除了几行
    $num = Student::destroy(1021);
    // 删除多个id的元组：
    $num = Student::destroy(1021, 33);
    // 或者：
    $num = Student::destroy([2021, 33]);

    // 3.通过查询语句删除,返回删除的行数
    $num = Student::where('id', '>', 23)->delete();
}
```

## 3.Blade模板

### 1.模板继承

![20180805224923.png](/assets/images/laravel-develop-study/20180805224923.png)

父模板(views.layouts)：

```php
// resources/views/layouts.blade.php
\{{--@section,展示片段内容--\}}
@section('header')
    头部
@show

@section('sidebar')
    侧边栏
@show

\{{--@yield，展示字符串内容--\}}
@yield('content', '主要内容')
```

子模板(views.student.child):

```php
// resources/views/student/child.blade.php
\{{--1.继承哪个模板--\}}
@extends('layouts')

\{{--2.替换父模板中@section的header内容，输出父模板对应地方的父内容--\}}
@section('header')
    @parent
    header
@stop
\{{--或者--\}}
\{{--重写父模板中@section的sidebar内容，不会输出父模板对应地方的父内容--\}}
@section('sidebar')
    sidebar
@stop

\{{--3.替换父模板中@yield的content内容--\}}
@section('content')
    content
@stop
```

controller中访问的是子模板：

```php
// App/Http/Controllers/StudentController.php
<?php

namespace App\Http\Controllers;


use App\Student;

class StudentController
{
    public function view() {
        return view('student.child'); // 访问views目录底下的student/child.blade.php
    }
}
```

### 2.基础语法：

```php
\{{--resources/views/student/child.blade.php--\}}
\{{--1.模板中输出PHP变量，该变量由控制器传入--\}}
\{{ $name \}}

\{{--2.模板中调用PHP代码,$name和$arr两个变量都由控制器中传进来--\}}
\{{ time() \}}
\{{ date('Y-m-d H:i:s', time()) \}}
\{{--判断$arr数组中是否有$name,有返回true，没有返回false--\}}
\{{ in_array($name, $arr) ? 'ture': 'false' \}}
\{{--判断$name是否存在,有返回$name值，没有返回字符串'default'--\}}
\{{ isset($name) ? $name: 'default' \}}
\{{--或者--\}}
\{{ $name or 'default' \}}

\{{--3.原样输出，视图渲染时输出\{{ $name \}}--\}}
@\{{ $name \}}

\{{--4.模板注释--\}}
\{{--xxxx--\}}

\{{--5.子模板中引入子视图--\}}
@include('student.common')
\{{--子视图中有占位符$msg,在这里将msg赋值并传给子视图--\}}
@include('student.common', ['msg' => 'error'])
```

控制器传入值：

```php
class StudentController
{
    public function view() {
        $name = 'Jim';
        $arr = ['a', 'b'];
        return view('student.child', [
            'name' => $name, // 传入值
            'arr' =>$arr, // 传入数组
        ]);
    }
}
```

子视图：

```php
\{{--resources/views/student/common.blade.php--\}}
\{{--$msg是个占位符，等着别处传过来值给它赋值--\}}
\{{ $msg \}}
```

### 3.模板中流程控制

```php
\{{--resources/vies/student/child.blade.php--\}}

\{{--if--\}}
@if ($name == 'Jim')
    Jim
@elseif($name == 'a')
    a
@else
    b
@endif

\{{--unless,相当于if的取反--\}}
@unless( $name == 'Jim' )
    output Jim
@endunless

\{{--for--\}}
@for ($i=0; $i<2; $i++)
    <p>\{{ $i \}}</p>
@endfor

\{{--foreach,遍历对象列表或者数组--\}}
@foreach($students as $student) \{{--该$student对象列表由控制器传入--\}}
    <p>\{{ $student->name \}}</p> \{{--返回$student对象的name属性--\}}
@endforeach

\{{--forelse--\}}
@forelse($students as $student)
    <p>\{{ $student->name \}}</p>
@empty\{{--如果对象列表为空--\}}
    <p>null</p>
@endforelse
```

控制器中将对象数组传给视图：

```php
<?php

namespace App\Http\Controllers;

use App\Student;

class StudentController
{
    public function view() {
        $students = Student::get(); // 从model中获取所有的元组对象，组成一个对象列表
        $name = 'Jim';
        return view('student.child', [
            'name' => $name,
            'students' => $students,
        ]);
    }
}
```

### 4.模板中url

路由：

```php
// 路由名字：urlTest， 路由别名：urlAlias， 控制器及方法：StudentController@urlTest 
Route::any('urlTest', ['as' => 'urlAlias', 'uses' => 'StudentController@urlTest']);
```

模板中生成url：

```php
\{{--resources/views/student/child.blade.php--\}}
\{{--1.指定的路由名字--\}}
<a href="\{{ url('urlTest') \}}">This is url.</a>
\{{--2.控制器+方法名--\}}
<a href="\{{ action('StudentController@urlTest') \}}">This is url.</a>
\{{--3.路由的别名--\}}
<a href="\{{ route('urlAlias') \}}">This is url.</a>
```

# 二、laravel表单

## 1.request

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

## 2.session

session的配置文件在config/session.php中。

使用session的三种方法：

* HTTP request类的session()方法
* session()辅助函数
* Session facade

config/session.php部分解析：

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

**先在路由表中添加要使用session()的路由的web中间件：**

```php
// routes/web.php
Route::group(['middleware' => ['web']], function (){ // 用路由组的方式同时给session1和session2两个路由添加webs中间价
    Route::any('session1', ['uses' => 'StudentController@session1']);
    Route::any('session2', ['uses' => 'StudentController@session2']);
});
```

1.HTTP request的session()

先访问session1方法，会往session放入一个key，然后访问session2方法，会从session中取出key值。

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

2.直接session()

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

3.Session facade

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

其他用法：

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

## 3.response

响应的类型：字符串， 视图， Json， 重定向。

1. Json

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

2. 重定向

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

	或者：
	
	action(), 控制器+方法

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

	或者：
	
	route(), 路由别名

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

	或者：
	
	back(),返回上一个页面

```php
class StudentController
{
    public function response() {
        redirect()->back();
    }
}
```

## 4.Middleware

Laravel中间件提供了一个方便的机制来过滤进入应用程序的HTTP请求。

假设一个场景：有一个活动，指定日期开始前只能访问宣传页面，活动开始日期后才可以访问活动页面。

1. 新建控制器方法

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

2. 新建中间件

![2018-08-06_213029](/assets/images/laravel-develop-study/2018-08-06_213029.png)

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

	在Kernel.php中注册中间件:

![2018-08-06_213247](/assets/images/laravel-develop-study/2018-08-06_213247.png)

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

	如果想注册全局中间件，则在Kernel.php里的这里注册：

```php
protected $middleware = [
    \Illuminate\Foundation\Http\Middleware\CheckForMaintenanceMode::class,
    \Illuminate\Foundation\Http\Middleware\ValidatePostSize::class,
    \App\Http\Middleware\TrimStrings::class,
    \Illuminate\Foundation\Http\Middleware\ConvertEmptyStringsToNull::class,
    \App\Http\Middleware\TrustProxies::class,
];
```

3. 使用中间件(在路由文件中)

```php
// 访问活动页面就会跳入这个中间件
Route::group(['middleware' => ['activity']], function () {
    Route::any('activity_running', ['uses' => 'StudentController@activity_running']);
});
// 然后中间件根据判断就会重定向到这个路由
Route::any('activity_advertise', ['uses' => 'StudentController@activity_advertise']);
```

4. 其他

中间件有前置操作和后置操作。

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

## 5.表单案例笔记

1.静态资源路径：`\{{ asset() \}}`

```php
    <link href="\{{ asset('static/css/bootstrap.min.css') \}}" rel="stylesheet">
```

这个路径是相对于public文件夹下的，也就是文件位置：![2018-08-07_134524](/assets/images/laravel-develop-study/2018-08-07_134524.png)

2. 表单分页

   控制器下用`Student::paginate(num)`取得所有的数据，然后将数据再传给视图。

```php
<?php

namespace App\Http\Controllers;


use App\Student;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Session;

class StudentController extends Controller
{
    public function index() {
        $students = Student::paginate(3); // '3'表示每页显示3条记录

        return view('student.index', [
            'students' => $students,
        ]);
    }
}
```

	在需要用到分页的视图里，直接` \{{ $students->render() \}}`就行了，这条语句会自动生成含有`ul`和`li`的分页信息的。

```php
<!--student.index视图的分页内容-->
	<!--分页-->
    <div class="pull-right">
        \{{ $students->render() \}}
    </div>
```

3. 默认选中项

```php
<ul class="nav nav-pills nav-stacked">
<li role="presentation" class="\{{ Request::getPathInfo() == '/student/index' ? 'active' : '' \}}"><a href="\{{ url('student/index') \}}">学生列表</a></li>
<li role="presentation" class="\{{ Request::getPathInfo() == '/student/create' ? 'active' : '' \}}"><a href="\{{ url('student/create') \}}">新增学生</a></li>
</ul>
```

用`Request::getPathInfo()`判断当前路径是否`/student/index`或者`/student/create`，是的话那就`active`,表示选中，不然就为空` `，不选中。注意`/student/index`和`/student/create`最前面的`/`是要有的。

4. 表单提交

* 提交到`save()`:

```php
<form action="\{{ url('student/save') \}}" method="POST"> 
    <!-- 1.设置action路径为'student/save',即提交到student/save -->

    <label for="inputName" >姓名：</label>
        <input type="text" name="Student[name]" id="inputName" placeholder="请输入姓名"> 
        <!-- 2.将各input的name属性都设为统一的数组，即统一都为Student的数组，只是下标不一样 -->

    <label for="inputAge">年龄：</label>
        <input type="text" name="Student[age]" id="inputAge" placeholder="请输入年龄">

    <div>
        <label>性别：</label>
        <div>
            <label>
                <input type="radio" name="Student[sex]" value="man">男
            </label> <!-- 3.注意radio的话可以这么设置，设两次Studnet[sex] -->
            <label>
                <input type="radio" name="Student[sex]" value="woman">女
            </label>
        </div>
    </div>
    <button type="submit">提交</button>
</form>
```

	添加一条路由：

```php
Route::any('student/save', ['uses' => 'StudentController@save']);
```

	在控制器中添加save():

```php
public function save(Request $request){
    $data = $request->input('Student');

    $student = new Student();
    $student->name = $data['name'];
    $student->age = $data['age'];
    $student->sex = $data['sex'];

    if($student->save()) {
        return redirect('student/index');
    } else {
        return redirect()->back();
    }
```

* 提交到当前页面

```php
<form action="" method="POST"> 
    <!-- 1.action没设置，默认提交到当前页面 -->

    <label for="inputName" >姓名：</label>
        <input type="text" name="Student[name]" id="inputName" placeholder="请输入姓名"> 
        <!-- 2.将各input的name属性都设为统一的数组，即统一都为Student的数组，只是下标不一样 -->

    <label for="inputAge">年龄：</label>
        <input type="text" name="Student[age]" id="inputAge" placeholder="请输入年龄">

    <div>
        <label>性别：</label>
        <div>
            <label>
                <input type="radio" name="Student[sex]" value="man">男
            </label> <!-- 3.注意radio的话可以这么设置，设两次Studnet[sex] -->
            <label>
                <input type="radio" name="Student[sex]" value="woman">女
            </label>
        </div>
    </div>
    <button type="submit">提交</button>
</form>
```

	不用添加一条路由，只是注意当前页面路由要能有POST方法：

```php
Route::any('student/create', ['uses' => 'StudentController@create']);
```

	在控制器中修改create():

```php
public function create(Request $request){
    if ($request->isMethod('POST')) { // 添加这个判断
        $data = $request->input('Student');
        if (Student::create($data)) { // 调用create()会采用批量赋值，所以要确保model中要有protected $fillable
            return redirect('student/index');
        } else {
            return redirect()->back();
        }
    }

    return view('student.create'); // 不是POST方法的话，就直接跳转到create视图中去
}
```

5. 操作提示

创建一个提示信息子视图：

```php
<!--message.blade.php-->
@if (Session::has('success'))
<!--成功提示框-->
<div class="alert alert-success alert-dismissable" role="alert">
    <button type="button" class="close" data-dismiss="alert" aria-label="Close">
        <span aria-hidden="true">&times;</span>
    </button>
    <strong>成功!!</strong>\{{ Session::get('success') \}}！
</div>
@endif
@if (Session::has('error'))
<!--失败提示框-->
<div class="alert alert-danger alert-dismissable" role="alert">
    <button type="button" class="close" data-dismiss="alert" aria-label="Close">
        <span aria-hidden="true">&times;</span>
    </button>
    <strong>失败!!</strong>\{{ Session::get('error') \}}！
</div>
@endif
```

位置：![2018-08-07_200359](/assets/images/laravel-develop-study/2018-08-07_200359.png)

哪个视图需要这个信息提示框就直接`@include('common.message')`过去。

控制器中使用：

```php
public function create(Request $request){
    if ($request->isMethod('POST')) {
        $data = $request->input('Student');
        if (Student::create($data)) {
            return redirect('student/index')->with('success', '添加成功');
            // 在控制器中调用暂存数据的方法，只能访问一次
        } else {
            return redirect()->back();
        }
    }
```

**这样，当数据保存成功然后返回的index页面时，就会向`session`中注入`success`的属性信息，当`common.message`页面中判断`session`属性存在时，就会显示信息在有`@include('common.message')`的视图里。**

记住，一定要将需要`session`的路由加进到`web`中间件中：

```php
Route::group(['middleware' => ['web']], function () {
    Route::get('student/index', ['uses' => 'StudentController@index']);
    Route::any('student/create', ['uses' => 'StudentController@create']);
    Route::post('student/save', ['uses' => 'StudentController@save']);
});
```

中间件`web`还能防止xxs攻击，所以，如果路由里有表单提交的话，一定要在表单视图中加入`\{{ csrf_field() \}}`。

```php
<!--create.blade.php-->
@section('content')
<form action="\{{ url('student/save') \}}" method="POST">

    \{{ csrf_field() \}} <!--防止xxs攻击-->

    <label for="inputName" >姓名：</label>
        <input type="text" name="Student[name]" id="inputName" placeholder="请输入姓名"> 

    <label for="inputAge">年龄：</label>
        <input type="text" name="Student[age]" id="inputAge" placeholder="请输入年龄">

    <button type="submit">提交</button>
</form>
@stop
```

6. 表单数据验证

* 控制器验证

```php
public function create(Request $request){
    if ($request->isMethod('POST')) {

        $this->validate($request, [
            'Student.name' => 'required|min:2|max:5',// 数组形式要写成这样子Student.name <= Student[name]
            'Student.age' => 'required|integer|max:2',
            'Student.sex' => 'required|integer'
        ], [
            'required' => ':attribute 为必选项',
            'min' => ':attribute 长度不符合要求',
            'integer' => ':attribute 必须为整数',
            'max' => ':attribute 长度不符合要求',
        ], [
            'Student.name' => '姓名',
            'Student.age' => '年龄',
            'Student.sex' => '性别',
        ]);


        $data = $request->input('Student');
        if (Student::create($data)) { // 调用create()会采用批量赋值，所以要确保model中要有protected $fillable
            return redirect('student/index')->with('success', '添加成功');
        } else {
            return redirect()->back();
        }
    }
```

验证通过是，程序将会继续往下执行，不通过时，表单将会重定向到上个页面并将错误抛给`session`，该错误属性是`$errors`，这个`$errors`是个数组，可以在全局的视图中捕获的。

然后，自定义错误内容：

```php
$this->validate($request, [
    'Student.name' => 'required|min:2|max:5',// 数组形式要写成这样子Student.name <= Student[name]
    'Student.age' => 'required|integer|max:2',
    'Student.sex' => 'required|integer'
], [
    'required' => ':attribute 为必选项', // :attribute是个占位符，表示对应的Student.name、Student.age、Student.sex
    'min' => ':attribute 长度不符合要求',
    'integer' => ':attribute 必须为整数',
    'max' => ':attribute 长度不符合要求',
], [
    'Student.name' => '姓名',
    'Student.age' => '年龄',
    'Student.sex' => '性别',
]);
```

	譬如：当因为`Student.name`的`required`不通过验证时，就会抛出`姓名 为必选项`。

![2018-08-07_210700](/assets/images/laravel-develop-study/2018-08-07_210700.png)

	如果不这样自定义的话，那抛出来的错误内容信息就是`Student.name is required.`，这个不太友好。

将用于捕获验证错误信息的程序放入一个视图：

```php
// common.validator.blade.php
@if (count($errors))
    <div class="alert alert-danger">
        <ul>
            @foreach($errors->all() as $error) // 将所有的错误都输出
            <li>\{{ $error \}}</li>
            @endforeach
        </ul>
    </div>
@endif
```

哪个视图需要输出验证错误信息的再来`@include('common.validator')`:

```php
@section('content')

    @include('common.validator') <!--需要输出验证信息的地方-->

    <form action="\{{ url('student/save') \}}" method="POST">
        \{{ csrf_field() \}}
        <label for="inputName" >姓名：</label>
            <input type="text" name="Student[name]" id="inputName" placeholder="请输入姓名"> 

        <label for="inputAge">年龄：</label>
            <input type="text" name="Student[age]" id="inputAge" placeholder="请输入年龄">

        <button type="submit">提交</button>
    </form>
@stop
```

* Validator类验证

```php
public function create(Request $request){
    if ($request->isMethod('POST')) {
        
        $validator = \Validator::make($request->input(), [
            'Student.name' => 'required|min:2|max:5',
            'Student.age' => 'required|integer|max:2',
            'Student.sex' => 'required|integer'
        ], [
            'required' => ':attribute 为必选项',
            'min' => ':attribute 长度不符合要求',
            'integer' => ':attribute 必须为整数',
            'max' => ':attribute 长度不符合要求',
        ], [
            'Student.name' => '姓名',
            'Student.age' => '年龄',
            'Student.sex' => '性别',
        ]);
        if ($validator->fails()) { // 这种方法验证也就是手动验证,在函数体里面还能做其他的事
            return redirect()->back()->withErrors($validator);
        } // 注意要用withErrors($validator)注册错误信息

        $data = $request->input('Student');
        if (Student::create($data)) { // 调用create()会采用批量赋值，所以要确保model中要有protected $fillable
            return redirect('student/index')->with('success', '添加成功');
        } else {
            return redirect()->back();
        }
    }

    return view('student.create');
}
```

在视图中调用指定的错误信息：`\{{ $errors->first('Student.name') \}}`,如果有自定义错误内容`姓名 为必选项`，则输出的是错误对应（`Student.name`）的自定义内容。

7. 数据保持

只需要在上述表单验证代码中加入`->withInput()`:

![2018-08-07_222555](/assets/images/laravel-develop-study/2018-08-07_222555.png)

`withInput()`自动默认将`$request`作为参数传进去，然后再在需要的`input`组件添加`value="\{{ old('Student')['name'] \}}"`即可：

```php
<input type="text" value="\{{ old('Student')['name'] \}}" name="Student[name]" class="form-control" id="inputName" placeholder="请输入姓名">
```

这样子，在提交表单而发生错误后，重定向到原先的表单填写页面时，它会自动补全在`input`之前填过的信息：![2018-08-07_223016](/assets/images/laravel-develop-study/2018-08-07_223016.png)

**注：**

`min:2|max:5`：
当要验证的值为数字时，那么这个数字要大于等于`2`小于等于`5`（`4`满足要求）；
当要验证的值为字符串，那么这个字符串不管是中英混合，还是全英，还是全文，它的长度要大于等于`2`小于等于`5`（`hh哈哈`长度为4，满足要求）。

8. 自定义数据库取出来的值

譬如，当存储性别时（有’未知‘，’男‘， ’女‘）,数据库真正所对应存储的是10， 20， 30。所以这时候就要自定义数据库取出来的值。

首先，在对应的model中写入一个函数：

```php
// App\Student.php
<?php

namespace App;

use Illuminate\Database\Eloquent\Model;

class Student extends Model
{
    protected $fillable = ['name', 'age', 'sex'];

    protected $table = 'student';

    public $timestamps = true;

    protected function getDateFormat()
    {
        return time();
    }
    protected function asDateTime($value)
    {
        return $value;
    }

    // 以下函数能将数字转化为对应的汉字，数字用来存储，汉字用来显示
    const SEX_UN = 10; // 定义三个常量
    const SEX_BOY = 20;
    const SEX_GIRL = 30;

    public function sex($ind = null) {
        $arr = [
            self::SEX_UN => '未知',
            self::SEX_BOY => '男',
            self::SEX_GIRL => '女',
        ];
        if ($ind !== null) { // 注意不等于是 !==
            return array_key_exists($ind, $arr) ? $arr[$ind] : $arr[self::SEX_UN];
        }
        return $arr;
    }

}
```

`Studen`这个model里有个`sex`函数，`sex()`时能将所有的性别取出来，传入相应的`index`时能取出对应的汉字性别。

接着，在控制器中将model注入到视图中去。

```php
public function create(){
    $student = new Student(); //先将model实例化
    return view('student.create', [
        'student' => $student // 然后再注入到视图里
    ]);
}
```

然后，在视图中就可以调用model的性别转化函数`sex()`。

```php
@foreach($students as $student)
    <tr>
        <td>\{{ $student->id \}}</td>
        <td>\{{ $student->name \}}</td>
        <td>\{{ $student->age \}}</td>
        <td>\{{ $student->sex($student->sex) \}}</td>
    </tr> <!--储存到model中的性别是个数字，$student->sex是个数字，$student->sex()才将这个数字转化对应性别为中文汉字-->
@endforeach
```

```php
@foreach($student->sex() as $ind=>$val)
    <label class="radio-inline"> <!--sex()返回一个数组，$ind是10,20,30,$val是未知，男，女-->
        <input type="radio" name="Student[sex]" value="\{{ $ind \}}">&nbsp;\{{ $val \}}
    </label> <!--最后提交到数据库是，如果是未知，那Student[sex]=10，男：Student[sex]=10等-->
@endforeach
```

	上面这样写就有这个效果：![2018-08-08_104915](/assets/images/laravel-develop-study/2018-08-08_104915.png)，就不必在页面上写很多个`input`标签了。

9. 遇到的坑：`App\Student::sex must return a relationship instance`

情况：

	在控制器中,当访问`student.create`时，会以这样注入一个model实例的方式：

```php
public function create(){
    $student = new Student();
    return view('student.create', [
        'student' => $student,
    ]);
}
```

	使得`create`视图里的`input`组件不用写多个，也能变成：![2018-08-08_104915](/assets/images/laravel-develop-study/2018-08-08_104915.png)

```php
@foreach($student->sex() as $ind=>$val)
    <label class="radio-inline">
    	<input type="radio" name="Student[sex]" value="\{{ $ind \}}">&nbsp;\{{ $val \}}
	</label>
@endforeach
```

	但是，`create`视图的这个部分其实也是`@include('student._form')`的，上面 的`input`标签也是放在这个通用的`_form`视图里的。所以实际上`_form.blade.php`：

```php
@foreach($student->sex() as $ind=>$val)
    <label class="radio-inline">
    	<input type="radio" name="Student[sex]" value="\{{ $ind \}}"
\{{ isset($student->sex) && ($student->sex == $ind) ? 'checked' : '' \}}
>&nbsp;\{{ $val \}}
	</label>
@endforeach	
```

`\{{ isset($student->sex) && ($student->sex == $ind) ? 'checked' : '' \}}`的意思是，如果控制器注入了一个`Student`实例，那么判断这个实例的`sex`有没有被设置，有的话，就判断`$student->sex`这个值和`$ind`相不相等，相等的话，那就这个`input`默认被选中。相当于，能指定一个`input`默认被选中。

然而，如果控制器仅仅：

```php
$student = new Student();
return view('student.create', [
    'student' => $student,
]);
```

视图直接用`$student->sex`，不管用在哪里，都会报错。故此，一定要在控制器添加：`$student->sex = null;`:

```php
$student = new Student();
$student->sex = null; // 等于不赋值给$student->sex
return view('student.create', [
    'student' => $student,
]);
```

这样，在视图：

```php
\{{ isset($student->sex) && ($student->sex == $ind) ? 'checked' : '' \}}
```

先判断`$student->sex`有没有被设置再来做其他事情。

10. 视图中url传值：

```php
\{{ url('student/update', ['id' => $student->id]) \}}
```

# 三、Laravel简单操作技巧

## 1.Composer

### 1.包管理器

![2018-08-08_164522](/assets/images/laravel-develop-study/2018-08-08_164522.png)

### 2.Composer

![2018-08-08_164723](/assets/images/laravel-develop-study/2018-08-08_164723.png)

### 3.安装

![2018-08-10_224648](/assets/images/laravel-develop-study/2018-08-10_224648.png)

![2018-08-10_224728](/assets/images/laravel-develop-study/2018-08-10_224728.png)

### 4.镜像

![2018-08-10_224851](/assets/images/laravel-develop-study/2018-08-10_224851.png)

使用[Composer中国全量镜像服务](https://www.phpcomposer.com)作为本地项目的依赖管理工具的下载中心会更快。

### 5.使用Composer

```shell
# 创建配置文件以及初始化
composer init

# 搜索某个库
composer search monolog

# 查看库的信息
composer show --all monolog/monolog
```

添加库：

在配置文件`composer.json`中添加依赖和版本：

```shell
"require": {
    "monolog/monolog": "2.21.*"
}
```

	然后用`composer install`下载依赖，之后打开`vendor`目录，库将会下载在里面。

也可以用`composer require`声明依赖，它也会自动添加、下载、安装依赖：`composer require symfony/http-foundation`。

删除依赖：只需在`composer.json`删除对应的依赖，然后执行`composer update`即可。

### 6.使用Composer安装Laravel

- `composer create-project --prefer-dist laravel/laravel <别名>`
- 先安装Laravel安装器:`composer global require "laravel/installer"`, 再通过安装器安装框架：`laravel new blog`

## 2.Artisan

![1533975220842](/assets/images/laravel-develop-study//assets/images/laravel-develop-study/1533975220842.png)

![1533975343503](/assets/images/laravel-develop-study/1533975343503.png)

![1533975353745](/assets/images/laravel-develop-study/1533975353745.png)

### 1.用户认证(Auth)

#### 1. 生成Auth所需文件

	命令：

```shell
php artisan make:auth
```

	生成的路由内容：

```php
<?php
Auth::routes();

Route::get('/home', 'HomeController@index')->name('home');
```

`Auth::routes()`位置：`\vendor\laravel\framework\src\Illuminate\Routing\Router.php`的`auth`函数：

```php
    /**
     * Register the typical authentication routes for an application.
     *
     * @return void
     */
public function auth()
{
    // Authentication Routes...
    $this->get('login', 'Auth\LoginController@showLoginForm')->name('login');
    $this->post('login', 'Auth\LoginController@login');
    $this->post('logout', 'Auth\LoginController@logout')->name('logout');

    // Registration Routes...
    $this->get('register', 'Auth\RegisterController@showRegistrationForm')->name('register');
    $this->post('register', 'Auth\RegisterController@register');

    // Password Reset Routes...
    $this->get('password/reset', 'Auth\ForgotPasswordController@showLinkRequestForm')->name('password.request');
    $this->post('password/email', 'Auth\ForgotPasswordController@sendResetLinkEmail')->name('password.email');
    $this->get('password/reset/{token}', 'Auth\ResetPasswordController@showResetForm')->name('password.reset');
    $this->post('password/reset', 'Auth\ResetPasswordController@reset');
}
```

#### 2.数据迁移 --> 在数据库生成对应的表

![1534234217992](/assets/images/laravel-develop-study/1534234217992.png)

`Mysql`语句：

```mysql
CREATE TABLE IF NOT EXISTS students(
	'id' INT AUTO_INCREMENT PRIMARY KEY,
    'name' VARCHAR(255) NOT NULL DEFAULT '' COMMENT '姓名',
    'age' INT UNSIGNED NOT NULL DEFAULT 0 COMMENT '年龄',
    'sex' INT UNSIGNED NOT NULL DEFAULT 10 COMMENT '性别',
    'created_at' INT NOT NULL DEFAULT 0 COMMENT '新增时间',
    'updated_at' INT NOT NULL DEFAULT 0 COMMENT '修改时间'
)ENGINE=InnoDB DEFAULT CHARSET=UTF8
AUTO_INCREMENT=1001 COMMENT='学生表';
```

	完善迁移文件 --> **在`up`函数中添加数据表里的字段**：

```php
<?php

use Illuminate\Support\Facades\Schema;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Database\Migrations\Migration;

class CreateStudentsTable extends Migration
{
    /**
     * Run the migrations.
     *
     * @return void
     */
    public function up()
    {
        Schema::create('students', function (Blueprint $table) {
            $table->increments('id');
            $table->string('name'); // unsigned()表示非负的意思
            $table->integer('age')->unsigned()->default(0);
            $table->integer('sex')->unsigned()->default(10);
            $table->integer('created_at')->default(0);
            $table->integer('updated_at')->default(0);
            $table->timestamps();
        });
    }

    /**
     * Reverse the migrations.
     *
     * @return void
     */
    public function down()
    {
        Schema::dropIfExists('students');
    }
}
```

	将`database/migrations`下的迁移文件做迁移：

```shell
php artisan migrate
```

**迁移步骤：**

1. 新建迁移文件：`php artisan make:model Student -m`或者`php artisan make:migration create_students_table --create=students`。
2. 完善迁移文件，即在`up`函数里添加字段。
3. 做迁移：`php artisan migrate`

#### 3.数据填充 --> 一般填充测试数据

![1534235808674](/assets/images/laravel-develop-study/1534235808674.png)

1. 创建填充文件：`php artisan make:seeder StudentTableSeeder`:

![1534236147269](/assets/images/laravel-develop-study/1534236147269.png)

`DatabaseSeeder.php`：用于批量填充文件。

`StudentTableSeeder.php`：用于单个填充文件。

1. 执行填充文件

   - 单个填充文件：

     ```php
     // \database\seeds\StudentTableSeeder.php
     <?php
     
     use Illuminate\Database\Seeder;
     use Illuminate\Support\Facades\DB;
     
     class StudentTableSeeder extends Seeder
     {
         /**
          * Run the database seeds.
          *
          * @return void
          */
         public function run()
         {   
             // 导入两条数据
             DB::table('students')->insert([
                 ['name' => 'name1', 'age' => 23],
                 ['name' => 'name2', 'age' => 24],
             ]);
         }
     }
     ```

     执行：`php artisan db:seed --class=StudentTableSeeder`

   - 批量填充文件：

     ```php
     // \database\seeds\DatabaseSeeder.php
     <?php
     
     use Illuminate\Database\Seeder;
     
     class DatabaseSeeder extends Seeder
     {
         /**
          * Run the database seeds.
          *
          * @return void
          */
         public function run()
         {	// 将多个填充文件一起执行
             $this->call(StudentTableSeeder::class);
             $this->call(ArticleTableSeeder::class);
             $this->call(CommentTableSeeder::class);
         }
     }
     ```

     执行：`php artisan db:seed`

### 2.Laravel框架常用功能

#### 1.文件上传

![1534237010212](/assets/images/laravel-develop-study/1534237010212.png)

![1534237027967](/assets/images/laravel-develop-study/1534237027967.png)

配置文件：

```php
// config/filesystems.php
<?php
return [
	// 支持"local", "ftp", "s3", "rackspace"，默认使用本地端空间
    'default' => env('FILESYSTEM_DRIVER', 'local'), 

    'cloud' => env('FILESYSTEM_CLOUD', 's3'),
    
	// 磁盘
    'disks' => [
        'local' => [ // 本地端空间磁盘,名字叫local
            'driver' => 'local', // 驱动是本地端空间
            'root' => storage_path('app'), // 目录是storage/app
        ],
        'public' => [ // 本地端空间磁盘,名字叫public，因为驱动是本地端空间，所以它是本地端空间磁盘
            'driver' => 'local',
            'root' => storage_path('app/public'),
            'url' => env('APP_URL').'/storage',
            'visibility' => 'public',
        ],
        's3' => [ // 亚马逊的配置
            'driver' => 's3',
            'key' => env('AWS_KEY'),
            'secret' => env('AWS_SECRET'),
            'region' => env('AWS_REGION'),
            'bucket' => env('AWS_BUCKET'),
        ],
    ],
];
```

使用本地端空间来让laravel有文件上传的功能：

1. 在`config/filesystems.php`创建一个本地端空间磁盘，名字叫：uploads：

   ```php
   // config/filesystems.php
   <?php
   return [
       'default' => env('FILESYSTEM_DRIVER', 'local'), 
   
       'cloud' => env('FILESYSTEM_CLOUD', 's3'),
       
   	// 磁盘
       'disks' => [
           'local' => [ 
               'driver' => 'local', 
               'root' => storage_path('app'), 
           ],
           'public' => [ 
               'driver' => 'local',
               'root' => storage_path('app/public'),
               'url' => env('APP_URL').'/storage',
               'visibility' => 'public',
           ],
           'uploads' => [ // 创建了一个本地端空间磁盘，目录是storage/app/uploads
               'driver' => 'local',
               'root' => storage_path('app/uploads') // 现在这里进行配置，这个文件夹会自己生成
           ],
           's3' => [
               'driver' => 's3',
               'key' => env('AWS_KEY'),
               'secret' => env('AWS_SECRET'),
               'region' => env('AWS_REGION'),
               'bucket' => env('AWS_BUCKET'),
           ],
       ],
   ];
   ```

   位置：

   ![1534237760826](/assets/images/laravel-develop-study/1534237760826.png)

2. 控制器和路由：

   ```php
   // StudentController.php
   <?php
   
   namespace App\Http\Controllers;
   
   use App\Student;
   use Illuminate\Http\Request;
   use Illuminate\Support\Facades\Session;
   use Illuminate\Support\Facades\Storage;
   
   class StudentController extends Controller
   {
      public function upload(Request $request) {
          if ($request->isMethod('POST')) {
              // 获取上传来的文件
              $file = $request->file('source'); 
              
              if ($file->isValid()) {
                  // 判断文件是否上传成功
                  $originaName = $file->getClientOriginalName(); // 原文件名
                  $ext = $file->getClientOriginalExtension(); // 扩展名，后缀
                  $type = $file->getClientMimeType(); // 文件类型
                  $realPath = $file->getRealPath(); // 临时绝对路径，还没手动保存之前文件存放的位置
   
                  // 这种做法保证文件名称都不相同
                  $filename = date('Y-m-d-H-i-s').'-'.uniqid().'.'.$ext;
                  // 保存文件在config/filesystems.php中设置的disk里，返回一个bool，保存得成功不成功
                  $bool = Storage::disk('uploads')->put($filename, file_get_contents($realPath));
              }
          }
   
          return view("student.upload");
      }
   }
   ```

   ```php
   // web.php
   Route::get('/home', 'HomeController@index')->name('home');
   ```

3. 视图里要提交文件的表单：

   ```php
   // resources/views/student/upload.blade.php
   <div class="panel-body">
   	\{{--enctype="multipart/form-data"必须加这个属性，表单才可以使用文件上传功能--\}}
   	<form class="form-horizontal" method="POST" action="" enctype="multipart/form-data">
   		\{{ csrf_field() \}}
       	<div>
                <label for="file" class="col-md-4 control-label">请选择文件</label>
                <div class="col-md-6">		\{{--name值是source--\}}
                   <input id="file" type="file" class="form-control" name="source" required>
                </div>
            </div>
            <div class="form-group">
                <div class="col-md-8 col-md-offset-4">
                   <button type="submit" class="btn btn-primary">
                       确认上传
                   </button>
                </div>
             </div>
        </form>
   </div>
   ```

4. 可以通过更改`config/filesystems.php`里的`uploads`磁盘的空间为`public`目录底下的`uploads`目录。

![1534342816613](/assets/images/laravel-develop-study/1534342816613.png)

#### 2.发送邮件

![1534343099473](/assets/images/laravel-develop-study/1534343099473.png)

![1534343121043](/assets/images/laravel-develop-study/1534343121043.png)

	配置文件：

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

1. 在`.env`中进行配置：

```properties
MAIL_DRIVER=smtp # 使用的服务
MAIL_HOST=smtp.mailtrap.io # 服务器地址
MAIL_PORT=2525 # 服务器端口
MAIL_USERNAME=jim # 账号
MAIL_PASSWORD=passowrd
MAIL_ENCRYPTION=ssl # 协议
```

1. 控制器以及路由

```php
Route::any('mail', ['uses' => 'StudentController@mail']);
```

控制器：

- 以`raw`方式发送邮件：

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

- 以`html`方式发送邮件：

创建一个`html`文件，即视图：

```php
<!--resources/views/student/mail.blade.php-->
<!DOCTYPE html>
<html>
<head>
    <title>标题</title>
</head>
<body> <!--$name由控制器注入进来-->
<h1>Hello \{{ $name \}}</h1>
</body>
</html>
```

	控制器：

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

#### 3.缓存使用

![1534344890615](/assets/images/laravel-develop-study/1534344890615.png)

![1534344915362](/assets/images/laravel-develop-study/1534344915362.png)

![1534344930819](/assets/images/laravel-develop-study/1534344930819.png)

配置文件：

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

控制器：

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

	`add()`:添加。

```php
public function cache1() {
    // add(),如果对象已经存在,就添加失败，如果对象不存在，添加成功
    // 返回一个bool值,10是时间
    $bool = Cache::add('key1', 'val1', '10');
}
```

	`forever()`：永久的保存对象到缓存中。	

```php
public function cache1() {
    Cache::forever('key1', 'val1');
}
```

	`has()`:判断缓存中的一个`key`值存不存在。

```php
public function cache1() {
    if (Cache::has('key')) {
        $val = Cache::get('key')
    } else {
        echo "No"
    }
}
```

	`pull`:取缓存中的`key`值，然后删了这个`key`。

```php
public function cache1() {
    $val = Cache::pull('key');
}
```

	`forget()`:从缓存中删除对象，删除成功返回`true`，返回一个`bool`值。

```php
public function cache1() {
    $bool = Cache::forget('key');
}
```

#### 4.错误和日志

![1535095566213](/assets/images/laravel-develop-study/1535095566213.png)

![1535095599480](/assets/images/laravel-develop-study/1535095599480.png)

1. `debug`模式：开发模式，调试模式。

可在`.env`里开启和调试：

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

	默认是开启调试模式的，如果发生错误，`laravel`会在网页打印出错误栈。
	
	**上线了一定要关闭调试模式！！**

1. `http`异常

![1535096147008](/assets/images/laravel-develop-study/1535096147008.png)

自定义`http`异常：

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

`http`异常的视图位置：

`vendor\laravel\framework\src\Illuminate\Foundation\Exceptions\views`:

![1535098035926](/assets/images/laravel-develop-study/1535098035926.png)

1. 日志

![1535098224286](/assets/images/laravel-develop-study/1535098224286.png)

`config/app.php`：

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

	配置日志模式：

```php
# 在.env中进行配置
# APP_LoG原本的.env里是没有的，是自己添加的，只能配置"single", "daily", "syslog", "errorlog"这几种模式
APP_LoG=single 
APP_LOG_LEVEL=debug
```

	这样是会在![1535098804878](/assets/images/laravel-develop-study/1535098804878.png)这里生成日志文件:`laravel.log`。
	
	使用日志：

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

	`daily`的`log`模式，会每天生成一个日志：

![1535099439063](/assets/images/laravel-develop-study/1535099439063.png)



















[看到这里](https://www.imooc.com/video/13341)

























---
layout: post
title: Laravel学习笔记
---
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
\{{ $name \}} \{{ $age \}}
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

## 2.数据库操作

**Laravel提供了DB facade（原始查找）、查询构造器和Eloquent ORM三种操作数据库的方式。**

### 1.连接数据库(config/database.php + .env)

打开config/database.php,找到：

```php
// 表示默认要连接的数据库是mysql
'default' => env('DB_CONNECTION', 'mysql'),
```

再往下找到：

```php
// 下面的env(..., ...)其实就是根目录的.env文件里的信息
'mysql' => [
    'driver' => 'mysql',
    'host' => env('DB_HOST', '127.0.0.1'),
    'port' => env('DB_PORT', '3306'),
    'database' => env('DB_DATABASE', 'forge'),
    'username' => env('DB_USERNAME', 'forge'),
    'password' => env('DB_PASSWORD', ''),
    'unix_socket' => env('DB_SOCKET', ''),
    'charset' => 'utf8mb4',
    'collation' => 'utf8mb4_unicode_ci',
    'prefix' => '', // 表前缀
    'strict' => true,
    'engine' => null,
],
```

打开.env,找到:

```php
DB_CONNECTION=mysql
DB_HOST=127.0.0.1
DB_PORT=3306
DB_DATABASE=laravel5
DB_USERNAME=root
DB_PASSWORD=
```

数据库连接完成。

### 2.使用DB facade实现CURD

CURD：增删改查

```php
// App/Http/Controllers/ArticleController.php，控制器里操作数据库
<?php

namespace App\Http\Controllers;
use App\Article;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\DB;

class ArticleController extends Controller
{
    public function operate(){
        // 插入
        $bool = DB::insert('insert into student(name, age) value(?, ?)', ['Jim', 18]);
        var_dump($bool); // 返回插入成不成功的值，true或false
        
        // 更新
        $num = DB::update('update student set age = ? where name = ?', [20, 'Jim']);
        var_dump($num); // 返回修改的行数
        
        // 查询
        $students = DB::select('select * from student where id > ?', [1001]);
        dd($students); // 返回查询结果，是个数组
        
        // 删除
        $num = DB::delete('delete from student where id > ?', [1001]);
        var_dump($num); // 返回被删除的行数

    }
}
```

var_dump(), dd()，都是调试代码，都能将()里的东西打印出来。

### 3.查询构造器

#### 1.新增数据

```php
// App/Http/Controllers/HomeController.php
public function query(){
        // 插入成功返回一个布尔值
        $bool = DB::table('student')->insert(
            ['name' => 'Jim', 'age' =>  18]
        );
        // 插入成功返回插入的id
        $id = DB::table('student')->insertGetId(
            ['name' => 'Jim', 'age' => 18]
        );
        // 插入多条数据
        $id = DB::table('student')->insert(
            ['name' => 'name1', 'age' => 18],
            ['name' => 'name2', 'age' => 18],
            ['name' => 'name3', 'age' => 18],
            ['name' => 'name4', 'age' => 18]
        );
    }
```

#### 2.更新数据

```php
// App/Http/Controllers/HomeController.php   
public function query(){
        // 将student表中id=2的元组中的age更新为30，返回的是受影响的行数
        $num = DB::table('student')
            ->where('id', 12) // 更新数据一定要带条件
            ->update(['age' => 30]);
        // 自增和自减
        $num = DB::table('student')->increment('age'); // 默认自增1
        $num = DB::table('student')->increment('age', 3); // 自增3
        $num = DB::table('student')->decrement('age'); // 默认自减1
        $num = DB::table('student')->decrement('age', 3); // 自减3
        // 将student表中id=12的元组的age自增3，同时name改为Jim
        $num = DB::table('student')
            ->where('id', 12)
            ->decrement('age', 3, ['name' => 'Jim']);
    }
```

#### 3.删除数据 

```php
// App/Http/Controllers/HomeController.php    
public function query(){
        // 删除student表中id=12的元组，返回受影响的行数
        $num = DB::table('student')
            ->where('id', 12)
            ->delete();
        // 删除student表中id>=12的元组，返回受影响的行数
        $num = DB::table('student')
            ->where('id', '>=', 12)
            ->delete();
        // 删除表，不返回任何东西
        DB::table('student')->truncate();
    }
```

#### 4.查询数据

get(), first(), where(), pluck(), lists(), select(), chunk().

```php
// App/Http/Controllers/HomeController.php  
public function query(){
        // get(),返回的是所有的表数据，一个列表
        $student = DB::table('student')->get();
        // first(),返回的是第一条记录
        $student = DB::table('student')->first();
        $student = DB::table('student') // 以student表的id进行倒序排序，获取第一条数据
            ->orderBy('id','desc')
            ->first();
        // where()
        $student = DB::table('student')
            ->where('id', '>=', 122)
            ->get();
        $student = DB::table('student') // 加多个条件查询
            ->whereRaw('id >= ? and age > ?', [122, 34])
            ->get();
        // pluck(),返回字段,是个列表
        $student = DB::table('student') // 返回student表的name字段
        ->pluck('name');
        // lists(),返回字段
        $student = DB::table('student') // 返回student表的name字段
        ->lists('name');
        $student = DB::table('student') // 返回student表的name字段
        ->lists('name', 'id');          // 但是这个列表中的索引用的是id
        // select()，返回的是指定的字段
        $name = DB::table('student')
            ->select('id', 'name', 'age')
            ->get();
        // chunk()，有时候数据太多，一次性获取会太慢，所以就要分段进行获取
        $name = DB::table('student')->chunk(50, function ($student){ // 每次获取50条元组，这50条元组赋值给闭包中的$student
            if( <条件> ){       // 当满足条件的时候，就会返回false，一旦返回false，程序就停止查询，所以可以通过设定条件让程序只查询几次就可以了
                return false;
            }
        });
    }
```

#### 5.聚合函数

count(), avg(), max(), sum(), min().

```php
// App/Http/Controllers/HomeController.php 
public function query(){
        // 返回元组的个数
        $sum = DB::table('student')->count();
        // 返回student表中age字段的最大值
        $sum = DB::table('student')->max('age');
        // 返回student表中age字段的最小值
        $sum = DB::table('student')->min('age');
        // 返回student表中age字段的值的平均值
        $sum = DB::table('student')->avg('age');
        // 返回student表中age字段的值的总和
        $sum = DB::table('student')->sum('age');
    }
```

### 4.Eloauent ORM

在laravel中用model跟数据库中的表进行交互，laravel自带的Eloquent ORM用来实现数据库操作。

#### 1.创建model

在App下面创建一个Student的model类：

```php
<?php

namespace App;

use Illuminate\Database\Eloquent\Model;

class Student extends Model
{
    // 指定表名，没有指定的话，默认为该模型的复数即students
    protected $table = 'student';

    // 指定主键，默认是表中的id字段
    protected $primaryKey = 'id';

}
```

这样，一个model就创建好了。

#### 2.使用model

在model对应的controller中使用model。

```php
<?php

namespace App\Http\Controllers;

class StudentController
{
    public function orm() {
        // all(),查询表的所有记录，返回一个集合collection
        $students = Student::all();
        // 返回id为12的元组
        $student = Student::find(12);
        // findOrFail(),根据指定查找，如果没有找到，返回异常
        $student = Student::findOrFail(12); // id为12的元组找不到就报错
    }
}
```

在ORM中使用查询构造器：

```php
<?php

namespace App\Http\Controllers;

class StudentController
{
    public function orm() {
        // 查询所有，返回一个集合collection
        $student = Student::get();
        
        $student = Student::where('id', '>', '34')
            ->orderBy('age', 'desc')
            ->first();
        
        Student::chunk(2, function($stuent){
            var_dump($student);
        });
        
        $num = Student::count();
        
        $max = Student::where('id', '>', 1002)->max('age');
              
    }
}
```

#### 3. 自定义时间戳及批量赋值

```php
// Student model
// App/Student.php
<?php

namespace App;


use Illuminate\Database\Eloquent\Model;

class Student extends Model
{
    // 指定表名，没有指定的话，默认为该模型的复数即students
    protected $table = 'student';

    // 指定主键，默认是表中的id字段
    protected $primaryKey = 'id';

    // 一般情况下模型对象向数据库增加数据时还会附加一个时间戳，
    // 如果不想要，在这里将$timestamps设置为false即可
    protected $timestamps = true;
    // 该函数与上面的$timestamps=true结合在一起给增添的字段附加一个时间戳
    protected function getDateFormat()
    {
        return time(); // 返回给我们的时间将会是格式化好的
    }
    // 如果我们不想格式化，让模型给我们返回一个时间戳（我们自己之后利用
    // 这个时间戳做自己想做的事。用下面这个函数：
    protected function asDateTime($value)
    {
        return $value;
    }
}
```

```php
// 在StudentConller这个控制器中操纵Student这个model
// App/Http/Controllers/StudentConller.php
<?php

namespace App\Http\Controllers;


class StudentController
{
    public function orm() {

        $student = new Student();
        $student->name = 'Jim';
        $student->age = 12;
        $bool = $student->save(); // 保存数据到数据库直接这样就行，返回一个bool
        // $student->created_at会返回一个时间戳，这个已经在Student这个model设置好了
        // 然后我们用这个时间戳自己再来格式化并打印
        echo data('Y-m-d H:i:s', $student->created_at);
    }
}
```

批量赋值数据：

```php
// App/Http/Controllers/StudentConller.php
<?php

namespace App\Http\Controllers;


class StudentController
{
    public function orm() {
		// 使用create()新增数据
        $student = Student::create(
        	['name' => 'Jim', 'age' => 23]
        );
    }
}
```

```php
// App/Student.php
<?php

namespace App;

use Illuminate\Database\Eloquent\Model;

class Student extends Model
{    // 指定允许批量赋值的model的字段，然后controller里就可以
    // 用model的create()批量赋值数据
    protected $fillable = ['name', 'age'];

    // 指定不允许批量赋值的model的字段
    protected $guarded = [];
}
```

其他新增数据的方法：

```php
// 以字段查找某个元组，如果没有那就创建
$student = Student::firstOrCreate(
    ['name' => 'Jim']
);

// 以字段查找某个元组，如果没有那就创建
$student = Student::firstOrNew(
    ['name' => 'Jim']
);
// firstOrNew是不会将数据保存数据库的，如果需要保存，
// 则自己编写以下的保存代码,返回是个bool，即保存成不成功
$bool = $student->save();
```

#### 4.修改数据

```php
// App/Http/Controllers/StudentConller.php
<?php

namespace App\Http\Controllers;

use App\Student;

class StudentController
{
    public function orm() {
        // 1.通过模型更新数据，返回的$bool代表保存得成不成功
        $student = Student::find(2021);
        $student->name = 'Jim';
        $bool = $student->save();
        // 2.利用查询语句来更新数据
        $num = Student::where('id', '>', 120)
            ->update(
                ['age' => 23]
            );
    }
}
```

#### 5.删除数据

```php
public function orm() {
    // 1.通过模型删除,返回一个代表删除成不成功的$bool
    $student = Student::find(201);
    $bool = $student->delete(); // 删除不到这个元组就会报错

    // 2.通过主键删除,返回删除的行数，即一个删除了几行
    $num = Student::destroy(1021);
    // 删除多个id的元组：
    $num = Student::destroy(1021, 33);
    // 或者：
    $num = Student::destroy([2021, 33]);

    // 3.通过查询语句删除,返回删除的行数
    $num = Student::where('id', '>', 23)->delete();
}
```

## 3.Blade模板

### 1.模板继承

![20180805224923.png](/assets/images/laravel-develop-study/20180805224923.png)

父模板(views.layouts)：

```php
// resources/views/layouts.blade.php
\{{--@section,展示片段内容--\}}
@section('header')
    头部
@show

@section('sidebar')
    侧边栏
@show

\{{--@yield，展示字符串内容--\}}
@yield('content', '主要内容')
```

子模板(views.student.child):

```php
// resources/views/student/child.blade.php
\{{--1.继承哪个模板--\}}
@extends('layouts')

\{{--2.替换父模板中@section的header内容，输出父模板对应地方的父内容--\}}
@section('header')
    @parent
    header
@stop
\{{--或者--\}}
\{{--重写父模板中@section的sidebar内容，不会输出父模板对应地方的父内容--\}}
@section('sidebar')
    sidebar
@stop

\{{--3.替换父模板中@yield的content内容--\}}
@section('content')
    content
@stop
```

controller中访问的是子模板：

```php
// App/Http/Controllers/StudentController.php
<?php

namespace App\Http\Controllers;


use App\Student;

class StudentController
{
    public function view() {
        return view('student.child'); // 访问views目录底下的student/child.blade.php
    }
}
```

### 2.基础语法：

```php
\{{--resources/views/student/child.blade.php--\}}
\{{--1.模板中输出PHP变量，该变量由控制器传入--\}}
\{{ $name \}}

\{{--2.模板中调用PHP代码,$name和$arr两个变量都由控制器中传进来--\}}
\{{ time() \}}
\{{ date('Y-m-d H:i:s', time()) \}}
\{{--判断$arr数组中是否有$name,有返回true，没有返回false--\}}
\{{ in_array($name, $arr) ? 'ture': 'false' \}}
\{{--判断$name是否存在,有返回$name值，没有返回字符串'default'--\}}
\{{ isset($name) ? $name: 'default' \}}
\{{--或者--\}}
\{{ $name or 'default' \}}

\{{--3.原样输出，视图渲染时输出\{{ $name \}}--\}}
@\{{ $name \}}

\{{--4.模板注释--\}}
\{{--xxxx--\}}

\{{--5.子模板中引入子视图--\}}
@include('student.common')
\{{--子视图中有占位符$msg,在这里将msg赋值并传给子视图--\}}
@include('student.common', ['msg' => 'error'])
```

控制器传入值：

```php
class StudentController
{
    public function view() {
        $name = 'Jim';
        $arr = ['a', 'b'];
        return view('student.child', [
            'name' => $name, // 传入值
            'arr' =>$arr, // 传入数组
        ]);
    }
}
```

子视图：

```php
\{{--resources/views/student/common.blade.php--\}}
\{{--$msg是个占位符，等着别处传过来值给它赋值--\}}
\{{ $msg \}}
```

### 3.模板中流程控制

```php
\{{--resources/vies/student/child.blade.php--\}}

\{{--if--\}}
@if ($name == 'Jim')
    Jim
@elseif($name == 'a')
    a
@else
    b
@endif

\{{--unless,相当于if的取反--\}}
@unless( $name == 'Jim' )
    output Jim
@endunless

\{{--for--\}}
@for ($i=0; $i<2; $i++)
    <p>\{{ $i \}}</p>
@endfor

\{{--foreach,遍历对象列表或者数组--\}}
@foreach($students as $student) \{{--该$student对象列表由控制器传入--\}}
    <p>\{{ $student->name \}}</p> \{{--返回$student对象的name属性--\}}
@endforeach

\{{--forelse--\}}
@forelse($students as $student)
    <p>\{{ $student->name \}}</p>
@empty\{{--如果对象列表为空--\}}
    <p>null</p>
@endforelse
```

控制器中将对象数组传给视图：

```php
<?php

namespace App\Http\Controllers;

use App\Student;

class StudentController
{
    public function view() {
        $students = Student::get(); // 从model中获取所有的元组对象，组成一个对象列表
        $name = 'Jim';
        return view('student.child', [
            'name' => $name,
            'students' => $students,
        ]);
    }
}
```

### 4.模板中url

路由：

```php
// 路由名字：urlTest， 路由别名：urlAlias， 控制器及方法：StudentController@urlTest 
Route::any('urlTest', ['as' => 'urlAlias', 'uses' => 'StudentController@urlTest']);
```

模板中生成url：

```php
\{{--resources/views/student/child.blade.php--\}}
\{{--1.指定的路由名字--\}}
<a href="\{{ url('urlTest') \}}">This is url.</a>
\{{--2.控制器+方法名--\}}
<a href="\{{ action('StudentController@urlTest') \}}">This is url.</a>
\{{--3.路由的别名--\}}
<a href="\{{ route('urlAlias') \}}">This is url.</a>
```

# 二、laravel表单

## 1.request

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

## 2.session

session的配置文件在config/session.php中。

使用session的三种方法：

* HTTP request类的session()方法
* session()辅助函数
* Session facade

config/session.php部分解析：

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

**先在路由表中添加要使用session()的路由的web中间件：**

```php
// routes/web.php
Route::group(['middleware' => ['web']], function (){ // 用路由组的方式同时给session1和session2两个路由添加webs中间价
    Route::any('session1', ['uses' => 'StudentController@session1']);
    Route::any('session2', ['uses' => 'StudentController@session2']);
});
```

1.HTTP request的session()

先访问session1方法，会往session放入一个key，然后访问session2方法，会从session中取出key值。

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

2.直接session()

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

3.Session facade

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

其他用法：

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

## 3.response

响应的类型：字符串， 视图， Json， 重定向。

1. Json

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

2. 重定向

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

	或者：
	
	action(), 控制器+方法

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

	或者：
	
	route(), 路由别名

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

	或者：
	
	back(),返回上一个页面

```php
class StudentController
{
    public function response() {
        redirect()->back();
    }
}
```

## 4.Middleware

Laravel中间件提供了一个方便的机制来过滤进入应用程序的HTTP请求。

假设一个场景：有一个活动，指定日期开始前只能访问宣传页面，活动开始日期后才可以访问活动页面。

1. 新建控制器方法

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

2. 新建中间件

![2018-08-06_213029](/assets/images/laravel-develop-study/2018-08-06_213029.png)

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

	在Kernel.php中注册中间件:

![2018-08-06_213247](/assets/images/laravel-develop-study/2018-08-06_213247.png)

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

	如果想注册全局中间件，则在Kernel.php里的这里注册：

```php
protected $middleware = [
    \Illuminate\Foundation\Http\Middleware\CheckForMaintenanceMode::class,
    \Illuminate\Foundation\Http\Middleware\ValidatePostSize::class,
    \App\Http\Middleware\TrimStrings::class,
    \Illuminate\Foundation\Http\Middleware\ConvertEmptyStringsToNull::class,
    \App\Http\Middleware\TrustProxies::class,
];
```

3. 使用中间件(在路由文件中)

```php
// 访问活动页面就会跳入这个中间件
Route::group(['middleware' => ['activity']], function () {
    Route::any('activity_running', ['uses' => 'StudentController@activity_running']);
});
// 然后中间件根据判断就会重定向到这个路由
Route::any('activity_advertise', ['uses' => 'StudentController@activity_advertise']);
```

4. 其他

中间件有前置操作和后置操作。

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

## 5.表单案例笔记

1.静态资源路径：`\{{ asset() \}}`

```php
    <link href="\{{ asset('static/css/bootstrap.min.css') \}}" rel="stylesheet">
```

这个路径是相对于public文件夹下的，也就是文件位置：![2018-08-07_134524](/assets/images/laravel-develop-study/2018-08-07_134524.png)

2. 表单分页

   控制器下用`Student::paginate(num)`取得所有的数据，然后将数据再传给视图。

```php
<?php

namespace App\Http\Controllers;


use App\Student;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Session;

class StudentController extends Controller
{
    public function index() {
        $students = Student::paginate(3); // '3'表示每页显示3条记录

        return view('student.index', [
            'students' => $students,
        ]);
    }
}
```

	在需要用到分页的视图里，直接` \{{ $students->render() \}}`就行了，这条语句会自动生成含有`ul`和`li`的分页信息的。

```php
<!--student.index视图的分页内容-->
	<!--分页-->
    <div class="pull-right">
        \{{ $students->render() \}}
    </div>
```

3. 默认选中项

```php
<ul class="nav nav-pills nav-stacked">
<li role="presentation" class="\{{ Request::getPathInfo() == '/student/index' ? 'active' : '' \}}"><a href="\{{ url('student/index') \}}">学生列表</a></li>
<li role="presentation" class="\{{ Request::getPathInfo() == '/student/create' ? 'active' : '' \}}"><a href="\{{ url('student/create') \}}">新增学生</a></li>
</ul>
```

用`Request::getPathInfo()`判断当前路径是否`/student/index`或者`/student/create`，是的话那就`active`,表示选中，不然就为空` `，不选中。注意`/student/index`和`/student/create`最前面的`/`是要有的。

4. 表单提交

* 提交到`save()`:

```php
<form action="\{{ url('student/save') \}}" method="POST"> 
    <!-- 1.设置action路径为'student/save',即提交到student/save -->

    <label for="inputName" >姓名：</label>
        <input type="text" name="Student[name]" id="inputName" placeholder="请输入姓名"> 
        <!-- 2.将各input的name属性都设为统一的数组，即统一都为Student的数组，只是下标不一样 -->

    <label for="inputAge">年龄：</label>
        <input type="text" name="Student[age]" id="inputAge" placeholder="请输入年龄">

    <div>
        <label>性别：</label>
        <div>
            <label>
                <input type="radio" name="Student[sex]" value="man">男
            </label> <!-- 3.注意radio的话可以这么设置，设两次Studnet[sex] -->
            <label>
                <input type="radio" name="Student[sex]" value="woman">女
            </label>
        </div>
    </div>
    <button type="submit">提交</button>
</form>
```

	添加一条路由：

```php
Route::any('student/save', ['uses' => 'StudentController@save']);
```

	在控制器中添加save():

```php
public function save(Request $request){
    $data = $request->input('Student');

    $student = new Student();
    $student->name = $data['name'];
    $student->age = $data['age'];
    $student->sex = $data['sex'];

    if($student->save()) {
        return redirect('student/index');
    } else {
        return redirect()->back();
    }
```

* 提交到当前页面

```php
<form action="" method="POST"> 
    <!-- 1.action没设置，默认提交到当前页面 -->

    <label for="inputName" >姓名：</label>
        <input type="text" name="Student[name]" id="inputName" placeholder="请输入姓名"> 
        <!-- 2.将各input的name属性都设为统一的数组，即统一都为Student的数组，只是下标不一样 -->

    <label for="inputAge">年龄：</label>
        <input type="text" name="Student[age]" id="inputAge" placeholder="请输入年龄">

    <div>
        <label>性别：</label>
        <div>
            <label>
                <input type="radio" name="Student[sex]" value="man">男
            </label> <!-- 3.注意radio的话可以这么设置，设两次Studnet[sex] -->
            <label>
                <input type="radio" name="Student[sex]" value="woman">女
            </label>
        </div>
    </div>
    <button type="submit">提交</button>
</form>
```

	不用添加一条路由，只是注意当前页面路由要能有POST方法：

```php
Route::any('student/create', ['uses' => 'StudentController@create']);
```

	在控制器中修改create():

```php
public function create(Request $request){
    if ($request->isMethod('POST')) { // 添加这个判断
        $data = $request->input('Student');
        if (Student::create($data)) { // 调用create()会采用批量赋值，所以要确保model中要有protected $fillable
            return redirect('student/index');
        } else {
            return redirect()->back();
        }
    }

    return view('student.create'); // 不是POST方法的话，就直接跳转到create视图中去
}
```

5. 操作提示

创建一个提示信息子视图：

```php
<!--message.blade.php-->
@if (Session::has('success'))
<!--成功提示框-->
<div class="alert alert-success alert-dismissable" role="alert">
    <button type="button" class="close" data-dismiss="alert" aria-label="Close">
        <span aria-hidden="true">&times;</span>
    </button>
    <strong>成功!!</strong>\{{ Session::get('success') \}}！
</div>
@endif
@if (Session::has('error'))
<!--失败提示框-->
<div class="alert alert-danger alert-dismissable" role="alert">
    <button type="button" class="close" data-dismiss="alert" aria-label="Close">
        <span aria-hidden="true">&times;</span>
    </button>
    <strong>失败!!</strong>\{{ Session::get('error') \}}！
</div>
@endif
```

位置：![2018-08-07_200359](/assets/images/laravel-develop-study/2018-08-07_200359.png)

哪个视图需要这个信息提示框就直接`@include('common.message')`过去。

控制器中使用：

```php
public function create(Request $request){
    if ($request->isMethod('POST')) {
        $data = $request->input('Student');
        if (Student::create($data)) {
            return redirect('student/index')->with('success', '添加成功');
            // 在控制器中调用暂存数据的方法，只能访问一次
        } else {
            return redirect()->back();
        }
    }
```

**这样，当数据保存成功然后返回的index页面时，就会向`session`中注入`success`的属性信息，当`common.message`页面中判断`session`属性存在时，就会显示信息在有`@include('common.message')`的视图里。**

记住，一定要将需要`session`的路由加进到`web`中间件中：

```php
Route::group(['middleware' => ['web']], function () {
    Route::get('student/index', ['uses' => 'StudentController@index']);
    Route::any('student/create', ['uses' => 'StudentController@create']);
    Route::post('student/save', ['uses' => 'StudentController@save']);
});
```

中间件`web`还能防止xxs攻击，所以，如果路由里有表单提交的话，一定要在表单视图中加入`\{{ csrf_field() \}}`。

```php
<!--create.blade.php-->
@section('content')
<form action="\{{ url('student/save') \}}" method="POST">

    \{{ csrf_field() \}} <!--防止xxs攻击-->

    <label for="inputName" >姓名：</label>
        <input type="text" name="Student[name]" id="inputName" placeholder="请输入姓名"> 

    <label for="inputAge">年龄：</label>
        <input type="text" name="Student[age]" id="inputAge" placeholder="请输入年龄">

    <button type="submit">提交</button>
</form>
@stop
```

6. 表单数据验证

* 控制器验证

```php
public function create(Request $request){
    if ($request->isMethod('POST')) {

        $this->validate($request, [
            'Student.name' => 'required|min:2|max:5',// 数组形式要写成这样子Student.name <= Student[name]
            'Student.age' => 'required|integer|max:2',
            'Student.sex' => 'required|integer'
        ], [
            'required' => ':attribute 为必选项',
            'min' => ':attribute 长度不符合要求',
            'integer' => ':attribute 必须为整数',
            'max' => ':attribute 长度不符合要求',
        ], [
            'Student.name' => '姓名',
            'Student.age' => '年龄',
            'Student.sex' => '性别',
        ]);


        $data = $request->input('Student');
        if (Student::create($data)) { // 调用create()会采用批量赋值，所以要确保model中要有protected $fillable
            return redirect('student/index')->with('success', '添加成功');
        } else {
            return redirect()->back();
        }
    }
```

验证通过是，程序将会继续往下执行，不通过时，表单将会重定向到上个页面并将错误抛给`session`，该错误属性是`$errors`，这个`$errors`是个数组，可以在全局的视图中捕获的。

然后，自定义错误内容：

```php
$this->validate($request, [
    'Student.name' => 'required|min:2|max:5',// 数组形式要写成这样子Student.name <= Student[name]
    'Student.age' => 'required|integer|max:2',
    'Student.sex' => 'required|integer'
], [
    'required' => ':attribute 为必选项', // :attribute是个占位符，表示对应的Student.name、Student.age、Student.sex
    'min' => ':attribute 长度不符合要求',
    'integer' => ':attribute 必须为整数',
    'max' => ':attribute 长度不符合要求',
], [
    'Student.name' => '姓名',
    'Student.age' => '年龄',
    'Student.sex' => '性别',
]);
```

	譬如：当因为`Student.name`的`required`不通过验证时，就会抛出`姓名 为必选项`。

![2018-08-07_210700](/assets/images/laravel-develop-study/2018-08-07_210700.png)

	如果不这样自定义的话，那抛出来的错误内容信息就是`Student.name is required.`，这个不太友好。

将用于捕获验证错误信息的程序放入一个视图：

```php
// common.validator.blade.php
@if (count($errors))
    <div class="alert alert-danger">
        <ul>
            @foreach($errors->all() as $error) // 将所有的错误都输出
            <li>\{{ $error \}}</li>
            @endforeach
        </ul>
    </div>
@endif
```

哪个视图需要输出验证错误信息的再来`@include('common.validator')`:

```php
@section('content')

    @include('common.validator') <!--需要输出验证信息的地方-->

    <form action="\{{ url('student/save') \}}" method="POST">
        \{{ csrf_field() \}}
        <label for="inputName" >姓名：</label>
            <input type="text" name="Student[name]" id="inputName" placeholder="请输入姓名"> 

        <label for="inputAge">年龄：</label>
            <input type="text" name="Student[age]" id="inputAge" placeholder="请输入年龄">

        <button type="submit">提交</button>
    </form>
@stop
```

* Validator类验证

```php
public function create(Request $request){
    if ($request->isMethod('POST')) {
        
        $validator = \Validator::make($request->input(), [
            'Student.name' => 'required|min:2|max:5',
            'Student.age' => 'required|integer|max:2',
            'Student.sex' => 'required|integer'
        ], [
            'required' => ':attribute 为必选项',
            'min' => ':attribute 长度不符合要求',
            'integer' => ':attribute 必须为整数',
            'max' => ':attribute 长度不符合要求',
        ], [
            'Student.name' => '姓名',
            'Student.age' => '年龄',
            'Student.sex' => '性别',
        ]);
        if ($validator->fails()) { // 这种方法验证也就是手动验证,在函数体里面还能做其他的事
            return redirect()->back()->withErrors($validator);
        } // 注意要用withErrors($validator)注册错误信息

        $data = $request->input('Student');
        if (Student::create($data)) { // 调用create()会采用批量赋值，所以要确保model中要有protected $fillable
            return redirect('student/index')->with('success', '添加成功');
        } else {
            return redirect()->back();
        }
    }

    return view('student.create');
}
```

在视图中调用指定的错误信息：`\{{ $errors->first('Student.name') \}}`,如果有自定义错误内容`姓名 为必选项`，则输出的是错误对应（`Student.name`）的自定义内容。

7. 数据保持

只需要在上述表单验证代码中加入`->withInput()`:

![2018-08-07_222555](/assets/images/laravel-develop-study/2018-08-07_222555.png)

`withInput()`自动默认将`$request`作为参数传进去，然后再在需要的`input`组件添加`value="\{{ old('Student')['name'] \}}"`即可：

```php
<input type="text" value="\{{ old('Student')['name'] \}}" name="Student[name]" class="form-control" id="inputName" placeholder="请输入姓名">
```

这样子，在提交表单而发生错误后，重定向到原先的表单填写页面时，它会自动补全在`input`之前填过的信息：![2018-08-07_223016](/assets/images/laravel-develop-study/2018-08-07_223016.png)

**注：**

`min:2|max:5`：
当要验证的值为数字时，那么这个数字要大于等于`2`小于等于`5`（`4`满足要求）；
当要验证的值为字符串，那么这个字符串不管是中英混合，还是全英，还是全文，它的长度要大于等于`2`小于等于`5`（`hh哈哈`长度为4，满足要求）。

8. 自定义数据库取出来的值

譬如，当存储性别时（有’未知‘，’男‘， ’女‘）,数据库真正所对应存储的是10， 20， 30。所以这时候就要自定义数据库取出来的值。

首先，在对应的model中写入一个函数：

```php
// App\Student.php
<?php

namespace App;

use Illuminate\Database\Eloquent\Model;

class Student extends Model
{
    protected $fillable = ['name', 'age', 'sex'];

    protected $table = 'student';

    public $timestamps = true;

    protected function getDateFormat()
    {
        return time();
    }
    protected function asDateTime($value)
    {
        return $value;
    }

    // 以下函数能将数字转化为对应的汉字，数字用来存储，汉字用来显示
    const SEX_UN = 10; // 定义三个常量
    const SEX_BOY = 20;
    const SEX_GIRL = 30;

    public function sex($ind = null) {
        $arr = [
            self::SEX_UN => '未知',
            self::SEX_BOY => '男',
            self::SEX_GIRL => '女',
        ];
        if ($ind !== null) { // 注意不等于是 !==
            return array_key_exists($ind, $arr) ? $arr[$ind] : $arr[self::SEX_UN];
        }
        return $arr;
    }

}
```

`Studen`这个model里有个`sex`函数，`sex()`时能将所有的性别取出来，传入相应的`index`时能取出对应的汉字性别。

接着，在控制器中将model注入到视图中去。

```php
public function create(){
    $student = new Student(); //先将model实例化
    return view('student.create', [
        'student' => $student // 然后再注入到视图里
    ]);
}
```

然后，在视图中就可以调用model的性别转化函数`sex()`。

```php
@foreach($students as $student)
    <tr>
        <td>\{{ $student->id \}}</td>
        <td>\{{ $student->name \}}</td>
        <td>\{{ $student->age \}}</td>
        <td>\{{ $student->sex($student->sex) \}}</td>
    </tr> <!--储存到model中的性别是个数字，$student->sex是个数字，$student->sex()才将这个数字转化对应性别为中文汉字-->
@endforeach
```

```php
@foreach($student->sex() as $ind=>$val)
    <label class="radio-inline"> <!--sex()返回一个数组，$ind是10,20,30,$val是未知，男，女-->
        <input type="radio" name="Student[sex]" value="\{{ $ind \}}">&nbsp;\{{ $val \}}
    </label> <!--最后提交到数据库是，如果是未知，那Student[sex]=10，男：Student[sex]=10等-->
@endforeach
```

	上面这样写就有这个效果：![2018-08-08_104915](/assets/images/laravel-develop-study/2018-08-08_104915.png)，就不必在页面上写很多个`input`标签了。

9. 遇到的坑：`App\Student::sex must return a relationship instance`

情况：

	在控制器中,当访问`student.create`时，会以这样注入一个model实例的方式：

```php
public function create(){
    $student = new Student();
    return view('student.create', [
        'student' => $student,
    ]);
}
```

	使得`create`视图里的`input`组件不用写多个，也能变成：![2018-08-08_104915](/assets/images/laravel-develop-study/2018-08-08_104915.png)

```php
@foreach($student->sex() as $ind=>$val)
    <label class="radio-inline">
    	<input type="radio" name="Student[sex]" value="\{{ $ind \}}">&nbsp;\{{ $val \}}
	</label>
@endforeach
```

	但是，`create`视图的这个部分其实也是`@include('student._form')`的，上面 的`input`标签也是放在这个通用的`_form`视图里的。所以实际上`_form.blade.php`：

```php
@foreach($student->sex() as $ind=>$val)
    <label class="radio-inline">
    	<input type="radio" name="Student[sex]" value="\{{ $ind \}}"
\{{ isset($student->sex) && ($student->sex == $ind) ? 'checked' : '' \}}
>&nbsp;\{{ $val \}}
	</label>
@endforeach	
```

`\{{ isset($student->sex) && ($student->sex == $ind) ? 'checked' : '' \}}`的意思是，如果控制器注入了一个`Student`实例，那么判断这个实例的`sex`有没有被设置，有的话，就判断`$student->sex`这个值和`$ind`相不相等，相等的话，那就这个`input`默认被选中。相当于，能指定一个`input`默认被选中。

然而，如果控制器仅仅：

```php
$student = new Student();
return view('student.create', [
    'student' => $student,
]);
```

视图直接用`$student->sex`，不管用在哪里，都会报错。故此，一定要在控制器添加：`$student->sex = null;`:

```php
$student = new Student();
$student->sex = null; // 等于不赋值给$student->sex
return view('student.create', [
    'student' => $student,
]);
```

这样，在视图：

```php
\{{ isset($student->sex) && ($student->sex == $ind) ? 'checked' : '' \}}
```

先判断`$student->sex`有没有被设置再来做其他事情。

10. 视图中url传值：

```php
\{{ url('student/update', ['id' => $student->id]) \}}
```

# 三、Laravel简单操作技巧

## 1.Composer

### 1.包管理器

![2018-08-08_164522](/assets/images/laravel-develop-study/2018-08-08_164522.png)

### 2.Composer

![2018-08-08_164723](/assets/images/laravel-develop-study/2018-08-08_164723.png)

### 3.安装

![2018-08-10_224648](/assets/images/laravel-develop-study/2018-08-10_224648.png)

![2018-08-10_224728](/assets/images/laravel-develop-study/2018-08-10_224728.png)

### 4.镜像

![2018-08-10_224851](/assets/images/laravel-develop-study/2018-08-10_224851.png)

使用[Composer中国全量镜像服务](https://www.phpcomposer.com)作为本地项目的依赖管理工具的下载中心会更快。

### 5.使用Composer

```shell
# 创建配置文件以及初始化
composer init

# 搜索某个库
composer search monolog

# 查看库的信息
composer show --all monolog/monolog
```

添加库：

在配置文件`composer.json`中添加依赖和版本：

```shell
"require": {
    "monolog/monolog": "2.21.*"
}
```

	然后用`composer install`下载依赖，之后打开`vendor`目录，库将会下载在里面。

也可以用`composer require`声明依赖，它也会自动添加、下载、安装依赖：`composer require symfony/http-foundation`。

删除依赖：只需在`composer.json`删除对应的依赖，然后执行`composer update`即可。

### 6.使用Composer安装Laravel

- `composer create-project --prefer-dist laravel/laravel <别名>`
- 先安装Laravel安装器:`composer global require "laravel/installer"`, 再通过安装器安装框架：`laravel new blog`

## 2.Artisan

![1533975220842](/assets/images/laravel-develop-study//assets/images/laravel-develop-study/1533975220842.png)

![1533975343503](/assets/images/laravel-develop-study/1533975343503.png)

![1533975353745](/assets/images/laravel-develop-study/1533975353745.png)

### 1.用户认证(Auth)

#### 1. 生成Auth所需文件

	命令：

```shell
php artisan make:auth
```

	生成的路由内容：

```php
<?php
Auth::routes();

Route::get('/home', 'HomeController@index')->name('home');
```

`Auth::routes()`位置：`\vendor\laravel\framework\src\Illuminate\Routing\Router.php`的`auth`函数：

```php
    /**
     * Register the typical authentication routes for an application.
     *
     * @return void
     */
public function auth()
{
    // Authentication Routes...
    $this->get('login', 'Auth\LoginController@showLoginForm')->name('login');
    $this->post('login', 'Auth\LoginController@login');
    $this->post('logout', 'Auth\LoginController@logout')->name('logout');

    // Registration Routes...
    $this->get('register', 'Auth\RegisterController@showRegistrationForm')->name('register');
    $this->post('register', 'Auth\RegisterController@register');

    // Password Reset Routes...
    $this->get('password/reset', 'Auth\ForgotPasswordController@showLinkRequestForm')->name('password.request');
    $this->post('password/email', 'Auth\ForgotPasswordController@sendResetLinkEmail')->name('password.email');
    $this->get('password/reset/{token}', 'Auth\ResetPasswordController@showResetForm')->name('password.reset');
    $this->post('password/reset', 'Auth\ResetPasswordController@reset');
}
```

#### 2.数据迁移 --> 在数据库生成对应的表

![1534234217992](/assets/images/laravel-develop-study/1534234217992.png)

`Mysql`语句：

```mysql
CREATE TABLE IF NOT EXISTS students(
	'id' INT AUTO_INCREMENT PRIMARY KEY,
    'name' VARCHAR(255) NOT NULL DEFAULT '' COMMENT '姓名',
    'age' INT UNSIGNED NOT NULL DEFAULT 0 COMMENT '年龄',
    'sex' INT UNSIGNED NOT NULL DEFAULT 10 COMMENT '性别',
    'created_at' INT NOT NULL DEFAULT 0 COMMENT '新增时间',
    'updated_at' INT NOT NULL DEFAULT 0 COMMENT '修改时间'
)ENGINE=InnoDB DEFAULT CHARSET=UTF8
AUTO_INCREMENT=1001 COMMENT='学生表';
```

	完善迁移文件 --> **在`up`函数中添加数据表里的字段**：

```php
<?php

use Illuminate\Support\Facades\Schema;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Database\Migrations\Migration;

class CreateStudentsTable extends Migration
{
    /**
     * Run the migrations.
     *
     * @return void
     */
    public function up()
    {
        Schema::create('students', function (Blueprint $table) {
            $table->increments('id');
            $table->string('name'); // unsigned()表示非负的意思
            $table->integer('age')->unsigned()->default(0);
            $table->integer('sex')->unsigned()->default(10);
            $table->integer('created_at')->default(0);
            $table->integer('updated_at')->default(0);
            $table->timestamps();
        });
    }

    /**
     * Reverse the migrations.
     *
     * @return void
     */
    public function down()
    {
        Schema::dropIfExists('students');
    }
}
```

	将`database/migrations`下的迁移文件做迁移：

```shell
php artisan migrate
```

**迁移步骤：**

1. 新建迁移文件：`php artisan make:model Student -m`或者`php artisan make:migration create_students_table --create=students`。
2. 完善迁移文件，即在`up`函数里添加字段。
3. 做迁移：`php artisan migrate`

#### 3.数据填充 --> 一般填充测试数据

![1534235808674](/assets/images/laravel-develop-study/1534235808674.png)

1. 创建填充文件：`php artisan make:seeder StudentTableSeeder`:

![1534236147269](/assets/images/laravel-develop-study/1534236147269.png)

`DatabaseSeeder.php`：用于批量填充文件。

`StudentTableSeeder.php`：用于单个填充文件。

1. 执行填充文件

   - 单个填充文件：

     ```php
     // \database\seeds\StudentTableSeeder.php
     <?php
     
     use Illuminate\Database\Seeder;
     use Illuminate\Support\Facades\DB;
     
     class StudentTableSeeder extends Seeder
     {
         /**
          * Run the database seeds.
          *
          * @return void
          */
         public function run()
         {   
             // 导入两条数据
             DB::table('students')->insert([
                 ['name' => 'name1', 'age' => 23],
                 ['name' => 'name2', 'age' => 24],
             ]);
         }
     }
     ```

     执行：`php artisan db:seed --class=StudentTableSeeder`

   - 批量填充文件：

     ```php
     // \database\seeds\DatabaseSeeder.php
     <?php
     
     use Illuminate\Database\Seeder;
     
     class DatabaseSeeder extends Seeder
     {
         /**
          * Run the database seeds.
          *
          * @return void
          */
         public function run()
         {	// 将多个填充文件一起执行
             $this->call(StudentTableSeeder::class);
             $this->call(ArticleTableSeeder::class);
             $this->call(CommentTableSeeder::class);
         }
     }
     ```

     执行：`php artisan db:seed`

### 2.Laravel框架常用功能

#### 1.文件上传

![1534237010212](/assets/images/laravel-develop-study/1534237010212.png)

![1534237027967](/assets/images/laravel-develop-study/1534237027967.png)

配置文件：

```php
// config/filesystems.php
<?php
return [
	// 支持"local", "ftp", "s3", "rackspace"，默认使用本地端空间
    'default' => env('FILESYSTEM_DRIVER', 'local'), 

    'cloud' => env('FILESYSTEM_CLOUD', 's3'),
    
	// 磁盘
    'disks' => [
        'local' => [ // 本地端空间磁盘,名字叫local
            'driver' => 'local', // 驱动是本地端空间
            'root' => storage_path('app'), // 目录是storage/app
        ],
        'public' => [ // 本地端空间磁盘,名字叫public，因为驱动是本地端空间，所以它是本地端空间磁盘
            'driver' => 'local',
            'root' => storage_path('app/public'),
            'url' => env('APP_URL').'/storage',
            'visibility' => 'public',
        ],
        's3' => [ // 亚马逊的配置
            'driver' => 's3',
            'key' => env('AWS_KEY'),
            'secret' => env('AWS_SECRET'),
            'region' => env('AWS_REGION'),
            'bucket' => env('AWS_BUCKET'),
        ],
    ],
];
```

使用本地端空间来让laravel有文件上传的功能：

1. 在`config/filesystems.php`创建一个本地端空间磁盘，名字叫：uploads：

   ```php
   // config/filesystems.php
   <?php
   return [
       'default' => env('FILESYSTEM_DRIVER', 'local'), 
   
       'cloud' => env('FILESYSTEM_CLOUD', 's3'),
       
   	// 磁盘
       'disks' => [
           'local' => [ 
               'driver' => 'local', 
               'root' => storage_path('app'), 
           ],
           'public' => [ 
               'driver' => 'local',
               'root' => storage_path('app/public'),
               'url' => env('APP_URL').'/storage',
               'visibility' => 'public',
           ],
           'uploads' => [ // 创建了一个本地端空间磁盘，目录是storage/app/uploads
               'driver' => 'local',
               'root' => storage_path('app/uploads') // 现在这里进行配置，这个文件夹会自己生成
           ],
           's3' => [
               'driver' => 's3',
               'key' => env('AWS_KEY'),
               'secret' => env('AWS_SECRET'),
               'region' => env('AWS_REGION'),
               'bucket' => env('AWS_BUCKET'),
           ],
       ],
   ];
   ```

   位置：

   ![1534237760826](/assets/images/laravel-develop-study/1534237760826.png)

2. 控制器和路由：

   ```php
   // StudentController.php
   <?php
   
   namespace App\Http\Controllers;
   
   use App\Student;
   use Illuminate\Http\Request;
   use Illuminate\Support\Facades\Session;
   use Illuminate\Support\Facades\Storage;
   
   class StudentController extends Controller
   {
      public function upload(Request $request) {
          if ($request->isMethod('POST')) {
              // 获取上传来的文件
              $file = $request->file('source'); 
              
              if ($file->isValid()) {
                  // 判断文件是否上传成功
                  $originaName = $file->getClientOriginalName(); // 原文件名
                  $ext = $file->getClientOriginalExtension(); // 扩展名，后缀
                  $type = $file->getClientMimeType(); // 文件类型
                  $realPath = $file->getRealPath(); // 临时绝对路径，还没手动保存之前文件存放的位置
   
                  // 这种做法保证文件名称都不相同
                  $filename = date('Y-m-d-H-i-s').'-'.uniqid().'.'.$ext;
                  // 保存文件在config/filesystems.php中设置的disk里，返回一个bool，保存得成功不成功
                  $bool = Storage::disk('uploads')->put($filename, file_get_contents($realPath));
              }
          }
   
          return view("student.upload");
      }
   }
   ```

   ```php
   // web.php
   Route::get('/home', 'HomeController@index')->name('home');
   ```

3. 视图里要提交文件的表单：

   ```php
   // resources/views/student/upload.blade.php
   <div class="panel-body">
   	\{{--enctype="multipart/form-data"必须加这个属性，表单才可以使用文件上传功能--\}}
   	<form class="form-horizontal" method="POST" action="" enctype="multipart/form-data">
   		\{{ csrf_field() \}}
       	<div>
                <label for="file" class="col-md-4 control-label">请选择文件</label>
                <div class="col-md-6">		\{{--name值是source--\}}
                   <input id="file" type="file" class="form-control" name="source" required>
                </div>
            </div>
            <div class="form-group">
                <div class="col-md-8 col-md-offset-4">
                   <button type="submit" class="btn btn-primary">
                       确认上传
                   </button>
                </div>
             </div>
        </form>
   </div>
   ```

4. 可以通过更改`config/filesystems.php`里的`uploads`磁盘的空间为`public`目录底下的`uploads`目录。

![1534342816613](/assets/images/laravel-develop-study/1534342816613.png)

#### 2.发送邮件

![1534343099473](/assets/images/laravel-develop-study/1534343099473.png)

![1534343121043](/assets/images/laravel-develop-study/1534343121043.png)

	配置文件：

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

1. 在`.env`中进行配置：

```properties
MAIL_DRIVER=smtp # 使用的服务
MAIL_HOST=smtp.mailtrap.io # 服务器地址
MAIL_PORT=2525 # 服务器端口
MAIL_USERNAME=jim # 账号
MAIL_PASSWORD=passowrd
MAIL_ENCRYPTION=ssl # 协议
```

1. 控制器以及路由

```php
Route::any('mail', ['uses' => 'StudentController@mail']);
```

控制器：

- 以`raw`方式发送邮件：

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

- 以`html`方式发送邮件：

创建一个`html`文件，即视图：

```php
<!--resources/views/student/mail.blade.php-->
<!DOCTYPE html>
<html>
<head>
    <title>标题</title>
</head>
<body> <!--$name由控制器注入进来-->
<h1>Hello \{{ $name \}}</h1>
</body>
</html>
```

	控制器：

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

#### 3.缓存使用

![1534344890615](/assets/images/laravel-develop-study/1534344890615.png)

![1534344915362](/assets/images/laravel-develop-study/1534344915362.png)

![1534344930819](/assets/images/laravel-develop-study/1534344930819.png)

配置文件：

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

控制器：

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

	`add()`:添加。

```php
public function cache1() {
    // add(),如果对象已经存在,就添加失败，如果对象不存在，添加成功
    // 返回一个bool值,10是时间
    $bool = Cache::add('key1', 'val1', '10');
}
```

	`forever()`：永久的保存对象到缓存中。	

```php
public function cache1() {
    Cache::forever('key1', 'val1');
}
```

	`has()`:判断缓存中的一个`key`值存不存在。

```php
public function cache1() {
    if (Cache::has('key')) {
        $val = Cache::get('key')
    } else {
        echo "No"
    }
}
```

	`pull`:取缓存中的`key`值，然后删了这个`key`。

```php
public function cache1() {
    $val = Cache::pull('key');
}
```

	`forget()`:从缓存中删除对象，删除成功返回`true`，返回一个`bool`值。

```php
public function cache1() {
    $bool = Cache::forget('key');
}
```

#### 4.错误和日志

![1535095566213](/assets/images/laravel-develop-study/1535095566213.png)

![1535095599480](/assets/images/laravel-develop-study/1535095599480.png)

1. `debug`模式：开发模式，调试模式。

可在`.env`里开启和调试：

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

	默认是开启调试模式的，如果发生错误，`laravel`会在网页打印出错误栈。
	
	**上线了一定要关闭调试模式！！**

1. `http`异常

![1535096147008](/assets/images/laravel-develop-study/1535096147008.png)

自定义`http`异常：

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

`http`异常的视图位置：

`vendor\laravel\framework\src\Illuminate\Foundation\Exceptions\views`:

![1535098035926](/assets/images/laravel-develop-study/1535098035926.png)

1. 日志

![1535098224286](/assets/images/laravel-develop-study/1535098224286.png)

`config/app.php`：

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

	配置日志模式：

```php
# 在.env中进行配置
# APP_LoG原本的.env里是没有的，是自己添加的，只能配置"single", "daily", "syslog", "errorlog"这几种模式
APP_LoG=single 
APP_LOG_LEVEL=debug
```

	这样是会在![1535098804878](/assets/images/laravel-develop-study/1535098804878.png)这里生成日志文件:`laravel.log`。
	
	使用日志：

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

	`daily`的`log`模式，会每天生成一个日志：

![1535099439063](/assets/images/laravel-develop-study/1535099439063.png)



















[看到这里](https://www.imooc.com/video/13341)

























---
layout: post
title: Laravel学习笔记
---
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
\{{ $name \}} \{{ $age \}}
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

## 2.数据库操作

**Laravel提供了DB facade（原始查找）、查询构造器和Eloquent ORM三种操作数据库的方式。**

### 1.连接数据库(config/database.php + .env)

打开config/database.php,找到：

```php
// 表示默认要连接的数据库是mysql
'default' => env('DB_CONNECTION', 'mysql'),
```

再往下找到：

```php
// 下面的env(..., ...)其实就是根目录的.env文件里的信息
'mysql' => [
    'driver' => 'mysql',
    'host' => env('DB_HOST', '127.0.0.1'),
    'port' => env('DB_PORT', '3306'),
    'database' => env('DB_DATABASE', 'forge'),
    'username' => env('DB_USERNAME', 'forge'),
    'password' => env('DB_PASSWORD', ''),
    'unix_socket' => env('DB_SOCKET', ''),
    'charset' => 'utf8mb4',
    'collation' => 'utf8mb4_unicode_ci',
    'prefix' => '', // 表前缀
    'strict' => true,
    'engine' => null,
],
```

打开.env,找到:

```php
DB_CONNECTION=mysql
DB_HOST=127.0.0.1
DB_PORT=3306
DB_DATABASE=laravel5
DB_USERNAME=root
DB_PASSWORD=
```

数据库连接完成。

### 2.使用DB facade实现CURD

CURD：增删改查

```php
// App/Http/Controllers/ArticleController.php，控制器里操作数据库
<?php

namespace App\Http\Controllers;
use App\Article;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\DB;

class ArticleController extends Controller
{
    public function operate(){
        // 插入
        $bool = DB::insert('insert into student(name, age) value(?, ?)', ['Jim', 18]);
        var_dump($bool); // 返回插入成不成功的值，true或false
        
        // 更新
        $num = DB::update('update student set age = ? where name = ?', [20, 'Jim']);
        var_dump($num); // 返回修改的行数
        
        // 查询
        $students = DB::select('select * from student where id > ?', [1001]);
        dd($students); // 返回查询结果，是个数组
        
        // 删除
        $num = DB::delete('delete from student where id > ?', [1001]);
        var_dump($num); // 返回被删除的行数

    }
}
```

var_dump(), dd()，都是调试代码，都能将()里的东西打印出来。

### 3.查询构造器

#### 1.新增数据

```php
// App/Http/Controllers/HomeController.php
public function query(){
        // 插入成功返回一个布尔值
        $bool = DB::table('student')->insert(
            ['name' => 'Jim', 'age' =>  18]
        );
        // 插入成功返回插入的id
        $id = DB::table('student')->insertGetId(
            ['name' => 'Jim', 'age' => 18]
        );
        // 插入多条数据
        $id = DB::table('student')->insert(
            ['name' => 'name1', 'age' => 18],
            ['name' => 'name2', 'age' => 18],
            ['name' => 'name3', 'age' => 18],
            ['name' => 'name4', 'age' => 18]
        );
    }
```

#### 2.更新数据

```php
// App/Http/Controllers/HomeController.php   
public function query(){
        // 将student表中id=2的元组中的age更新为30，返回的是受影响的行数
        $num = DB::table('student')
            ->where('id', 12) // 更新数据一定要带条件
            ->update(['age' => 30]);
        // 自增和自减
        $num = DB::table('student')->increment('age'); // 默认自增1
        $num = DB::table('student')->increment('age', 3); // 自增3
        $num = DB::table('student')->decrement('age'); // 默认自减1
        $num = DB::table('student')->decrement('age', 3); // 自减3
        // 将student表中id=12的元组的age自增3，同时name改为Jim
        $num = DB::table('student')
            ->where('id', 12)
            ->decrement('age', 3, ['name' => 'Jim']);
    }
```

#### 3.删除数据 

```php
// App/Http/Controllers/HomeController.php    
public function query(){
        // 删除student表中id=12的元组，返回受影响的行数
        $num = DB::table('student')
            ->where('id', 12)
            ->delete();
        // 删除student表中id>=12的元组，返回受影响的行数
        $num = DB::table('student')
            ->where('id', '>=', 12)
            ->delete();
        // 删除表，不返回任何东西
        DB::table('student')->truncate();
    }
```

#### 4.查询数据

get(), first(), where(), pluck(), lists(), select(), chunk().

```php
// App/Http/Controllers/HomeController.php  
public function query(){
        // get(),返回的是所有的表数据，一个列表
        $student = DB::table('student')->get();
        // first(),返回的是第一条记录
        $student = DB::table('student')->first();
        $student = DB::table('student') // 以student表的id进行倒序排序，获取第一条数据
            ->orderBy('id','desc')
            ->first();
        // where()
        $student = DB::table('student')
            ->where('id', '>=', 122)
            ->get();
        $student = DB::table('student') // 加多个条件查询
            ->whereRaw('id >= ? and age > ?', [122, 34])
            ->get();
        // pluck(),返回字段,是个列表
        $student = DB::table('student') // 返回student表的name字段
        ->pluck('name');
        // lists(),返回字段
        $student = DB::table('student') // 返回student表的name字段
        ->lists('name');
        $student = DB::table('student') // 返回student表的name字段
        ->lists('name', 'id');          // 但是这个列表中的索引用的是id
        // select()，返回的是指定的字段
        $name = DB::table('student')
            ->select('id', 'name', 'age')
            ->get();
        // chunk()，有时候数据太多，一次性获取会太慢，所以就要分段进行获取
        $name = DB::table('student')->chunk(50, function ($student){ // 每次获取50条元组，这50条元组赋值给闭包中的$student
            if( <条件> ){       // 当满足条件的时候，就会返回false，一旦返回false，程序就停止查询，所以可以通过设定条件让程序只查询几次就可以了
                return false;
            }
        });
    }
```

#### 5.聚合函数

count(), avg(), max(), sum(), min().

```php
// App/Http/Controllers/HomeController.php 
public function query(){
        // 返回元组的个数
        $sum = DB::table('student')->count();
        // 返回student表中age字段的最大值
        $sum = DB::table('student')->max('age');
        // 返回student表中age字段的最小值
        $sum = DB::table('student')->min('age');
        // 返回student表中age字段的值的平均值
        $sum = DB::table('student')->avg('age');
        // 返回student表中age字段的值的总和
        $sum = DB::table('student')->sum('age');
    }
```

### 4.Eloauent ORM

在laravel中用model跟数据库中的表进行交互，laravel自带的Eloquent ORM用来实现数据库操作。

#### 1.创建model

在App下面创建一个Student的model类：

```php
<?php

namespace App;

use Illuminate\Database\Eloquent\Model;

class Student extends Model
{
    // 指定表名，没有指定的话，默认为该模型的复数即students
    protected $table = 'student';

    // 指定主键，默认是表中的id字段
    protected $primaryKey = 'id';

}
```

这样，一个model就创建好了。

#### 2.使用model

在model对应的controller中使用model。

```php
<?php

namespace App\Http\Controllers;

class StudentController
{
    public function orm() {
        // all(),查询表的所有记录，返回一个集合collection
        $students = Student::all();
        // 返回id为12的元组
        $student = Student::find(12);
        // findOrFail(),根据指定查找，如果没有找到，返回异常
        $student = Student::findOrFail(12); // id为12的元组找不到就报错
    }
}
```

在ORM中使用查询构造器：

```php
<?php

namespace App\Http\Controllers;

class StudentController
{
    public function orm() {
        // 查询所有，返回一个集合collection
        $student = Student::get();
        
        $student = Student::where('id', '>', '34')
            ->orderBy('age', 'desc')
            ->first();
        
        Student::chunk(2, function($stuent){
            var_dump($student);
        });
        
        $num = Student::count();
        
        $max = Student::where('id', '>', 1002)->max('age');
              
    }
}
```

#### 3. 自定义时间戳及批量赋值

```php
// Student model
// App/Student.php
<?php

namespace App;


use Illuminate\Database\Eloquent\Model;

class Student extends Model
{
    // 指定表名，没有指定的话，默认为该模型的复数即students
    protected $table = 'student';

    // 指定主键，默认是表中的id字段
    protected $primaryKey = 'id';

    // 一般情况下模型对象向数据库增加数据时还会附加一个时间戳，
    // 如果不想要，在这里将$timestamps设置为false即可
    protected $timestamps = true;
    // 该函数与上面的$timestamps=true结合在一起给增添的字段附加一个时间戳
    protected function getDateFormat()
    {
        return time(); // 返回给我们的时间将会是格式化好的
    }
    // 如果我们不想格式化，让模型给我们返回一个时间戳（我们自己之后利用
    // 这个时间戳做自己想做的事。用下面这个函数：
    protected function asDateTime($value)
    {
        return $value;
    }
}
```

```php
// 在StudentConller这个控制器中操纵Student这个model
// App/Http/Controllers/StudentConller.php
<?php

namespace App\Http\Controllers;


class StudentController
{
    public function orm() {

        $student = new Student();
        $student->name = 'Jim';
        $student->age = 12;
        $bool = $student->save(); // 保存数据到数据库直接这样就行，返回一个bool
        // $student->created_at会返回一个时间戳，这个已经在Student这个model设置好了
        // 然后我们用这个时间戳自己再来格式化并打印
        echo data('Y-m-d H:i:s', $student->created_at);
    }
}
```

批量赋值数据：

```php
// App/Http/Controllers/StudentConller.php
<?php

namespace App\Http\Controllers;


class StudentController
{
    public function orm() {
		// 使用create()新增数据
        $student = Student::create(
        	['name' => 'Jim', 'age' => 23]
        );
    }
}
```

```php
// App/Student.php
<?php

namespace App;

use Illuminate\Database\Eloquent\Model;

class Student extends Model
{    // 指定允许批量赋值的model的字段，然后controller里就可以
    // 用model的create()批量赋值数据
    protected $fillable = ['name', 'age'];

    // 指定不允许批量赋值的model的字段
    protected $guarded = [];
}
```

其他新增数据的方法：

```php
// 以字段查找某个元组，如果没有那就创建
$student = Student::firstOrCreate(
    ['name' => 'Jim']
);

// 以字段查找某个元组，如果没有那就创建
$student = Student::firstOrNew(
    ['name' => 'Jim']
);
// firstOrNew是不会将数据保存数据库的，如果需要保存，
// 则自己编写以下的保存代码,返回是个bool，即保存成不成功
$bool = $student->save();
```

#### 4.修改数据

```php
// App/Http/Controllers/StudentConller.php
<?php

namespace App\Http\Controllers;

use App\Student;

class StudentController
{
    public function orm() {
        // 1.通过模型更新数据，返回的$bool代表保存得成不成功
        $student = Student::find(2021);
        $student->name = 'Jim';
        $bool = $student->save();
        // 2.利用查询语句来更新数据
        $num = Student::where('id', '>', 120)
            ->update(
                ['age' => 23]
            );
    }
}
```

#### 5.删除数据

```php
public function orm() {
    // 1.通过模型删除,返回一个代表删除成不成功的$bool
    $student = Student::find(201);
    $bool = $student->delete(); // 删除不到这个元组就会报错

    // 2.通过主键删除,返回删除的行数，即一个删除了几行
    $num = Student::destroy(1021);
    // 删除多个id的元组：
    $num = Student::destroy(1021, 33);
    // 或者：
    $num = Student::destroy([2021, 33]);

    // 3.通过查询语句删除,返回删除的行数
    $num = Student::where('id', '>', 23)->delete();
}
```

## 3.Blade模板

### 1.模板继承

![20180805224923.png](/assets/images/laravel-develop-study/20180805224923.png)

父模板(views.layouts)：

```php
// resources/views/layouts.blade.php
\{{--@section,展示片段内容--\}}
@section('header')
    头部
@show

@section('sidebar')
    侧边栏
@show

\{{--@yield，展示字符串内容--\}}
@yield('content', '主要内容')
```

子模板(views.student.child):

```php
// resources/views/student/child.blade.php
\{{--1.继承哪个模板--\}}
@extends('layouts')

\{{--2.替换父模板中@section的header内容，输出父模板对应地方的父内容--\}}
@section('header')
    @parent
    header
@stop
\{{--或者--\}}
\{{--重写父模板中@section的sidebar内容，不会输出父模板对应地方的父内容--\}}
@section('sidebar')
    sidebar
@stop

\{{--3.替换父模板中@yield的content内容--\}}
@section('content')
    content
@stop
```

controller中访问的是子模板：

```php
// App/Http/Controllers/StudentController.php
<?php

namespace App\Http\Controllers;


use App\Student;

class StudentController
{
    public function view() {
        return view('student.child'); // 访问views目录底下的student/child.blade.php
    }
}
```

### 2.基础语法：

```php
\{{--resources/views/student/child.blade.php--\}}
\{{--1.模板中输出PHP变量，该变量由控制器传入--\}}
\{{ $name \}}

\{{--2.模板中调用PHP代码,$name和$arr两个变量都由控制器中传进来--\}}
\{{ time() \}}
\{{ date('Y-m-d H:i:s', time()) \}}
\{{--判断$arr数组中是否有$name,有返回true，没有返回false--\}}
\{{ in_array($name, $arr) ? 'ture': 'false' \}}
\{{--判断$name是否存在,有返回$name值，没有返回字符串'default'--\}}
\{{ isset($name) ? $name: 'default' \}}
\{{--或者--\}}
\{{ $name or 'default' \}}

\{{--3.原样输出，视图渲染时输出\{{ $name \}}--\}}
@\{{ $name \}}

\{{--4.模板注释--\}}
\{{--xxxx--\}}

\{{--5.子模板中引入子视图--\}}
@include('student.common')
\{{--子视图中有占位符$msg,在这里将msg赋值并传给子视图--\}}
@include('student.common', ['msg' => 'error'])
```

控制器传入值：

```php
class StudentController
{
    public function view() {
        $name = 'Jim';
        $arr = ['a', 'b'];
        return view('student.child', [
            'name' => $name, // 传入值
            'arr' =>$arr, // 传入数组
        ]);
    }
}
```

子视图：

```php
\{{--resources/views/student/common.blade.php--\}}
\{{--$msg是个占位符，等着别处传过来值给它赋值--\}}
\{{ $msg \}}
```

### 3.模板中流程控制

```php
\{{--resources/vies/student/child.blade.php--\}}

\{{--if--\}}
@if ($name == 'Jim')
    Jim
@elseif($name == 'a')
    a
@else
    b
@endif

\{{--unless,相当于if的取反--\}}
@unless( $name == 'Jim' )
    output Jim
@endunless

\{{--for--\}}
@for ($i=0; $i<2; $i++)
    <p>\{{ $i \}}</p>
@endfor

\{{--foreach,遍历对象列表或者数组--\}}
@foreach($students as $student) \{{--该$student对象列表由控制器传入--\}}
    <p>\{{ $student->name \}}</p> \{{--返回$student对象的name属性--\}}
@endforeach

\{{--forelse--\}}
@forelse($students as $student)
    <p>\{{ $student->name \}}</p>
@empty\{{--如果对象列表为空--\}}
    <p>null</p>
@endforelse
```

控制器中将对象数组传给视图：

```php
<?php

namespace App\Http\Controllers;

use App\Student;

class StudentController
{
    public function view() {
        $students = Student::get(); // 从model中获取所有的元组对象，组成一个对象列表
        $name = 'Jim';
        return view('student.child', [
            'name' => $name,
            'students' => $students,
        ]);
    }
}
```

### 4.模板中url

路由：

```php
// 路由名字：urlTest， 路由别名：urlAlias， 控制器及方法：StudentController@urlTest 
Route::any('urlTest', ['as' => 'urlAlias', 'uses' => 'StudentController@urlTest']);
```

模板中生成url：

```php
\{{--resources/views/student/child.blade.php--\}}
\{{--1.指定的路由名字--\}}
<a href="\{{ url('urlTest') \}}">This is url.</a>
\{{--2.控制器+方法名--\}}
<a href="\{{ action('StudentController@urlTest') \}}">This is url.</a>
\{{--3.路由的别名--\}}
<a href="\{{ route('urlAlias') \}}">This is url.</a>
```

# 二、laravel表单

## 1.request

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

## 2.session

session的配置文件在config/session.php中。

使用session的三种方法：

* HTTP request类的session()方法
* session()辅助函数
* Session facade

config/session.php部分解析：

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

**先在路由表中添加要使用session()的路由的web中间件：**

```php
// routes/web.php
Route::group(['middleware' => ['web']], function (){ // 用路由组的方式同时给session1和session2两个路由添加webs中间价
    Route::any('session1', ['uses' => 'StudentController@session1']);
    Route::any('session2', ['uses' => 'StudentController@session2']);
});
```

1.HTTP request的session()

先访问session1方法，会往session放入一个key，然后访问session2方法，会从session中取出key值。

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

2.直接session()

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

3.Session facade

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

其他用法：

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

## 3.response

响应的类型：字符串， 视图， Json， 重定向。

1. Json

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

2. 重定向

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

	或者：
	
	action(), 控制器+方法

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

	或者：
	
	route(), 路由别名

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

	或者：
	
	back(),返回上一个页面

```php
class StudentController
{
    public function response() {
        redirect()->back();
    }
}
```

## 4.Middleware

Laravel中间件提供了一个方便的机制来过滤进入应用程序的HTTP请求。

假设一个场景：有一个活动，指定日期开始前只能访问宣传页面，活动开始日期后才可以访问活动页面。

1. 新建控制器方法

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

2. 新建中间件

![2018-08-06_213029](/assets/images/laravel-develop-study/2018-08-06_213029.png)

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

	在Kernel.php中注册中间件:

![2018-08-06_213247](/assets/images/laravel-develop-study/2018-08-06_213247.png)

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

	如果想注册全局中间件，则在Kernel.php里的这里注册：

```php
protected $middleware = [
    \Illuminate\Foundation\Http\Middleware\CheckForMaintenanceMode::class,
    \Illuminate\Foundation\Http\Middleware\ValidatePostSize::class,
    \App\Http\Middleware\TrimStrings::class,
    \Illuminate\Foundation\Http\Middleware\ConvertEmptyStringsToNull::class,
    \App\Http\Middleware\TrustProxies::class,
];
```

3. 使用中间件(在路由文件中)

```php
// 访问活动页面就会跳入这个中间件
Route::group(['middleware' => ['activity']], function () {
    Route::any('activity_running', ['uses' => 'StudentController@activity_running']);
});
// 然后中间件根据判断就会重定向到这个路由
Route::any('activity_advertise', ['uses' => 'StudentController@activity_advertise']);
```

4. 其他

中间件有前置操作和后置操作。

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

## 5.表单案例笔记

1.静态资源路径：`\{{ asset() \}}`

```php
    <link href="\{{ asset('static/css/bootstrap.min.css') \}}" rel="stylesheet">
```

这个路径是相对于public文件夹下的，也就是文件位置：![2018-08-07_134524](/assets/images/laravel-develop-study/2018-08-07_134524.png)

2. 表单分页

   控制器下用`Student::paginate(num)`取得所有的数据，然后将数据再传给视图。

```php
<?php

namespace App\Http\Controllers;


use App\Student;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Session;

class StudentController extends Controller
{
    public function index() {
        $students = Student::paginate(3); // '3'表示每页显示3条记录

        return view('student.index', [
            'students' => $students,
        ]);
    }
}
```

	在需要用到分页的视图里，直接` \{{ $students->render() \}}`就行了，这条语句会自动生成含有`ul`和`li`的分页信息的。

```php
<!--student.index视图的分页内容-->
	<!--分页-->
    <div class="pull-right">
        \{{ $students->render() \}}
    </div>
```

3. 默认选中项

```php
<ul class="nav nav-pills nav-stacked">
<li role="presentation" class="\{{ Request::getPathInfo() == '/student/index' ? 'active' : '' \}}"><a href="\{{ url('student/index') \}}">学生列表</a></li>
<li role="presentation" class="\{{ Request::getPathInfo() == '/student/create' ? 'active' : '' \}}"><a href="\{{ url('student/create') \}}">新增学生</a></li>
</ul>
```

用`Request::getPathInfo()`判断当前路径是否`/student/index`或者`/student/create`，是的话那就`active`,表示选中，不然就为空` `，不选中。注意`/student/index`和`/student/create`最前面的`/`是要有的。

4. 表单提交

* 提交到`save()`:

```php
<form action="\{{ url('student/save') \}}" method="POST"> 
    <!-- 1.设置action路径为'student/save',即提交到student/save -->

    <label for="inputName" >姓名：</label>
        <input type="text" name="Student[name]" id="inputName" placeholder="请输入姓名"> 
        <!-- 2.将各input的name属性都设为统一的数组，即统一都为Student的数组，只是下标不一样 -->

    <label for="inputAge">年龄：</label>
        <input type="text" name="Student[age]" id="inputAge" placeholder="请输入年龄">

    <div>
        <label>性别：</label>
        <div>
            <label>
                <input type="radio" name="Student[sex]" value="man">男
            </label> <!-- 3.注意radio的话可以这么设置，设两次Studnet[sex] -->
            <label>
                <input type="radio" name="Student[sex]" value="woman">女
            </label>
        </div>
    </div>
    <button type="submit">提交</button>
</form>
```

	添加一条路由：

```php
Route::any('student/save', ['uses' => 'StudentController@save']);
```

	在控制器中添加save():

```php
public function save(Request $request){
    $data = $request->input('Student');

    $student = new Student();
    $student->name = $data['name'];
    $student->age = $data['age'];
    $student->sex = $data['sex'];

    if($student->save()) {
        return redirect('student/index');
    } else {
        return redirect()->back();
    }
```

* 提交到当前页面

```php
<form action="" method="POST"> 
    <!-- 1.action没设置，默认提交到当前页面 -->

    <label for="inputName" >姓名：</label>
        <input type="text" name="Student[name]" id="inputName" placeholder="请输入姓名"> 
        <!-- 2.将各input的name属性都设为统一的数组，即统一都为Student的数组，只是下标不一样 -->

    <label for="inputAge">年龄：</label>
        <input type="text" name="Student[age]" id="inputAge" placeholder="请输入年龄">

    <div>
        <label>性别：</label>
        <div>
            <label>
                <input type="radio" name="Student[sex]" value="man">男
            </label> <!-- 3.注意radio的话可以这么设置，设两次Studnet[sex] -->
            <label>
                <input type="radio" name="Student[sex]" value="woman">女
            </label>
        </div>
    </div>
    <button type="submit">提交</button>
</form>
```

	不用添加一条路由，只是注意当前页面路由要能有POST方法：

```php
Route::any('student/create', ['uses' => 'StudentController@create']);
```

	在控制器中修改create():

```php
public function create(Request $request){
    if ($request->isMethod('POST')) { // 添加这个判断
        $data = $request->input('Student');
        if (Student::create($data)) { // 调用create()会采用批量赋值，所以要确保model中要有protected $fillable
            return redirect('student/index');
        } else {
            return redirect()->back();
        }
    }

    return view('student.create'); // 不是POST方法的话，就直接跳转到create视图中去
}
```

5. 操作提示

创建一个提示信息子视图：

```php
<!--message.blade.php-->
@if (Session::has('success'))
<!--成功提示框-->
<div class="alert alert-success alert-dismissable" role="alert">
    <button type="button" class="close" data-dismiss="alert" aria-label="Close">
        <span aria-hidden="true">&times;</span>
    </button>
    <strong>成功!!</strong>\{{ Session::get('success') \}}！
</div>
@endif
@if (Session::has('error'))
<!--失败提示框-->
<div class="alert alert-danger alert-dismissable" role="alert">
    <button type="button" class="close" data-dismiss="alert" aria-label="Close">
        <span aria-hidden="true">&times;</span>
    </button>
    <strong>失败!!</strong>\{{ Session::get('error') \}}！
</div>
@endif
```

位置：![2018-08-07_200359](/assets/images/laravel-develop-study/2018-08-07_200359.png)

哪个视图需要这个信息提示框就直接`@include('common.message')`过去。

控制器中使用：

```php
public function create(Request $request){
    if ($request->isMethod('POST')) {
        $data = $request->input('Student');
        if (Student::create($data)) {
            return redirect('student/index')->with('success', '添加成功');
            // 在控制器中调用暂存数据的方法，只能访问一次
        } else {
            return redirect()->back();
        }
    }
```

**这样，当数据保存成功然后返回的index页面时，就会向`session`中注入`success`的属性信息，当`common.message`页面中判断`session`属性存在时，就会显示信息在有`@include('common.message')`的视图里。**

记住，一定要将需要`session`的路由加进到`web`中间件中：

```php
Route::group(['middleware' => ['web']], function () {
    Route::get('student/index', ['uses' => 'StudentController@index']);
    Route::any('student/create', ['uses' => 'StudentController@create']);
    Route::post('student/save', ['uses' => 'StudentController@save']);
});
```

中间件`web`还能防止xxs攻击，所以，如果路由里有表单提交的话，一定要在表单视图中加入`\{{ csrf_field() \}}`。

```php
<!--create.blade.php-->
@section('content')
<form action="\{{ url('student/save') \}}" method="POST">

    \{{ csrf_field() \}} <!--防止xxs攻击-->

    <label for="inputName" >姓名：</label>
        <input type="text" name="Student[name]" id="inputName" placeholder="请输入姓名"> 

    <label for="inputAge">年龄：</label>
        <input type="text" name="Student[age]" id="inputAge" placeholder="请输入年龄">

    <button type="submit">提交</button>
</form>
@stop
```

6. 表单数据验证

* 控制器验证

```php
public function create(Request $request){
    if ($request->isMethod('POST')) {

        $this->validate($request, [
            'Student.name' => 'required|min:2|max:5',// 数组形式要写成这样子Student.name <= Student[name]
            'Student.age' => 'required|integer|max:2',
            'Student.sex' => 'required|integer'
        ], [
            'required' => ':attribute 为必选项',
            'min' => ':attribute 长度不符合要求',
            'integer' => ':attribute 必须为整数',
            'max' => ':attribute 长度不符合要求',
        ], [
            'Student.name' => '姓名',
            'Student.age' => '年龄',
            'Student.sex' => '性别',
        ]);


        $data = $request->input('Student');
        if (Student::create($data)) { // 调用create()会采用批量赋值，所以要确保model中要有protected $fillable
            return redirect('student/index')->with('success', '添加成功');
        } else {
            return redirect()->back();
        }
    }
```

验证通过是，程序将会继续往下执行，不通过时，表单将会重定向到上个页面并将错误抛给`session`，该错误属性是`$errors`，这个`$errors`是个数组，可以在全局的视图中捕获的。

然后，自定义错误内容：

```php
$this->validate($request, [
    'Student.name' => 'required|min:2|max:5',// 数组形式要写成这样子Student.name <= Student[name]
    'Student.age' => 'required|integer|max:2',
    'Student.sex' => 'required|integer'
], [
    'required' => ':attribute 为必选项', // :attribute是个占位符，表示对应的Student.name、Student.age、Student.sex
    'min' => ':attribute 长度不符合要求',
    'integer' => ':attribute 必须为整数',
    'max' => ':attribute 长度不符合要求',
], [
    'Student.name' => '姓名',
    'Student.age' => '年龄',
    'Student.sex' => '性别',
]);
```

	譬如：当因为`Student.name`的`required`不通过验证时，就会抛出`姓名 为必选项`。

![2018-08-07_210700](/assets/images/laravel-develop-study/2018-08-07_210700.png)

	如果不这样自定义的话，那抛出来的错误内容信息就是`Student.name is required.`，这个不太友好。

将用于捕获验证错误信息的程序放入一个视图：

```php
// common.validator.blade.php
@if (count($errors))
    <div class="alert alert-danger">
        <ul>
            @foreach($errors->all() as $error) // 将所有的错误都输出
            <li>\{{ $error \}}</li>
            @endforeach
        </ul>
    </div>
@endif
```

哪个视图需要输出验证错误信息的再来`@include('common.validator')`:

```php
@section('content')

    @include('common.validator') <!--需要输出验证信息的地方-->

    <form action="\{{ url('student/save') \}}" method="POST">
        \{{ csrf_field() \}}
        <label for="inputName" >姓名：</label>
            <input type="text" name="Student[name]" id="inputName" placeholder="请输入姓名"> 

        <label for="inputAge">年龄：</label>
            <input type="text" name="Student[age]" id="inputAge" placeholder="请输入年龄">

        <button type="submit">提交</button>
    </form>
@stop
```

* Validator类验证

```php
public function create(Request $request){
    if ($request->isMethod('POST')) {
        
        $validator = \Validator::make($request->input(), [
            'Student.name' => 'required|min:2|max:5',
            'Student.age' => 'required|integer|max:2',
            'Student.sex' => 'required|integer'
        ], [
            'required' => ':attribute 为必选项',
            'min' => ':attribute 长度不符合要求',
            'integer' => ':attribute 必须为整数',
            'max' => ':attribute 长度不符合要求',
        ], [
            'Student.name' => '姓名',
            'Student.age' => '年龄',
            'Student.sex' => '性别',
        ]);
        if ($validator->fails()) { // 这种方法验证也就是手动验证,在函数体里面还能做其他的事
            return redirect()->back()->withErrors($validator);
        } // 注意要用withErrors($validator)注册错误信息

        $data = $request->input('Student');
        if (Student::create($data)) { // 调用create()会采用批量赋值，所以要确保model中要有protected $fillable
            return redirect('student/index')->with('success', '添加成功');
        } else {
            return redirect()->back();
        }
    }

    return view('student.create');
}
```

在视图中调用指定的错误信息：`\{{ $errors->first('Student.name') \}}`,如果有自定义错误内容`姓名 为必选项`，则输出的是错误对应（`Student.name`）的自定义内容。

7. 数据保持

只需要在上述表单验证代码中加入`->withInput()`:

![2018-08-07_222555](/assets/images/laravel-develop-study/2018-08-07_222555.png)

`withInput()`自动默认将`$request`作为参数传进去，然后再在需要的`input`组件添加`value="\{{ old('Student')['name'] \}}"`即可：

```php
<input type="text" value="\{{ old('Student')['name'] \}}" name="Student[name]" class="form-control" id="inputName" placeholder="请输入姓名">
```

这样子，在提交表单而发生错误后，重定向到原先的表单填写页面时，它会自动补全在`input`之前填过的信息：![2018-08-07_223016](/assets/images/laravel-develop-study/2018-08-07_223016.png)

**注：**

`min:2|max:5`：
当要验证的值为数字时，那么这个数字要大于等于`2`小于等于`5`（`4`满足要求）；
当要验证的值为字符串，那么这个字符串不管是中英混合，还是全英，还是全文，它的长度要大于等于`2`小于等于`5`（`hh哈哈`长度为4，满足要求）。

8. 自定义数据库取出来的值

譬如，当存储性别时（有’未知‘，’男‘， ’女‘）,数据库真正所对应存储的是10， 20， 30。所以这时候就要自定义数据库取出来的值。

首先，在对应的model中写入一个函数：

```php
// App\Student.php
<?php

namespace App;

use Illuminate\Database\Eloquent\Model;

class Student extends Model
{
    protected $fillable = ['name', 'age', 'sex'];

    protected $table = 'student';

    public $timestamps = true;

    protected function getDateFormat()
    {
        return time();
    }
    protected function asDateTime($value)
    {
        return $value;
    }

    // 以下函数能将数字转化为对应的汉字，数字用来存储，汉字用来显示
    const SEX_UN = 10; // 定义三个常量
    const SEX_BOY = 20;
    const SEX_GIRL = 30;

    public function sex($ind = null) {
        $arr = [
            self::SEX_UN => '未知',
            self::SEX_BOY => '男',
            self::SEX_GIRL => '女',
        ];
        if ($ind !== null) { // 注意不等于是 !==
            return array_key_exists($ind, $arr) ? $arr[$ind] : $arr[self::SEX_UN];
        }
        return $arr;
    }

}
```

`Studen`这个model里有个`sex`函数，`sex()`时能将所有的性别取出来，传入相应的`index`时能取出对应的汉字性别。

接着，在控制器中将model注入到视图中去。

```php
public function create(){
    $student = new Student(); //先将model实例化
    return view('student.create', [
        'student' => $student // 然后再注入到视图里
    ]);
}
```

然后，在视图中就可以调用model的性别转化函数`sex()`。

```php
@foreach($students as $student)
    <tr>
        <td>\{{ $student->id \}}</td>
        <td>\{{ $student->name \}}</td>
        <td>\{{ $student->age \}}</td>
        <td>\{{ $student->sex($student->sex) \}}</td>
    </tr> <!--储存到model中的性别是个数字，$student->sex是个数字，$student->sex()才将这个数字转化对应性别为中文汉字-->
@endforeach
```

```php
@foreach($student->sex() as $ind=>$val)
    <label class="radio-inline"> <!--sex()返回一个数组，$ind是10,20,30,$val是未知，男，女-->
        <input type="radio" name="Student[sex]" value="\{{ $ind \}}">&nbsp;\{{ $val \}}
    </label> <!--最后提交到数据库是，如果是未知，那Student[sex]=10，男：Student[sex]=10等-->
@endforeach
```

	上面这样写就有这个效果：![2018-08-08_104915](/assets/images/laravel-develop-study/2018-08-08_104915.png)，就不必在页面上写很多个`input`标签了。

9. 遇到的坑：`App\Student::sex must return a relationship instance`

情况：

	在控制器中,当访问`student.create`时，会以这样注入一个model实例的方式：

```php
public function create(){
    $student = new Student();
    return view('student.create', [
        'student' => $student,
    ]);
}
```

	使得`create`视图里的`input`组件不用写多个，也能变成：![2018-08-08_104915](/assets/images/laravel-develop-study/2018-08-08_104915.png)

```php
@foreach($student->sex() as $ind=>$val)
    <label class="radio-inline">
    	<input type="radio" name="Student[sex]" value="\{{ $ind \}}">&nbsp;\{{ $val \}}
	</label>
@endforeach
```

	但是，`create`视图的这个部分其实也是`@include('student._form')`的，上面 的`input`标签也是放在这个通用的`_form`视图里的。所以实际上`_form.blade.php`：

```php
@foreach($student->sex() as $ind=>$val)
    <label class="radio-inline">
    	<input type="radio" name="Student[sex]" value="\{{ $ind \}}"
\{{ isset($student->sex) && ($student->sex == $ind) ? 'checked' : '' \}}
>&nbsp;\{{ $val \}}
	</label>
@endforeach	
```

`\{{ isset($student->sex) && ($student->sex == $ind) ? 'checked' : '' \}}`的意思是，如果控制器注入了一个`Student`实例，那么判断这个实例的`sex`有没有被设置，有的话，就判断`$student->sex`这个值和`$ind`相不相等，相等的话，那就这个`input`默认被选中。相当于，能指定一个`input`默认被选中。

然而，如果控制器仅仅：

```php
$student = new Student();
return view('student.create', [
    'student' => $student,
]);
```

视图直接用`$student->sex`，不管用在哪里，都会报错。故此，一定要在控制器添加：`$student->sex = null;`:

```php
$student = new Student();
$student->sex = null; // 等于不赋值给$student->sex
return view('student.create', [
    'student' => $student,
]);
```

这样，在视图：

```php
\{{ isset($student->sex) && ($student->sex == $ind) ? 'checked' : '' \}}
```

先判断`$student->sex`有没有被设置再来做其他事情。

10. 视图中url传值：

```php
\{{ url('student/update', ['id' => $student->id]) \}}
```

# 三、Laravel简单操作技巧

## 1.Composer

### 1.包管理器

![2018-08-08_164522](/assets/images/laravel-develop-study/2018-08-08_164522.png)

### 2.Composer

![2018-08-08_164723](/assets/images/laravel-develop-study/2018-08-08_164723.png)

### 3.安装

![2018-08-10_224648](/assets/images/laravel-develop-study/2018-08-10_224648.png)

![2018-08-10_224728](/assets/images/laravel-develop-study/2018-08-10_224728.png)

### 4.镜像

![2018-08-10_224851](/assets/images/laravel-develop-study/2018-08-10_224851.png)

使用[Composer中国全量镜像服务](https://www.phpcomposer.com)作为本地项目的依赖管理工具的下载中心会更快。

### 5.使用Composer

```shell
# 创建配置文件以及初始化
composer init

# 搜索某个库
composer search monolog

# 查看库的信息
composer show --all monolog/monolog
```

添加库：

在配置文件`composer.json`中添加依赖和版本：

```shell
"require": {
    "monolog/monolog": "2.21.*"
}
```

	然后用`composer install`下载依赖，之后打开`vendor`目录，库将会下载在里面。

也可以用`composer require`声明依赖，它也会自动添加、下载、安装依赖：`composer require symfony/http-foundation`。

删除依赖：只需在`composer.json`删除对应的依赖，然后执行`composer update`即可。

### 6.使用Composer安装Laravel

- `composer create-project --prefer-dist laravel/laravel <别名>`
- 先安装Laravel安装器:`composer global require "laravel/installer"`, 再通过安装器安装框架：`laravel new blog`

## 2.Artisan

![1533975220842](/assets/images/laravel-develop-study//assets/images/laravel-develop-study/1533975220842.png)

![1533975343503](/assets/images/laravel-develop-study/1533975343503.png)

![1533975353745](/assets/images/laravel-develop-study/1533975353745.png)

### 1.用户认证(Auth)

#### 1. 生成Auth所需文件

	命令：

```shell
php artisan make:auth
```

	生成的路由内容：

```php
<?php
Auth::routes();

Route::get('/home', 'HomeController@index')->name('home');
```

`Auth::routes()`位置：`\vendor\laravel\framework\src\Illuminate\Routing\Router.php`的`auth`函数：

```php
    /**
     * Register the typical authentication routes for an application.
     *
     * @return void
     */
public function auth()
{
    // Authentication Routes...
    $this->get('login', 'Auth\LoginController@showLoginForm')->name('login');
    $this->post('login', 'Auth\LoginController@login');
    $this->post('logout', 'Auth\LoginController@logout')->name('logout');

    // Registration Routes...
    $this->get('register', 'Auth\RegisterController@showRegistrationForm')->name('register');
    $this->post('register', 'Auth\RegisterController@register');

    // Password Reset Routes...
    $this->get('password/reset', 'Auth\ForgotPasswordController@showLinkRequestForm')->name('password.request');
    $this->post('password/email', 'Auth\ForgotPasswordController@sendResetLinkEmail')->name('password.email');
    $this->get('password/reset/{token}', 'Auth\ResetPasswordController@showResetForm')->name('password.reset');
    $this->post('password/reset', 'Auth\ResetPasswordController@reset');
}
```

#### 2.数据迁移 --> 在数据库生成对应的表

![1534234217992](/assets/images/laravel-develop-study/1534234217992.png)

`Mysql`语句：

```mysql
CREATE TABLE IF NOT EXISTS students(
	'id' INT AUTO_INCREMENT PRIMARY KEY,
    'name' VARCHAR(255) NOT NULL DEFAULT '' COMMENT '姓名',
    'age' INT UNSIGNED NOT NULL DEFAULT 0 COMMENT '年龄',
    'sex' INT UNSIGNED NOT NULL DEFAULT 10 COMMENT '性别',
    'created_at' INT NOT NULL DEFAULT 0 COMMENT '新增时间',
    'updated_at' INT NOT NULL DEFAULT 0 COMMENT '修改时间'
)ENGINE=InnoDB DEFAULT CHARSET=UTF8
AUTO_INCREMENT=1001 COMMENT='学生表';
```

	完善迁移文件 --> **在`up`函数中添加数据表里的字段**：

```php
<?php

use Illuminate\Support\Facades\Schema;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Database\Migrations\Migration;

class CreateStudentsTable extends Migration
{
    /**
     * Run the migrations.
     *
     * @return void
     */
    public function up()
    {
        Schema::create('students', function (Blueprint $table) {
            $table->increments('id');
            $table->string('name'); // unsigned()表示非负的意思
            $table->integer('age')->unsigned()->default(0);
            $table->integer('sex')->unsigned()->default(10);
            $table->integer('created_at')->default(0);
            $table->integer('updated_at')->default(0);
            $table->timestamps();
        });
    }

    /**
     * Reverse the migrations.
     *
     * @return void
     */
    public function down()
    {
        Schema::dropIfExists('students');
    }
}
```

	将`database/migrations`下的迁移文件做迁移：

```shell
php artisan migrate
```

**迁移步骤：**

1. 新建迁移文件：`php artisan make:model Student -m`或者`php artisan make:migration create_students_table --create=students`。
2. 完善迁移文件，即在`up`函数里添加字段。
3. 做迁移：`php artisan migrate`

#### 3.数据填充 --> 一般填充测试数据

![1534235808674](/assets/images/laravel-develop-study/1534235808674.png)

1. 创建填充文件：`php artisan make:seeder StudentTableSeeder`:

![1534236147269](/assets/images/laravel-develop-study/1534236147269.png)

`DatabaseSeeder.php`：用于批量填充文件。

`StudentTableSeeder.php`：用于单个填充文件。

1. 执行填充文件

   - 单个填充文件：

     ```php
     // \database\seeds\StudentTableSeeder.php
     <?php
     
     use Illuminate\Database\Seeder;
     use Illuminate\Support\Facades\DB;
     
     class StudentTableSeeder extends Seeder
     {
         /**
          * Run the database seeds.
          *
          * @return void
          */
         public function run()
         {   
             // 导入两条数据
             DB::table('students')->insert([
                 ['name' => 'name1', 'age' => 23],
                 ['name' => 'name2', 'age' => 24],
             ]);
         }
     }
     ```

     执行：`php artisan db:seed --class=StudentTableSeeder`

   - 批量填充文件：

     ```php
     // \database\seeds\DatabaseSeeder.php
     <?php
     
     use Illuminate\Database\Seeder;
     
     class DatabaseSeeder extends Seeder
     {
         /**
          * Run the database seeds.
          *
          * @return void
          */
         public function run()
         {	// 将多个填充文件一起执行
             $this->call(StudentTableSeeder::class);
             $this->call(ArticleTableSeeder::class);
             $this->call(CommentTableSeeder::class);
         }
     }
     ```

     执行：`php artisan db:seed`

### 2.Laravel框架常用功能

#### 1.文件上传

![1534237010212](/assets/images/laravel-develop-study/1534237010212.png)

![1534237027967](/assets/images/laravel-develop-study/1534237027967.png)

配置文件：

```php
// config/filesystems.php
<?php
return [
	// 支持"local", "ftp", "s3", "rackspace"，默认使用本地端空间
    'default' => env('FILESYSTEM_DRIVER', 'local'), 

    'cloud' => env('FILESYSTEM_CLOUD', 's3'),
    
	// 磁盘
    'disks' => [
        'local' => [ // 本地端空间磁盘,名字叫local
            'driver' => 'local', // 驱动是本地端空间
            'root' => storage_path('app'), // 目录是storage/app
        ],
        'public' => [ // 本地端空间磁盘,名字叫public，因为驱动是本地端空间，所以它是本地端空间磁盘
            'driver' => 'local',
            'root' => storage_path('app/public'),
            'url' => env('APP_URL').'/storage',
            'visibility' => 'public',
        ],
        's3' => [ // 亚马逊的配置
            'driver' => 's3',
            'key' => env('AWS_KEY'),
            'secret' => env('AWS_SECRET'),
            'region' => env('AWS_REGION'),
            'bucket' => env('AWS_BUCKET'),
        ],
    ],
];
```

使用本地端空间来让laravel有文件上传的功能：

1. 在`config/filesystems.php`创建一个本地端空间磁盘，名字叫：uploads：

   ```php
   // config/filesystems.php
   <?php
   return [
       'default' => env('FILESYSTEM_DRIVER', 'local'), 
   
       'cloud' => env('FILESYSTEM_CLOUD', 's3'),
       
   	// 磁盘
       'disks' => [
           'local' => [ 
               'driver' => 'local', 
               'root' => storage_path('app'), 
           ],
           'public' => [ 
               'driver' => 'local',
               'root' => storage_path('app/public'),
               'url' => env('APP_URL').'/storage',
               'visibility' => 'public',
           ],
           'uploads' => [ // 创建了一个本地端空间磁盘，目录是storage/app/uploads
               'driver' => 'local',
               'root' => storage_path('app/uploads') // 现在这里进行配置，这个文件夹会自己生成
           ],
           's3' => [
               'driver' => 's3',
               'key' => env('AWS_KEY'),
               'secret' => env('AWS_SECRET'),
               'region' => env('AWS_REGION'),
               'bucket' => env('AWS_BUCKET'),
           ],
       ],
   ];
   ```

   位置：

   ![1534237760826](/assets/images/laravel-develop-study/1534237760826.png)

2. 控制器和路由：

   ```php
   // StudentController.php
   <?php
   
   namespace App\Http\Controllers;
   
   use App\Student;
   use Illuminate\Http\Request;
   use Illuminate\Support\Facades\Session;
   use Illuminate\Support\Facades\Storage;
   
   class StudentController extends Controller
   {
      public function upload(Request $request) {
          if ($request->isMethod('POST')) {
              // 获取上传来的文件
              $file = $request->file('source'); 
              
              if ($file->isValid()) {
                  // 判断文件是否上传成功
                  $originaName = $file->getClientOriginalName(); // 原文件名
                  $ext = $file->getClientOriginalExtension(); // 扩展名，后缀
                  $type = $file->getClientMimeType(); // 文件类型
                  $realPath = $file->getRealPath(); // 临时绝对路径，还没手动保存之前文件存放的位置
   
                  // 这种做法保证文件名称都不相同
                  $filename = date('Y-m-d-H-i-s').'-'.uniqid().'.'.$ext;
                  // 保存文件在config/filesystems.php中设置的disk里，返回一个bool，保存得成功不成功
                  $bool = Storage::disk('uploads')->put($filename, file_get_contents($realPath));
              }
          }
   
          return view("student.upload");
      }
   }
   ```

   ```php
   // web.php
   Route::get('/home', 'HomeController@index')->name('home');
   ```

3. 视图里要提交文件的表单：

   ```php
   // resources/views/student/upload.blade.php
   <div class="panel-body">
   	\{{--enctype="multipart/form-data"必须加这个属性，表单才可以使用文件上传功能--\}}
   	<form class="form-horizontal" method="POST" action="" enctype="multipart/form-data">
   		\{{ csrf_field() \}}
       	<div>
                <label for="file" class="col-md-4 control-label">请选择文件</label>
                <div class="col-md-6">		\{{--name值是source--\}}
                   <input id="file" type="file" class="form-control" name="source" required>
                </div>
            </div>
            <div class="form-group">
                <div class="col-md-8 col-md-offset-4">
                   <button type="submit" class="btn btn-primary">
                       确认上传
                   </button>
                </div>
             </div>
        </form>
   </div>
   ```

4. 可以通过更改`config/filesystems.php`里的`uploads`磁盘的空间为`public`目录底下的`uploads`目录。

![1534342816613](/assets/images/laravel-develop-study/1534342816613.png)

#### 2.发送邮件

![1534343099473](/assets/images/laravel-develop-study/1534343099473.png)

![1534343121043](/assets/images/laravel-develop-study/1534343121043.png)

	配置文件：

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

1. 在`.env`中进行配置：

```properties
MAIL_DRIVER=smtp # 使用的服务
MAIL_HOST=smtp.mailtrap.io # 服务器地址
MAIL_PORT=2525 # 服务器端口
MAIL_USERNAME=jim # 账号
MAIL_PASSWORD=passowrd
MAIL_ENCRYPTION=ssl # 协议
```

1. 控制器以及路由

```php
Route::any('mail', ['uses' => 'StudentController@mail']);
```

控制器：

- 以`raw`方式发送邮件：

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

- 以`html`方式发送邮件：

创建一个`html`文件，即视图：

```php
<!--resources/views/student/mail.blade.php-->
<!DOCTYPE html>
<html>
<head>
    <title>标题</title>
</head>
<body> <!--$name由控制器注入进来-->
<h1>Hello \{{ $name \}}</h1>
</body>
</html>
```

	控制器：

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

#### 3.缓存使用

![1534344890615](/assets/images/laravel-develop-study/1534344890615.png)

![1534344915362](/assets/images/laravel-develop-study/1534344915362.png)

![1534344930819](/assets/images/laravel-develop-study/1534344930819.png)

配置文件：

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

控制器：

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

	`add()`:添加。

```php
public function cache1() {
    // add(),如果对象已经存在,就添加失败，如果对象不存在，添加成功
    // 返回一个bool值,10是时间
    $bool = Cache::add('key1', 'val1', '10');
}
```

	`forever()`：永久的保存对象到缓存中。	

```php
public function cache1() {
    Cache::forever('key1', 'val1');
}
```

	`has()`:判断缓存中的一个`key`值存不存在。

```php
public function cache1() {
    if (Cache::has('key')) {
        $val = Cache::get('key')
    } else {
        echo "No"
    }
}
```

	`pull`:取缓存中的`key`值，然后删了这个`key`。

```php
public function cache1() {
    $val = Cache::pull('key');
}
```

	`forget()`:从缓存中删除对象，删除成功返回`true`，返回一个`bool`值。

```php
public function cache1() {
    $bool = Cache::forget('key');
}
```

#### 4.错误和日志

![1535095566213](/assets/images/laravel-develop-study/1535095566213.png)

![1535095599480](/assets/images/laravel-develop-study/1535095599480.png)

1. `debug`模式：开发模式，调试模式。

可在`.env`里开启和调试：

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

	默认是开启调试模式的，如果发生错误，`laravel`会在网页打印出错误栈。
	
	**上线了一定要关闭调试模式！！**

1. `http`异常

![1535096147008](/assets/images/laravel-develop-study/1535096147008.png)

自定义`http`异常：

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

`http`异常的视图位置：

`vendor\laravel\framework\src\Illuminate\Foundation\Exceptions\views`:

![1535098035926](/assets/images/laravel-develop-study/1535098035926.png)

1. 日志

![1535098224286](/assets/images/laravel-develop-study/1535098224286.png)

`config/app.php`：

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

	配置日志模式：

```php
# 在.env中进行配置
# APP_LoG原本的.env里是没有的，是自己添加的，只能配置"single", "daily", "syslog", "errorlog"这几种模式
APP_LoG=single 
APP_LOG_LEVEL=debug
```

	这样是会在![1535098804878](/assets/images/laravel-develop-study/1535098804878.png)这里生成日志文件:`laravel.log`。
	
	使用日志：

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

	`daily`的`log`模式，会每天生成一个日志：

![1535099439063](/assets/images/laravel-develop-study/1535099439063.png)



















[看到这里](https://www.imooc.com/video/13341)

























