---
layout: post
category: [Larave学习笔记]
tag: [Larave, 学习笔记]
title: Larave学习笔记2
---
{% raw %}  

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
{{--@section,展示片段内容--}}
@section('header')
    头部
@show

@section('sidebar')
    侧边栏
@show

{{--@yield，展示字符串内容--}}
@yield('content', '主要内容')
```

子模板(views.student.child):

```php
// resources/views/student/child.blade.php
{{--1.继承哪个模板--}}
@extends('layouts')

{{--2.替换父模板中@section的header内容，输出父模板对应地方的父内容--}}
@section('header')
    @parent
    header
@stop
{{--或者--}}
{{--重写父模板中@section的sidebar内容，不会输出父模板对应地方的父内容--}}
@section('sidebar')
    sidebar
@stop

{{--3.替换父模板中@yield的content内容--}}
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
{{--resources/views/student/child.blade.php--}}
{{--1.模板中输出PHP变量，该变量由控制器传入--}}
{{ $name }}

{{--2.模板中调用PHP代码,$name和$arr两个变量都由控制器中传进来--}}
{{ time() }}
{{ date('Y-m-d H:i:s', time()) }}
{{--判断$arr数组中是否有$name,有返回true，没有返回false--}}
{{ in_array($name, $arr) ? 'ture': 'false' }}
{{--判断$name是否存在,有返回$name值，没有返回字符串'default'--}}
{{ isset($name) ? $name: 'default' }}
{{--或者--}}
{{ $name or 'default' }}

{{--3.原样输出，视图渲染时输出{{ $name }}--}}
@{{ $name }}

{{--4.模板注释--}}
{{--xxxx--}}

{{--5.子模板中引入子视图--}}
@include('student.common')
{{--子视图中有占位符$msg,在这里将msg赋值并传给子视图--}}
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
{{--resources/views/student/common.blade.php--}}
{{--$msg是个占位符，等着别处传过来值给它赋值--}}
{{ $msg }}
```

### 3.模板中流程控制

```php
{{--resources/vies/student/child.blade.php--}}

{{--if--}}
@if ($name == 'Jim')
    Jim
@elseif($name == 'a')
    a
@else
    b
@endif

{{--unless,相当于if的取反--}}
@unless( $name == 'Jim' )
    output Jim
@endunless

{{--for--}}
@for ($i=0; $i<2; $i++)
    <p>{{ $i }}</p>
@endfor

{{--foreach,遍历对象列表或者数组--}}
@foreach($students as $student) {{--该$student对象列表由控制器传入--}}
    <p>{{ $student->name }}</p> {{--返回$student对象的name属性--}}
@endforeach

{{--forelse--}}
@forelse($students as $student)
    <p>{{ $student->name }}</p>
@empty{{--如果对象列表为空--}}
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
{{--resources/views/student/child.blade.php--}}
{{--1.指定的路由名字--}}
<a href="{{ url('urlTest') }}">This is url.</a>
{{--2.控制器+方法名--}}
<a href="{{ action('StudentController@urlTest') }}">This is url.</a>
{{--3.路由的别名--}}
<a href="{{ route('urlAlias') }}">This is url.</a>
```

{% endraw %}  