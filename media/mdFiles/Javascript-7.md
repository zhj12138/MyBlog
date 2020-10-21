# 使用Canvas绘图

### 基本用法

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>canvas</title>
</head>
<body>
<canvas id="drawing" width="200" height="200">A drawing of something.</canvas>

</body>
</html>
<script type="text/javascript">
    let drawing = document.getElementById("drawing");
    if(drawing.getContext){//检查浏览器是否支持<canvas>元素
        //取得图像的数据URL
        let imgURL = drawing.toDataURL("image/png");

        //显示图像
        let image = document.createElement("img");
        image.src = imgURL;
        document.body.appendChild(image);
    }
</script>
```

### 2D上下文

#### 填充和描边

属性：`fillStyle`和`strokeStyle`。两个属性的值可以是字符串、渐变对象或模式对象，默认值为`#000000`

```js
var drawing = document.getElementById("drawing");
if(drawing.getContext){
    let context = drawing.getContext("2d");
    context.strokeStyle = "red";
    context.fillStyle = "#0000ff";
}
```

#### 绘制矩形

与矩形有关的方法包括fillRect()、strokeRect()和clearRect()。这三个方法都能接收4 个参数：矩形的x 坐标、矩形的y 坐标、矩形宽度和矩形高度。这些参数的单位都是像素。

```js
    var drawing = document.getElementById("drawing");
    let context = drawing.getContext("2d");

	//绘制红色矩形
    context.fillStyle = "#ff0000";
    context.fillRect(10, 10, 50, 50);

	//绘制半透明的蓝色矩形
    context.fillStyle = "rgba(0, 0, 255, 0.5)";
    context.fillRect(30, 30, 50, 50);
```

```js
    //绘制红色描边矩形
    context.strokeStyle = "#ff0000";
    context.strokeRect(10, 10, 50, 50);
    //绘制半透明的蓝色描边矩形
    context.strokeStyle = "rgba(0,0,255,0.5)";
    context.strokeRect(30, 30, 50, 50);
```

```js
	//clearRect()方法用于清除画布上的矩形区域
	context.clearRect(40, 40, 10, 10);
```

#### 绘制路径

要绘制路径，首先需要调用beginPath()方法，然后再调用以下方法来绘制路径：

* arc(x, y, radius, startAngle, endAngle, counterclockwise)：以(x,y)为圆心绘制一条弧线，弧线半径为radius，起始和结束角度（用弧度表示）分别为startAngle 和endAngle。最后一个参数表示startAngle 和endAngle 是否按逆时针方向计算，值为false表示按顺时针方向计算。
* arcTo(x1, y1, x2, y2, radius)：从上一点开始绘制一条弧线，到(x2,y2)为止，并且以给定的半径radius 穿过(x1,y1)。
* bezierCurveTo(c1x, c1y, c2x, c2y, x, y)：从上一点开始绘制一条曲线，到(x,y)为止，并且以(c1x,c1y)和(c2x,c2y)为控制点。
* lineTo(x, y)：从上一点开始绘制一条直线，到(x,y)为止。
* moveTo(x, y)：将绘图游标移动到(x,y)，不画线。
* quadraticCurveTo(cx, cy, x, y)：从上一点开始绘制一条二次曲线，到(x,y)为止，并且以(cx,cy)作为控制点。
* rect(x, y, width, height)：从点(x,y)开始绘制一个矩形，宽度和高度分别由width 和height 指定。这个方法绘制的是矩形路径，而不是strokeRect()和fillRect()所绘制的独立的形状。

创建了路径后，接下来有几种可能的选择。如果想绘制一条连接到路径起点的线条，可以调用closePath()。如果路径已经完成，你想用fillStyle 填充它，可以调用fill()方法。另外，还可以调用stroke()方法对路径描边，描边使用的是strokeStyle。最后还可以调用clip()，这个方法可以在路径上创建一个剪切区域。

```html
<!--绘制一个不带数字的时钟表盘-->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>canvas</title>
</head>
<body>
<canvas id="clock" height="200" width="200"></canvas>
</body>
</html>
<script type="text/javascript">
    var clock = document.getElementById("clock");
    let context = clock.getContext("2d");
    context.beginPath();//开始
    context.arc(100, 100, 99, 0, 2 * Math.PI, false);//外圆

    context.moveTo(194, 100);
    context.arc(100, 100, 94, 0, 2 * Math.PI, false);//内圆

    context.moveTo(100, 100);
    context.lineTo(100, 15);//分针

    context.moveTo(100, 100);
    context.lineTo(35, 100);//时针

    context.stroke();//描边
</script>
```

#### 绘制文本

两个方法：fillText()和strokeText()。接收4个参数：要绘制的文本字符串、x 坐标、y 坐标和可选的最大像素宽度。三个属性：

* font：表示文本样式、大小及字体，用CSS 中指定字体的格式来指定，例如"10px Arial"。
* textAlign：表示文本对齐方式。可能的值有"start"、"end"、"left"、"right"和"center"。建议使用"start"和"end"，不要使用"left"和"right"，因为前两者的意思更稳妥，能同时适合从左到右和从右到左显示（阅读）的语言。
* textBaseline：表示文本的基线。可能的值有"top"、"hanging"、"middle"、"alphabetic"、"ideographic"和"bottom"。

```js
    //在表盘的上方绘制了数字12
	context.font = "bold 10px Arial";
    context.textAlign = "center";
    context.textBaseline = "middle";
    context.fillText("12", 100, 12);
```

```js
    //起点对齐
    context.textAlign = "start";
    context.fillText("12", 100, 40);
    //终点对齐
    context.textAlign = "end";
    context.fillText("12", 100, 60);
```

确定文本大小的方法：measureText()，接收一个参数，即要绘制的文本，返回一个TextMetrics对象。

```js
    let cfont = document.getElementById("font");
    let context = cfont.getContext("2d");
    let fontSize = 100;
    context.font = fontSize + "px Arial";
    while(context.measureText("Hello world").width > 140){
        fontSize--;
        context.font = fontSize + "px Arial";
    }
    context.fillText("Hello  world", 10, 10);
    context.fillText("Font size is" + fontSize + "px", 10, 50);
```

#### 变换

修改变化矩阵的方法：

* rotate(angle)：围绕原点旋转图像angle 弧度。

* scale(scaleX, scaleY)：缩放图像，在x 方向乘以scaleX，在y 方向乘以scaleY。scaleX和scaleY 的默认值都是1.0。

* translate(x, y)：将坐标原点移动到(x,y)。执行这个变换之后，坐标(0,0)会变成之前由(x,y)表示的点。

* transform(m1_1, m1_2, m2_1, m2_2, dx, dy)：直接修改变换矩阵，方式是乘以如下
  矩阵。

  `m1_1 m1_2 dx`
  `m2_1 m2_2 dy`
    `0   0   1`

* setTransform(m1_1, m1_2, m2_1, m2_2, dx, dy)：将变换矩阵重置为默认状态，然后
再调用transform()。

```js
    context.translate(100, 100);//将原点移动到100，100

    context.moveTo(0, 0);
    context.lineTo(0, -85);

    context.moveTo(0, 0);
    context.lineTo(-65, 0);
```

```js
	context.rotate(1);//向右旋转一定角度
```

有两个方法可以跟踪上下文的状态变化。如果将来要返回某组属性与变换的组合，可以调用save()方法。调用这个方法后，当时的所有设置都会进入一个栈结构，可以调用restore()方法回到之前保存的设置。

```js
    var can = document.getElementById("save");
    let context = can.getContext("2d");
    context.fillStyle = "#ff0000";
    context.save();

    context.fillStyle = "#00ff00";
    context.translate(100, 100);
    context.save();

    context.fillStyle = "#0000ff";
    context.fillRect(0, 0, 100, 200);//蓝色

    context.restore();
    context.fillRect(10, 10, 100, 200);//绿色
    
    context.restore();
    context.fillRect(0, 0, 100, 200);//红色
```

#### 绘制图像

```js
let image = document.images[0];
let canv = document.getElementById("image");
let context = canv.getContext("2d");
context.drawImage(image, 10, 10);//起点（10，10）
```

```js
context.drawImage(image, 50, 10, 20, 30);//变成20*30像素
```

```js
context.drawImage(image, 0, 10, 50, 50, 0, 100, 40, 60);//9个参数：要绘制的图像、源图像的x 坐标、源图像的y 坐标、源图像的宽度、源图像的高度、目标图像的x 坐标、目标图像的y 坐标、目标图像的宽度、目标图像的高度。
```

#### 阴影

属性值：

* shadowColor：用CSS 颜色格式表示的阴影颜色，默认为黑色。
* shadowOffsetX：形状或路径x 轴方向的阴影偏移量，默认为0。
* shadowOffsetY：形状或路径y 轴方向的阴影偏移量，默认为0。
* shadowBlur：模糊的像素数，默认0，即不模糊。

```js
//设置阴影
context.shadowOffsetX = 5;
context.shadowOffsetY = 5;
context.shadowBlur = 4;
context.shadowColor = "rgba(0, 0, 0, 0.5)";
```

#### 渐变

由CanvasGradient实例表示。通过createLinearGradient()方法，接收4个参数：起点的x坐标、起点的y坐标、终点的x坐标、终点的y坐标。

使用addColorStop()方法来指定色标。接收两个参数：色标位置和CSS颜色值。

```js
var gradient = context.createLinearGradient(30, 30, 70, 70);
gradient.addColorStop(0, "white");
gradient.addColorStop(1, "black");

var gra = document.getElementById("gradient");
let context = gra.getContext("2d");
let gradient = context.createLinearGradient(30, 30, 70, 70);
gradient.addColorStop(0, "white");
gradient.addColorStop(1, "black");

//绘制红色矩形
context.fillStyle = "#ff0000";
context.fillRect(10, 10, 50, 50);

//绘制渐变矩形
context.fillStyle = gradient;
context.fillRect(30, 30, 50, 50);
```

要创建径向渐变或放射渐变，可以使用createRadialGradient()方法。接收6 个参数，对应着两个圆的圆心和半径。前三个参数指定的是起点圆的原心（x 和y）及半径，后三个参数指定的是终点圆的原心（x 和y）及半径。

```js
var gradient = context.createRadialGradient(55, 55, 10, 55, 55, 30);
```

#### 模式

模式就是重复的图像，用来填充或描边图形。通过调用createPattern()方法，两个参数：一个HTML `<img>`元素和一个表示如何重复图像的字符串。第二个字符串：`repeat`、`repeat-x`、`repeat-y`和`no-repeat`

```js
    let image = document.images[0];
    let pattern = context.createPattern(image, "repeat");
    context.fillStyle = pattern;
    context.fillRect(10, 10, 150, 150);
	//<img>可以改为<video>或另一个<canvas>元素
```

#### 使用图像数据

```js
var imageData = context.getImageData(10, 5, 50, 50);
```

返回的对象是ImageData 的实例。每个ImageData 对象都有三个属性：width、height 和data。data 属性是一个数组，保存着图像中每一个像素的数据。在data 数组中，每一个像素用4 个元素来保存，分别表示红、绿、蓝和透明度值

```js
var drawing = document.getElementById("drawing");
//确定浏览器支持<canvas>元素
if (drawing.getContext){
    var context = drawing.getContext("2d"),
        image = document.images[0],
        imageData, data,
        i, len, average,
        red, green, blue, alpha;
    //绘制原始图像
    context.drawImage(image, 0, 0);
    //取得图像数据
    imageData = context.getImageData(0, 0, image.width, image.height);
    data = imageData.data;
    for (i=0, len=data.length; i < len; i+=4){
        red = data[i];
        green = data[i+1];
        blue = data[i+2];
        alpha = data[i+3];
        //求得rgb 平均值
        average = Math.floor((red + green + blue) / 3);
        //设置颜色值，透明度不变
        data[i] = average;
        data[i+1] = average;
        data[i+2] = average;
    }
    //回写图像数据并显示结果
    imageData.data = data;
    context.putImageData(imageData, 0, 0);
}
```

#### 合成

两个属性：globalAlpha 和globalComposition-Operation

```js
//绘制红色矩形
context.fillStyle = "#ff0000";
context.fillRect(10, 10, 50, 50);
//修改全局透明度
context.globalAlpha = 0.5;
//绘制蓝色矩形
context.fillStyle = "rgba(0,0,255,1)";
context.fillRect(30, 30, 50, 50);
//重置全局透明度
context.globalAlpha = 0;
```

第二个属性的可能值：

* source-over（默认值）：后绘制的图形位于先绘制的图形上方。
* source-in：后绘制的图形与先绘制的图形重叠的部分可见，两者其他部分完全透明。
* source-out：后绘制的图形与先绘制的图形不重叠的部分可见，先绘制的图形完全透明。
* source-atop：后绘制的图形与先绘制的图形重叠的部分可见，先绘制图形不受影响。
* destination-over：后绘制的图形位于先绘制的图形下方，只有之前透明像素下的部分才可见。
* destination-in：后绘制的图形位于先绘制的图形下方，两者不重叠的部分完全透明。
* destination-out：后绘制的图形擦除与先绘制的图形重叠的部分。
* destination-atop：后绘制的图形位于先绘制的图形下方，在两者不重叠的地方，先绘制的图形会变透明。
* lighter：后绘制的图形与先绘制的图形重叠部分的值相加，使该部分变亮。
* copy：后绘制的图形完全替代与之重叠的先绘制图形。
* xor：后绘制的图形与先绘制的图形重叠的部分执行“异或”操作。

```js
//绘制红色矩形
context.fillStyle = "#ff0000";
context.fillRect(10, 10, 50, 50);
//设置合成操作
context.globalCompositeOperation = "destination-over";
//绘制蓝色矩形
context.fillStyle = "rgba(0,0,255,1)";
context.fillRect(30, 30, 50, 50);
```

### WebGL

#### 类型化数组

类型化数组的核心就是一个名为ArrayBuffer 的类型。每个ArrayBuffer 对象表示的是内存中指定的字节数

```js
var buffer = new ArrayBuffer(20);//分配20B
```

```js
var bytes = buffer.byteLength;
```

##### 视图

最常见的视图是DataView，通过它可以选择ArrayBuffer中的一小段字节。创建DataView实例的时候传入一个ArrayBuffer、一个可选的字节偏移量（从该字节开始选择）和一个可选的要选择的字节数。

```js
//基于整个缓冲器创建一个新视图
var view = new DataView(buffer);
//创建一个开始于字节9 的新视图
var view = new DataView(buffer, 9);
//创建一个从字节9 开始到字节18 的新视图
var view = new DataView(buffer, 9, 10);
```

```js
alert(view.byteOffset);
alert(view.byteLength);
```

DataView支持的数据类型和相应的读写方法：

![image-20200715211758483](https://gitee.com/snow_zhao/img/raw/master/img/image-20200715211758483.png)

![image-20200715211839800](https://gitee.com/snow_zhao/img/raw/master/img/image-20200715211839800.png)

第一个参数都是字节偏移量，表示从哪个字节开始读入或写出

```js
var buffer = new ArrayBuffer(20),
    view = new DataView(buffer),
    value;
view.setUint16(0, 25);
view.setUint16(2, 50); //不能从字节1开始，因为16位整数要用2B
value = view.getUint16(0);
```

littleEndian是一个布尔值，表示读写数值时是否采用小端字节序（即将数据的最低有效位保存在低内存地址中），而不是大端字节序（即将数据的最低有效位保存在高内存地址中)

```js
var buffer = new ArrayBuffer(20),
    view = new DataView(buffer),
    value;
view.setUint16(0, 25);
value = view.getInt8(0);
alert(value); //0
```

##### 类型化视图

都继承DataView，可分为以下几种：

* Int8Array：表示8 位二补整数。
* Uint8Array：表示8 位无符号整数。
* Int16Array：表示16 位二补整数。
* Uint16Array：表示16 位无符号整数。
* Int32Array：表示32 位二补整数。
* Uint32Array：表示32 位无符号整数。
* Float32Array：表示32 位IEEE 浮点值。
* Float64Array：表示64 位IEEE 浮点值。

```js
//创建一个新数组，使用整个缓冲器
var int8s = new Int8Array(buffer);
//只使用从字节9 开始的缓冲器
var int16s = new Int16Array(buffer, 9);
//只使用从字节9 到字节18 的缓冲器
var uint16s = new Uint16Array(buffer, 9, 10);
```

```js
//使用缓冲器的一部分保存8 位整数，另一部分保存16 位整数
var int8s = new Int8Array(buffer, 0, 10);
var uint16s = new Uint16Array(buffer, 11, 10);
```

每个视图构造函数都有一个名为BYTES_PER_ELEMENT 的属性，表示类型化数组的每个元素需要多少字节

```js
//需要10 个元素空间
var int8s = new Int8Array(buffer, 0, 10 * Int8Array.BYTES_PER_ELEMENT);
//需要5 个元素空间
var uint16s = new Uint16Array(buffer, int8s.byteOffset + int8s.byteLength,5 * Uint16Array.BYTES_PER_ELEMENT);
```

```js
//类型化视图
//创建一个数组保存5 个8 位整数（10 字节）
var int8s = new Int8Array([10, 20, 30, 40, 50]);
```

类型化视图的一个方法：subarray()，基于底层数组缓冲器的子集创建一个新视图。这个方法接收两个参数：开始元素的索引和可选的结束元素的索引

```js
var uint16s = new Uint16Array(10),
	sub = uint16s.subarray(2, 5);
```

#### WebGL上下文

```js
    let drawing = document.getElementById("drawing");
    let gl = drawing.getContext("webgl");
    if(gl){
        alert("Exist!");
    }
```

通过给getContext()传递第二个参数，可以对WebGL上下文进行一些设置。这个参数是一个对象，包含以下属性：

* alpha：值为true，表示为上下文创建一个Alpha 通道缓冲区；默认值为true。
* depth：值为true，表示可以使用16 位深缓冲区；默认值为true。
* stencil：值为true，表示可以使用8 位模板缓冲区；默认值为false。
* antialias：值为true，表示将使用默认机制执行抗锯齿操作；默认值为true。
* premultipliedAlpha：值为true，表示绘图缓冲区有预乘Alpha 值；默认值为true。
* preserveDrawingBuffer：值为true，表示在绘图完成后保留绘图缓冲区；默认值为false。

```js
var gl = drawing.getContext("experimental-webgl", { alpha: false});
```

##### 准备绘图

使用clearColor()方法来指定要使用的颜色值，该方法接收4 个参数：红、绿、蓝和透明度。

```js
gl.clearColor(0,0,0,1); //black
gl.clear(gl.COLOR_BUFFER_BIT);//使用之前定义的颜色来填充相关区域
```

##### 视口与坐标

默认情况下，视口可以使用整个`<canvas>`区域。要改变视口大小，可以调用viewport()方法并传入4 个参数：（视口相对于`<canvas>`元素的x 坐标、y 坐标、宽度和高度

```js
//视口是<canvas>左下角的四分之一区域
gl.viewport(0, 0, drawing.width/2, drawing.height/2);
//视口是<canvas>左上角的四分之一区域
gl.viewport(0, drawing.height/2, drawing.width/2, drawing.height/2);
//视口是<canvas>右下角的四分之一区域
gl.viewport(drawing.width/2, 0, drawing.width/2, drawing.height/2);
```

##### 缓冲区

```js
var buffer = gl.createBuffer();
gl.bindBuffer(gl.ARRAY_BUFFER, buffer);
gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([0, 0.5, 1]), gl.STATIC_DRAW);
```

gl.bufferData()的最后一个参数用于指定使用缓冲区的方式，取值范围是如下几个常量。
* gl.STATIC_DRAW：数据只加载一次，在多次绘图中使用。
* gl.STREAM_DRAW：数据只加载一次，在几次绘图中使用。
* gl.DYNAMIC_DRAW：数据动态改变，在多次绘图中使用。

```js
gl.deleteBuffer(buffer);
```

##### 错误

WebGL 操作一般不会抛出错误。所以我们需要在调用某个可能出错的方法后，手工调用gl.getError()方法。这个方法返回一个表示错误类型的常量。可能的错误常量：

* gl.NO_ERROR：上一次操作没有发生错误（值为0）。
* gl.INVALID_ENUM：应该给方法传入WebGL 常量，但却传错了参数。
* gl.INVALID_VALUE：在需要无符号数的地方传入了负值。
* gl.INVALID_OPERATION：在当前状态下不能完成操作。
* gl.OUT_OF_MEMORY：没有足够的内存完成操作。
* gl.CONTEXT_LOST_WEBGL：由于外部事件（如设备断电）干扰丢失了当前WebGL 上下文。

##### 着色器

WebGL 中有两种着色器：顶点着色器和片段（或像素）着色器。顶点着色器用于将3D 顶点转换为需要渲染的2D 点。片段着色器用于准确计算要绘制的每个像素的颜色。

##### 编写着色器

```glsl
//OpenGL 着色语言
//着色器，作者Bartek Drozdz，摘自他的文章
//http://www.netmagazine.com/tutorials/get-started-webgl-draw-square
attribute vec2 aVertexPosition;
void main() {
	gl_Position = vec4(aVertexPosition, 0.0, 1.0);
}
```

```glsl
//OpenGL 着色语言
//着色器，作者Bartek Drozdz，摘自他的文章
//http://www.netmagazine.com/tutorials/get-started-webgl-draw-square
uniform vec4 uColor;
void main() {
	gl_FragColor = uColor;
}
```

片段着色器必须返回一个值，赋给变量gl_FragColor，表示绘图时使用的颜色

##### 编写着色器程序

暂时略




