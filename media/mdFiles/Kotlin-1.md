[TOC]

注：文章很多例子和文字来自：[Kotlin中文网](https://www.kotlincn.net/)

# 基本概念

### Hello World

```kotlin
fun main(){
	println("Hello world!")
}
```

从一个简单的`HelloWorld`程序中就可以大致窥得`Kotlin`这门语言的大致风格，不像Java那么复杂（Java中连一个简单的输出都需要`System.out.println()`）,但也没有Python那么的简单。`Kotlin`更像是一种`Java`、`Python`、`Scala`的混合产物（虽然我只学过`Python`，对`Java`只是有个简单的了解，而对`Scala`更是一无所知:joy:)，它是对`Java`的`Python`化，并且融入了函数式编程的内容。

**`Kotlin`学习之旅就这样开始了！**

### 包的导入

```kotlin
import kotlin.text.*
```

风格与`Java`和`Python`是一致的

### 变量

#### 声明变量的关键字

* `val`：只读
* `var`：可修改

其中`val`与其他语言中的`const`并不相同，讲到集合的时候你就会发现用`val`声明的集合其实是可以修改集合里面的值的，但是在集合上的操作还是会受到限制，讲到集合的时候再来说，**在其他情况下大多与`const`的用法等同**

这个关键字与`Javascript`很相似，就是万金油类型，两种关键字都可以声明任何其他类型

#### 变量的声明

```kotlin
val a: Int = 1  // 声明类型并立即赋值
val b = 2   // 采用自动推断类型

val c: Int  // 先声明类型
c = 3       //再赋值
```

从变量声明来看，`Kotlin`与`C`、`C++`、`Java`、`Javascript`的差别还是比较大。他有`Javascript`中的自由，却也能明确的指出到底是哪种类型。而且Kotlin采用了在变量之后声明类型的方式

### 注释

```kotlin
// 单行注释

/* 多行
   注释 */
```

`Kotlin`的注释风格是`C`语言风格的

值得一提的是`Kotlin`支持嵌套注释

```kotlin
/* 外层注释
/* 内层注释 */     
外层注释 */
```

这在`C`、`C++`、`Java`中都是会报错的（从markdown文档的代码着色来看应该支持嵌套注释的语言很少:joy:），个人觉得这个特性还是蛮不错的。

### 字符串模板

字符串模板即格式化字符串，`Kotlin`采用了一种很方便的内嵌方式

```kotlin
var a = 1
val s1 = "a is $a" //s1在a = 1的条件下为字符串`a is 1`

a = 2
val s2 = "${s1.replace("is", "was")}, but now is $a"//a was 1, but now is 2
```

它采用`$`运算符来格式化输出字符串，用`${}`的方式来格式化输出一些稍微复杂的表达式的值，这样给人一种完整的字符串的感觉，写起来也很方便，而其他语言很多都将变量和主体的字符串分离了。

### 区间

```kotlin
if(0 in 0..10){//true
    println("0")
}
if(10 in 0..10){//true
    println("10")
}
```

`Kotlin`使用`..`来建立一个正向的区间（从小到大），并且区间左右两端都是闭

```kotlin
if(1 in 10 downTo 1){//true
    println(1)
}
if(10 in 10 downTo 1){//true
    println(10)
}
```

`Kotlin`采用`downTo`来构建一个逆向的区间（从大到小），也是左右都闭

```kotlin
for(i in 1..10 step 2){
	println(i)
}
//输出一到十之内的所有奇数，step 2即采取每次走两步的遍历方式
```

要构造一个左闭右开的区间需要使用`until`

```kotlin
for(i in 1 until 10){
	print(i)
}
//输出1到9
```

### null

`null`就是空，与其他语言相同，需要注意的就是：`Kotlin`的函数在类型后面添加一个`?`号，表示该值可能为`null`

### 语句

#### 条件表达式

```kotlin
if(a > b){
	print(a)
}else{
	print(b)
}
```

#### for循环

```kotlin
val items = listOf("apple", "banana", "orange")//建立一个List集合
for(item in items){
    print(item)
}
```

有关`listOf`的内容将在集合部分讲述，目前只需要知道可以调用`listOf`函数来建立一个集合就行，集合就类似于其他语言中的数组或列表

#### while循环

```kotlin
val items = listOf("apple", "banana", "orange")//建立一个List集合
var index = 0
while(index < items.size) {//items.size是集合的大小
    println(items[index])
    index++
}
```

#### when表达式

`when`表达式相当于其他语言中的`switch`语句（`when`更加强大），两者逻辑一致，不过用法有不同

```kotlin
val str: String = "orange"
when(str){
    "apple" -> println("a")
    "orange" -> println("b")
    "banana" -> println("c")
    else -> println("d")
}
```

`when`语句里的`else`就相当于`switch`语句中的`default`。`when`语句左边除了是一些字面常量以外，还可以是一些用来判断真假的表达式，找到第一个满足条件的字面量或表达式后就执行`->`之后的语句，没找到就执行`else`后面的语句

### 返回与跳转

三类结构化跳转表达式：

*  `return`
* `break`
* `continue`

用法和其他语言类似，`return`直接返回，`break`退出最直接包围它的循环，`continue`继续下一次最直接包围它的循环。

#### 标签

```kotlin
loop@ for(i in 1..10){
    for(j in 1..10){
        if(j == 3) break@loop
        print("($i, $j)")
    }
}
println()
for(i in 1..10){
    for(j in 1..10){
        if(j == 2) break
        print("($i, $j)")
    }
}
```

输出

```kotlin
(1, 1)(1, 2)
(1, 1)(2, 1)(3, 1)(4, 1)(5, 1)(6, 1)(7, 1)(8, 1)(9, 1)(10, 1)
```

标签限制的 break 跳转到刚好位于该标签指定的循环后面的执行点。 *continue* 继续标签指定的循环的下一次迭代。

```kotlin
listOf(1, 2, 3, 4, 5).forEach {
    if (it == 3) return // 非局部直接返回到 foo() 的调用者
    print(it)
}
println("this point is unreachable")
```
输出

```
12
```

```kotlin
listOf(1, 2, 3, 4, 5).forEach lit@{
    if (it == 3) return@lit // 局部返回到该 lambda 表达式的调用者，即 forEach 循环
    print(it)
}
print(" done with explicit label")
```
输出

```kotlin
1245 done with explicit label
```

通过以上例子，我们可以看到有标签和无标签的区别

当要返一个回值的时候，解析器优先选用标签限制的 return，即

```
return@a 1
```

意为“返回 `1` 到 `@a`”，而不是“返回一个标签标注的表达式 `(@a 1)`”。

**第一部分结束了，下一部分讲`Kotlin`的基础类型**

