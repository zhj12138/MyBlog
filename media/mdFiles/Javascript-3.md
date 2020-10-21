# 函数表达式

1. 函数声明语法

   ```js
   function functionName(arg0, arg1,...){
   	//content
   }
   ```

   ```js
   	function functionName(arg1) {
           alert(arg1);
       }
       alert(functionName.name);//functionName
   ```

2. 函数声明提升：执行代码之前会先读取函数声明

3. 函数表达式：

   ```js
   let functionName = function(arg0, arg1, ...){
   	//content
   };
   //这种情况创建的函数叫匿名函数，因为function关键字后面没有标识符
   ```
   
4. 区别：
   
```js
if(condition){
    function sayHi(){
        alert("yes!");
    }
} else {
    function sayHi(){
        alert("no!");
    }
}
```

 ==这是不可行的，这在ECMAScript中属于无效语法。==（个人觉得是因为会进行函数声明提升然后引发了一系列问题），在这里可以通过使用函数表达式来避免这个问题

5. 递归

   解决在严格模式下不能使用arguments.callee的问题：

   ```js
   //通过命名函数表示式来达成相同的效果
   let factorial = (function f(num){
   	if (num <= 1){
   		return 1;
   	} else {
   		return num * f(num-1);
   	}
   });
   ```

6. 闭包：有权访问另一个函数作用域中的变量的函数

   创建闭包的常见方式：**在一个函数内部创建另一个函数：**

   ```js
   	function createComparisonFunction(propertyName) {
           return function (object1, object2) {
               let value1 = object1[propertyName];
               let value2 = object2[propertyName];
               
               if(value1 <value2){
                   return -1;
               }else if(value1>value2){
                   return 1;
               }else{
                   return 0;
               }
           };
       }
   ```

   后台的每个执行环境都有一个表示变量的对象——变量对象。全局环境的变量对象始终存在，而像函数这样的局部环境的变量对象只在函数执行的过程中存在。

   作用域链本质是指向变量对象的指针列表，它只引用但不实际包含变量对象

   ```js
   //创建函数
   var compareNames = createComparisonFunction("name");
   //调用函数
   var result = compareNames({ name: "Nicholas" }, { name: "Greg" });
   //解除对匿名函数的引用（以便释放内存）
   compareNames = null;
   ```

   闭包的缺点：比其他函数占用更多的内存

7. 闭包与变量：

   ```js
   function createFunctions(){
   	var result = new Array();
   	for (var i=0; i < 10; i++){
   		result[i] = function(){
   			return i;
   		};
   	}
   	return result;
   }
   //每个函数都返回10
   //解决方案：
   function createFunctions(){
   	var result = new Array();
   	for (var i=0; i < 10; i++){
   		result[i] = function(num){
   			return function(){
   				return num;
   			};
   		}(i);
   	}
   	return result;
   }
   ```

8. this对象：在全局函数中，this等于window，由于匿名函数的执行环境具有全局性，因此其this对象通常指向window（可通过call方法和apply方法改变）

   ```js
   	var name = "THe Window";
       var object = {
           name: "Object",
           getNameFunc: function () {
               return function () {
                   return this.name;
               };
           }
       };
       alert(object.getNameFunc()());//THe Window
   
   	//解决方式
   	var name = "THe Window";
       var object = {
           name: "Object",
           getNameFunc: function () {
               let that = this;
               return function () {
                   return that.name;
               };
           }
       };
       alert(object.getNameFunc()());//Object
   ```

   ```js
   	var name = 'The Window';
       let object = {
           name: "My Object",
           getName: function () {
               return this.name;
           }
       }
       alert(object.getName());//My Object
       alert((object.getName)());//My Object
       alert((object.getName = object.getName)());//The Window
   ```

   第三种调用先执行了一条赋值语句，然后再调用赋值后的结果。因为这个赋值表达式的值是函数本身，所以this 的值不能得到维持，结果就返回了"The Window"。

   javascript中没有块级作用域的概念

   用作块级作用域（私有作用域）的匿名函数的语法：

   ```js
   (function(){
   	//块级作用域
   })();
   ```

   将函数表达式包含在圆括号中，表示它实际上是一个函数表达式

   无论在什么地方，只临时需要一些变量，就可以使用私有作用域：

   ```js
   	function outNum(num) {
           (function (num) {
               for(var i = 0; i < 10; i++){
                   alert(i);
               }
           })();
           alert(i);//将报错,将var改成let已经解决这个问题
       }
   ```

9. 严格说，JavaScript没有私有成员的概念，所有对象属性都是公有的

10. 私有变量

    任何在函数中定义的变量都可以认为是私有变量

    有权访问私有变量和私有函数的共有方法称为特权方法

    1. 静态私有变量：

       ```js
       (function(){
       	//私有变量和私有函数
       	var privateVariable = 10;
       	function privateFunction(){
       		return false;
       	}
           
       	//构造函数
       	MyObject = function(){
       	};
           //Attention:MyObject前面没有使用var
           
       	//公有/特权方法
       	MyObject.prototype.publicMethod = function(){ 
               privateVariable++;
               return privateFunction();
           };
       })();
       ```
       

==初始化未经声明的变量总是会创建一个全局变量==，因此MyObject成了全局变量，能够在私有作用域之外访问到。但在严格模式下，给未经声明的变量赋值会导致错误

```js
(function () {
    let name = '';
    Person = function (value) {
        name = value;
    };
    Person.prototype.getName = function () {
        return name;
    };
    Person.prototype.setName = function (a) {
        name = a;
    };
})();
let person1 = new Person("Nicholas");
alert(person1.getName());//Nicholas
person1.setName("Greg");
alert(person1.getName());//Greg

let person2 = new Person("Mia");
alert(person1.getName());//Mia
alert(person2.getName());//Mia
//在一个实例上调用setName()会影响所有实例，因为name始终只有一个
```

   2. 模块模式：

      ```js
      var application = function () {
          //私有变量和函数
          var components = new Array();
          //初始化
          components.push(new BaseComponent());
          //公共
          return {
              getComponentCount: function () {
                  return components.length;
              },
              registerComponent: function (component) {
                  if (typeof component == "object") {
                      components.push(component);
                  }
              }
          };
      }();
      ```
      
   3. 增强的模块模式：
      
 ```js
       var singleton = function(){
       	//私有变量和私有函数
       	var privateVariable = 10;
       	function privateFunction(){
       		return false;
       	}
       	//创建对象
       	var object = new CustomType();
       	//添加特权/公有属性和方法
       	object.publicProperty = true;
       	object.publicMethod = function(){
       		privateVariable++;
       		return privateFunction();
       	};
       	//返回这个对象
       	return object;
       }();
 ```


​       

# BOM

1. BOM：浏览器对象模型

2. BOM的核心对象是window,它表示浏览器的一个实例。在网页中定义的任何一个对象，变量和函数，都以window作位其Global对象

3. 全局作用域：

   ```js
   var age = 29;
   function sayAge() {
       alert(this.age);
   }
   alert(window.age);//29
   sayAge();//29
   window.sayAge();//29
   ```

4. ==var和let的区别：==

   以下内容来源于[百度知道](https://zhidao.baidu.com/question/329685205173520085.html)

   1. 作用域不一样，var是函数作用域，而let是块作用域，也就是说，在函数内声明了var，整个函数内都是有效的，比如说在for循环内定义了一个var变量，实际上其在for循环以外也是可以访问的，而let由于是块作用域，所以如果在块作用域内（比如说for循环内）定义的变量，在其外面是不可被访问的。

   2. let不能在定义之前访问该变量，但是var可以。也就是说，let必须是先定义，再使用，而var先使用后声明也行，只不过直接使用但是没有却没有定义的时候，其值为undefined。

   3. let不能被重新定义，但是var可以。

5. 定义全局变量与在window对象上直接定义属性还是有一定差别：全局变量不能通过delete操作符删除，在直接在window对象上定义的属性可以

6. ```js
   //这里会抛出错误，因为oldValue 未定义
   var newValue = oldValue;
   
   //这里不会抛出错误，因为这是一次属性查询
   //newValue 的值是undefined
   var newValue = window.oldValue;
   ```

7. 如果页面包含框架，则每个框架都拥有自己的window对象，并保存在frames集合中。每个window对象都有一个name属性，其中包含框架的名称

   ```html
   <!DOCTYPE html>
   <html lang="en">
   <head>
       <meta charset="UTF-8">
       <title>Frameset Example</title>
   </head>
   <frameset rows="160,*">
       <frame src="frame.html" name="topFrame">
       <frameset cols="50%, 50%">
           <frame src="anotherframe.html" name="leftFrame">
           <frame src="yetanotherframe.html" name="rightFrame">
       </frameset>
   </frameset>
   </html>
   ```

   可以使用window.frames[0]或window.frames['topFrame']来引用上方的框架

   也可使用top对象引用这些框架，top对象始终指向最高层二点框架，也就是浏览器窗口

   parent对象始终指向当前框架的直接上层框架。在没有框架的情况下，parent一定等于top（此时它们都等于window）

   self对象始终指向windows

8. 窗口位置：

   ```js
   //取得窗口左边和上边的位置
   let leftPos = (typeof window.screenLeft == 'number')? window.screenLeft : window.screenX;
   let topPos = (typeof window.screenTop == 'number')? window.screenTop : window.screenY;
   ```

   移动窗口位置：

   ```js
   //将窗口移动到屏幕左上角
   window.moveTo(0,0);
   //将窗向下移动100 像素
   window.moveBy(0,100);
   //将窗口移动到(200,300)
   window.moveTo(200,300);
   //将窗口向左移动50 像素
   window.moveBy(-50,0);
   ```

   跨浏览器确定一个窗口的大小不是一件简单的事。IE9+、Firefox、Safari、Opera 和Chrome 均为此提供了4 个属性：innerWidth、innerHeight、outerWidth 和outerHeight。在IE9+、Safari 和Firefox中,outerWidth 和outerHeight 返回浏览器窗口本身的尺寸（无论是从最外层的window 对象还是从某个框架访问）。在Opera 中，这两个属性的值表示页面视图容器①的大小。而innerWidth 和innerHeight则表示该容器中页面视图区的大小（减去边框宽度）。在Chrome 中，outerWidth、outerHeight 与innerWidth、innerHeight 返回相同的值，即视口（viewport）大小而非浏览器窗口大小。
   
9. ```js
   //可通过下面两种属性获取页面视口的信息
   let width = document.documentElement.clientWidth;
   let hight = document.documentElement.clientHeight;
   ```

   ```js
   //跨浏览器获取页面视口的大小
   var pageWidth = window.innerWidth,
   pageHeight = window.innerHeight;
   if (typeof pageWidth != "number"){
   	if (document.compatMode == "CSS1Compat"){
   		pageWidth = document.documentElement.clientWidth;
   		pageHeight = document.documentElement.clientHeight;
   	} else {
   		pageWidth = document.body.clientWidth;
   		pageHeight = document.body.clientHeight;
   	}
   }
   ```

   ```js
   //调整浏览器窗口的大小
   //resizeTo接受浏览器的新宽度和新高度
   //resizeBy()接受新窗口和原窗口的宽度和高度之差
   //调整到100×100
   window.resizeTo(100, 100);
   //调整到200×150
   window.resizeBy(100, 50);
   //调整到 300×300
   window.resizeTo(300, 300);
   ```

10. 导航和打开窗口

    window.open()方法：导航到一个特定的URL,也可以打开一个新的浏览器窗口，四个参数：

    * 要加载的URL
    * 窗口目标
    * 一个特性字符串
    * 一个表示新页面是否取代浏览器历史记录中当前加载页面的布尔值

    ```js
    //等同于< a href="http://www.wrox.com" target="topFrame"></a>
    window.open("http://www.wrox.com/", "topFrame");
    ```

    1. 弹出窗口：

       如果给window.open()传递的第二个参数并不是一个已经存在的窗口或框架，那么该方法将根据第三个参数位置上传入的字符串创建一个新窗口或新标签页。在不带开新窗口的情况下，会忽略第三个参数，

       第三个参数是一个逗号分隔的设置字符串，表示在新窗口显示哪些特性

       ![image-20200709150857189](https://gitee.com/snow_zhao/img/raw/master/img/image-20200709150857189.png)

       ```js
       window.open('http://www.wrox.com/', 'wroxWindow',"height=400, width=400, top=10, left=10, resizable=yes");
       //打开一个新的可调节大小的窗口，初始为400*400像素，距离屏幕上边和左边各10像素
       ```

       window.open()方法将返回一个指向新窗口的引用

       ```js
       var wroxWin = window.open("http://www.wrox.com/","wroxWindow","height=400,width=400,top=10,left=10,resizable=yes");
       //调整大小
       wroxWin.resizeTo(500,500);
       //移动位置
       wroxWin.moveTo(100,100);
       //关闭窗口
       wroxWin.close();//该方法仅适用于通过window.open()打开的弹出窗口
       //新创建的window对象有一个opener属性，保存着打开它的原始窗口对象，这个属性只在弹出窗口的最外层window对象(top)中有定义，指向调用window.open()的窗口或框架
       ```

       检测弹出窗口是否被屏蔽：

       ```js
       	let blocked = false;
           try{
               let wrox = window.open("http://www.wrox.com", "_bland");
               if(wrox == null){
                   blocked = true;
               }
           }catch (ex) {
               blocked = true;
           }
           if(blocked){
               alert("The popup was blocked!");
           }
       ```

    2. 间歇调用和超时调用：

       超时调用：window对象的setTimeout()方法:

       ```js
       //不建议使用
       setTimeout("alert('hello world!')", 5000);
       
       //建议使用
       setTimeout(function () {
           alert("hello world!");
       } ,5000);
       ```

       取消超时调用：

       ```js
       let timeoutId = setTimeout(function () {
           alert("hello world!");
       } ,5000);
       clearTimeout(timeoutId);
       ```

       间歇调用：按指定的时间间隔重复执行代码，直到间歇调用被取消或页面被卸载。

       ```js
       //不建议传递字符串！
       setInterval ("alert('Hello world!') ", 10000);
       
       //推荐的调用方式
       setInterval (function() {
       	alert("Hello world!");
       }, 10000);
       ```

       ```js
       	let count = 0;
           let max = 10;
           let intervalID = null;
           
           function incrementNumber() {
               count++;
               if(count >= max){
                   clearInterval(intervalID);
                   alert("Done!");
               }
           }
           
           setInterval(incrementNumber, 500);
       ```

       用超时调用来代替间歇调用：

       ```js
       var num = 0;
       var max = 10;
       function incrementNumber() {
       	num++;
       	//如果执行次数未达到max 设定的值，则设置另一次超时调用
       	if (num < max) {
       		setTimeout(incrementNumber, 500);
       	} else {
       		alert("Done");
       	}
       }
       setTimeout(incrementNumber, 500);
       ```

    3. 窗口：

       confirm()方法

       ```js
       confirm("are you ok?");
       //需要手动确定
       ```

       prompt()方法

       ```js
       let result = prompt("What's your name?", "Mike");
       if(result != null){
           alert("Hello" + result);
       }
       ```

       ```js
       window.print();//打印
       ```

11. Location对象：

    它既是window对象的属性，也是document对象的属性

    location对象的所有属性：

    ![image-20200709165434129](https://gitee.com/snow_zhao/img/raw/master/img/image-20200709165434129.png)

    查询字符串参数：

    ```js
     	function getQueryStringArgs(){
            let qs = (location.search.length > 0 ? location.search.substring(1) : ''),
            args = {},
            items = qs.length ? qs.split("&") : [],
            item = null,
                name = null,
                value = null,
    
                i = 0,
                len = items.length;
            for(i = 0; i < len; i++){
                item = items[i].split("=");
                name = decodeURIComponent(item[0]);
                value = decodeURIComponent(item[1]);
                
                if(name.length) {
                    args[name] = value;
                }
            }
            return args;
        }
    ```

    位置操作：

    `location.assign("http://www.wrox.com");`

    `window.location = "http://www.wrox.com";`

    `location.href = "http://www.wrox.com";`

    通过修改其他属性来改变URL:

    ```js
    //假设初始URL 为http://www.wrox.com/WileyCDA/
    
    //将URL修改为"http://www.wrox.com/WileyCDA/#section1"
    location.hash = "#section1";
    
    //将URL 修改为"http://www.wrox.com/WileyCDA/?q=javascript"
    location.search = "?q=javascript";
    
    //将URL 修改为"http://www.yahoo.com/WileyCDA/"
    location.hostname = "www.yahoo.com";
    
    //将URL 修改为"http://www.yahoo.com/mydir/"
    location.pathname = "mydir";
    
    //将URL 修改为"http://www.yahoo.com:8080/WileyCDA/"
    location.port = 8080;
    ```

    禁用后退按钮：

    ```html
    <!DOCTYPE html>
    <html>
    <head>
    	<title>You won't be able to get back here</title>
    </head>
    <body>
    	<p>Enjoy this page for a second, because you won't be coming back here.</p>
    	<script type="text/javascript">
    		setTimeout(function () {
    			location.replace("http://www.wrox.com/");
    		}, 1000);
    	</script>
    </body>
    </html>
    ```

    重新加载：

    ```js
    location.reload(); //重新加载（有可能从缓存中加载）
    location.reload(true); //重新加载（从服务器重新加载）
    ```

12. navigator对象

    属性和方法：

    ![image-20200709210735531](https://gitee.com/snow_zhao/img/raw/master/img/image-20200709210735531.png)

![image-20200709210754530](https://gitee.com/snow_zhao/img/raw/master/img/image-20200709210754530.png)

1. 检测插件：plugins数组

	该数组的每一项包含以下属性：
	* name:插件名
	* description:插件描述
	* filename:插件的文件名
	* length:插件所处理的MIME类型数量

```js
	function hasPlugin(name) {
        name = name.toLowerCase();
        for(let i = 0; i < navigator.plugins.length; i++ ){
            if(navigator.plugins[i].name.toLowerCase().indexOf(name) > -1){
                return true;
            }
        }
        return false;
    }
    alert(hasPlugin("flash"));
    alert(hasPlugin("infinity"));
```

每个插件本身也是一个MimeType对象的数组，这些对象拥有4个属性：包含MIME 类型描述的description、回指插件对象的enabledPlugin、表示与MIME 类型对应的文件扩展名的字符串suffixes（以逗号分隔）和表示完整MIME 类型字符串的type。

检测IE中的插件：

```js
//检测IE 中的插件
function hasIEPlugin(name){
	try {
		new ActiveXObject(name);
		return true;
	} catch (ex){
		return false;
	}
}
//检测Flash
alert(hasIEPlugin("ShockwaveFlash.ShockwaveFlash"));
//检测QuickTime
alert(hasIEPlugin("QuickTime.QuickTime"));
```

13. screen对象

    ![image-20200709212528197](https://gitee.com/snow_zhao/img/raw/master/img/image-20200709212528197.png)

    ![image-20200709212556162](https://gitee.com/snow_zhao/img/raw/master/img/image-20200709212556162.png)

14. history对象：

    ```js
    history.go(-1);//后退一页
    history.go(1);//前进一页
    history.go(2);//前进两页
    ```

    ```js
    history.go("wrox.com");//跳转到最近的wrox.com页面
    history.go("nczonline.net");
    ```

    ```js
    history.back();//后退一页
    history.forward();//前进一页
    ```

    `history.length`保存着历史记录的数量







[百度知道]: https://zhidao.baidu.com/question/329685205173520085.html
