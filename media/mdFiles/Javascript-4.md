# 客户端检测

1. 能力检测：

   ```js
   function getElement(id){
   	if (document.getElementById){
   		return document.getElementById(id);
   	} else if (document.all){
   		return document.all[id];
   	} else {
   		throw new Error("No way to retrieve element!");
   	}
   }
   ```

2. 检测是否支持排序：

   ```js
   function isSortable(object){
   	return typeof object.sort == "function";
   }
   ```

### 大量内容略

# DOM

### Node类型

1. javascript中所有节点类型都继承自Node类型

2. 每个节点都有一个nodeType属性，表明节点类型：

    * Node.ELEMENT_NODE(1)；
    * Node.ATTRIBUTE_NODE(2)；
    * Node.TEXT_NODE(3)；
    * Node.CDATA_SECTION_NODE(4)；
    * Node.ENTITY_REFERENCE_NODE(5)；
    * Node.ENTITY_NODE(6)；
    * Node.PROCESSING_INSTRUCTION_NODE(7)；
    * Node.COMMENT_NODE(8)；
    * Node.DOCUMENT_NODE(9)；
    * Node.DOCUMENT_TYPE_NODE(10)；
    * Node.DOCUMENT_FRAGMENT_NODE(11)；
    * Node.NOTATION_NODE(12)
    
3. 判断节点类型是否为元素：

    ```js
    if(someNode.nodeType == 1){
    	alert("Node is an element.");
    }
    ```

4. nodeName与nodeValue属性：

    ```js
    if(someNode.nodeType == 1){
    	value = someNode.nodeName;//元素节点标签名
    }
    ```

    对于元素节点：nodeName中保存的始终都是元素的标签名，而nodeValue的值则始终为null

5. 节点关系：

    每个节点都有一个childNodes属性，其中保存着一个NodeList对象，NodeList是一种类数组对象，用于保存一组有序的节点，并可以通过位置来访问这些节点（并非Array的实例)。NodeList对象的独特之处在于它是基于DOM结构**动态**执行查询的结果

    ```js
        let firstChild = someNode.childNodes[0];
        let secondChild = someNode.childNodes.item(1);
        let count = someNode.childNodes.length;
    ```

    将NodeList对象转换成数组：

    ```js
    let arrayOfNodes = Array.prototype.slice.call(someNode.childNodes, 0);//IE不适用
    ```

    ```js
        function convertToArray(nodes) {
            let array = null;
            try{
                array = Array.prototype.slice.call(nodes, 0);
            }catch (ex) {
                array = [];
                for(let i = 0; i < nodes.length; i++ ){
                    array.push(nodes[i]);
                }
            }
            return array;
        }//通用
    ```

    属性：

    * parentNode
    * childNodes
    * previousSibling
    * nextSibling
    * firstChild
    * lastChild

    hasChildNodes()方法在节点但包含一个或多个子节点的情况下返回True。所有节点都有ownerDocument属性，该属性指向整个文档的文档节点。

6. 操作节点

    * appendChild()

    ```js
        let someNode, newNode;
        let returnNode = someNode.appendChild(newNode);
        alert(returnNode === newNode);
        alert(someNode.lastChild === newNode);
    ```

    * insertBefore()

    ```js
    //两个参数：要插入的节点和作为参照的节点，如果参照节点为null，则执行结果与appendChild()相同。
    
    //插入后成为最后一个子节点
    returnedNode = someNode.insertBefore(newNode, null);
    alert(newNode == someNode.lastChild); //true
    
    //插入后成为第一个子节点
    var returnedNode = someNode.insertBefore(newNode, someNode.firstChild);
    alert(returnedNode == newNode); //true
    alert(newNode == someNode.firstChild); //true
    
    //插入到最后一个子节点前面
    returnedNode = someNode.insertBefore(newNode, someNode.lastChild);
    alert(newNode == someNode.childNodes[someNode.childNodes.length-2]); //true
    ```

    * replaceChild()

    ```js
    //两个参数：要插入的节点和要替换的节点
    
    //替换第一个子节点
    var returnedNode = someNode.replaceChild(newNode, someNode.firstChild);
    
    //替换最后一个子节点
    returnedNode = someNode.replaceChild(newNode, someNode.lastChild);
    ```

    * removeChild()

    ```js
    //一个参数：要移除的节点
    
    //移除第一个子节点
    var formerFirstChild = someNode.removeChild(someNode.firstChild);
    
    //移除最后一个子节点
    var formerLastChild = someNode.removeChild(someNode.lastChild);
    ```

    * cloneNode()：所有类型的节点都有该方法

      创建一个完全相同的副本，接受一个布尔值参数，表示是否执行深复制（复制节点和整颗子节点数）。复制后的结点是孤立的，没有为它指定父节点

    * normalize()：处理文档树中的文本节点

### Document类型

1. document对象是window对象的一个属性，具有以下特征：

   * nodeType 的值为9；
   * nodeName 的值为"#document"；
   * nodeValue 的值为null；
   * parentNode 的值为null；
   * ownerDocument 的值为 null；
   * 其子节点可能是一个DocumentType（最多一个）、Element（最多一个）、ProcessingInstruction或Comment。

2. 文档的子节点：

   * documentElement属性，始终指向HTML页面的`<html>`元素
   * 通过childnodes列表访问文档元素
   * document.body：取得对body属性的引用
   * document.doctype：取得对`<!DOCTYPE>`的引用
   * document.title：取得网页标题
   * document.URL：取得完整的URL
   * document.domain：取得域名(可修改)
   * document.referer：取得来源页面的URL

3. 方法：

   查找元素：

   * getElementById()：接受一个参数：要取得元素的ID，

   * getElementsByTagName()：接受一个参数：要取得元素的标签名，返回包含零个或多个元素的NodeList。在HTML文档中返回HTMLCollection对象，HTML对象支持按名称访问项：如`image['myImage']`

     ```js
     var images = document.getElementsByTagName("img");
     alert(images.length); //输出图像的数量
     alert(images[0].src); //输出第一个图像元素的src 特性
     alert(images.item(0).src); //输出第一个图像元素的 src 特性
     ```

   * namedItem()：根据元素的name特性取得集合中的项

   `document.getElementsByTagName("*")`返回的HTMLCollection中包含了整个页面的所有元素（按照它们出现的先后顺序）

   HTMLDocument类型才有的方法：getElementsByName()，返回一个HTMLColletion对象

   特殊集合：

   * document.anchors, 包含文档中所有带name属性的`<a>`元素
   * document.applets，不推荐使用
   * document.forms，包含文档中所有的`<form>`元素
   * document.images，包含文档中所有`<img>`元素
   * document.links，包含文档中所有带`href`特性的`<a>`标签

   DOM一致性检测：

   ![image-20200710101337839](https://gitee.com/snow_zhao/img/raw/master/img/image-20200710101337839.png)

   文档写入：

   document对象的几个方法：

   * write()
   * writeln()：在传入字符串的末尾添加一个换行符在将输出流写入网页
   * open()：打开网页的输出流
   * close()：关闭网页的输出流

   ```html
   <!DOCTYPE html>
   <html lang="en">
   <head>
       <meta charset="UTF-8">
       <title>document.write() Example</title>
   </head>
   <body>
       <p>The current date and time is:
       <script type="text/javascript">
           document.write("<strong>" + (new Date()).toString() + '</strong>');
       </script>
       </p>
   </body>
   </html>
   ```

   ```js
   document.write("<script type=\"text/javascript\" src=\"file.js\">" + "<\/script>");
   ```

### Element类型

1. Element节点的特征：

   * nodeType 的值为1；
   * nodeName 的值为元素的标签名；
   * nodeValue 的值为null；
   * parentNode 可能是Document 或Element；
   * 其子节点可能是Element、Text、Comment、ProcessingInstruction、CDATASection 或EntityReference。
   
   要访问元素的标签名，可以使用nodeName属性，也可以使用tagName属性

2. HTML元素：

   所有HTML元素都有HTMLElement类型表示，属性：

   * id，元素在文档中的唯一标识符。
   * title，有关元素的附加说明信息，一般通过工具提示条显示出来。
   * lang，元素内容的语言代码，很少使用。
   * dir，语言的方向，值为"ltr"（left-to-right，从左至右）或"rtl"（right-to-left，从右至左），也很少使用。
   * className，与元素的class 特性对应，即为元素指定的CSS类。没有将这个属性命名为class，是因为class 是ECMAScript 的保留字（有关保留字的信息，请参见第1章）。
   
   `<div id="myDiv" class="bd" title="Body text" lang="en" dir="ltr"></div>`
   
   ```js
   var div = document.getElementById("myDiv");
   alert(div.id); //"myDiv""
   alert(div.className); //"bd"
   alert(div.title); //"Body text"
   alert(div.lang); //"en"
   alert(div.dir); //"ltr"
   //也可以对这些属性直接赋值修改
   ```
   
   所有HTML元素以及与之关联的类型：
   
   ![image-20200710111536240](https://gitee.com/snow_zhao/img/raw/master/img/image-20200710111536240.png)
   
   ![image-20200710111557259](https://gitee.com/snow_zhao/img/raw/master/img/image-20200710111557259.png)
   
3. **取得特性**：getAttribute()，还可以取得自定义特性

   `var div = document.getElementById("myDiv"); `

   `eg`：`div.getAttribute("id")`，特性名称不区分大小写

   根据HTML5规范，自定义特性应该加上`data-`前缀以便验证

   任何元素的所有特性，都可以通过DOM元素本身的属性来访问，不过，只有公认的（非自定义）的特性才会以属性的形式添加到DOM对象中：

   ```js
   alert(div.id); //"myDiv"
   alert(div.my_special_attribute); //undefined（IE 除外）
   alert(div.align); //"left"
   ```

   有两类特殊的特性属性的值与通过getAttribute()返回的值并不相同。
   

第一类特性就是style，用于通过CSS 为元素指定样式。在通过getAttribute()访问时，返回的style 特性值中包含的是CSS 文本，而通过属性来访问它则会返回一个对象。

第二类与众不同的特性是onclick 这样的事件处理程序。当在元素上使用时，onclick 特性中包含的JavaScript 代码，如果通getAttribute()访问，则会返回相应代码的字符串。而在访问onclick 属性时，则会返回一个JavaScript 函数（如果未在元素中指定相应特性，则返回null）。开发人员经常不使用getAttribute()，而是只使用对象的属性。只有在取得自定义特性值的情况下，才会使用getAttribute()方法。

**设置特性**：setAttribute()，接受两个参数：要设置的特性名和值。若特性已存在，则替换原值。

`eg`：`div.setAttribute("id", "someOtherId");`

可以通过直接给属性赋值的方法修改特性的值，但不能通过此方式添加自定义属性

**删除属性**：removeAttribute()

   **attributes属性**：包含一个NamedNodeMap，与NodeList类似，是一个动态的集合

   NamedNodeMap对象的方法：

   * getNamedItem(name)：返回nodeName 属性等于name 的节点；
   * removeNamedItem(name)：从列表中移除nodeName 属性等于name 的节点；
   * setNamedItem(node)：向列表中添加节点，以节点的nodeName属性为索引；
   * item(pos)：返回位于数字pos位置处的节点。

   attributes属性中包含一系列节点，每个节点的nodeName为特性名，nodeValue为特性值

   取得元素的id特性：

   ```js
   var id = element.attributes.getNamedItem("id").nodeValue;
   //or
   var id = element.attributes["id"].nodeValue;
   //也可以通过此种方式来设置特性的值
   ```

   ```js
   //删除特性
   var oldAttr = element.attributes.removeNamedItem("id");
   
   //添加特性
   element.attributes.setNamedItem(newAttr);
   ```

   ```js
   //遍历元素的特性
   function outputAttributes(element){
       let pairs = [], attrName, attrValue, i, len;
       for (i=0, len=element.attributes.length; i < len; i++){
           attrName = element.attributes[i].nodeName;
           attrValue = element.attributes[i].nodeValue;
           if(element.attributes[i].specified){
           	pairs.push(attrName + "=\"" + attrValue + "\"");
           }
        }
        return pairs.join(" ");
   }
   ```

   创建元素：document.createElement()：接受一个参数，要创建元素的标签名，在HTML中不区分大小写，在XML中区分大小写：

   ```js
       let div = document.createElement("div");
       div.id = 'MyNewDiv';
       div.className = 'box';
       div.textContent = "Hello world";
       document.body.appendChild(div);
   ```

   在IE中，可以采用另一种方式使用createElement()，即为这个方法传入完整的元素标签：

   ```js
   let div = document.createElement("<div id=\"MyNewDiv\" class=\"box\">你好世界</div>")//我尝试好像失败了，不知道IE是否现在仍支持这种语法
   ```

4. Text类型

   Text节点具有以下特征：

   * nodeType 的值为3；
   * nodeName 的值为"#text"；
   * nodeValue 的值为节点所包含的文本；
   * parentNode 是一个Element；
   * 不支持（没有）子节点。
   
   可以通过nodeValue属性或data属性来访问Text节点中包含的文本
   
   操作方法：
   
   * appendData(text)：将text 添加到节点的末尾。
   * deleteData(offset, count)：从offset 指定的位置开始删除count 个字符。
   * insertData(offset, text)：在offset指定的位置插入text。
   * replaceData(offset, count, text)：用text 替换从offset 指定的位置开始到offset+count 为止处的文本。
   * splitText(offset)：从offset 指定的位置将当前文本节点分成两个文本节点。
   * substringData(offset, count)：提取从offset 指定的位置开始到offset+count 为止处的字符串。
   
   文本节点中length属性保存着字符的数目，nodeValue.length与data.length中保存着同样的值
   
   访问文本节点：`<div>Hello world!</div>`
   
   ```js
   let textNode = div.firstChild;
   ```
   
   ```js
       let div = document.getElementsByTagName('div')
       let textNode = div[0].firstChild;
       alert(textNode.nodeValue);
       textNode.nodeValue = "Are you ok!";
   ```
   
   * 创建文本节点：
   
     `document.createTextNode()`：接受一个参数，要插入节点中的文本
   
     ```js
     let div = document.createElement("div");
     div.className = 'message';
     let text = document.createTextNode("Hello world");
     div.appendChild(text);
     document.body.appendChild(div);
     ```
   
     一般情况下每个元素只有一个文本子节点，但在某些情况下也可能包含多个文本子节点：
   
     ```js
     let div = document.createElement("div");
     div.className = 'message';
     let text = document.createTextNode("Hello world");
     div.appendChild(text);
     let text2 = document.createTextNode(".Yappy!");
     div.appendChild(text2);
     document.body.appendChild(div);
     ```
   
   * 规范化文本节点：
   
     normalize()方法：在包含两个或多个文本节点的父元素上调用normalize()方法，会将所有的文本节点合并成一个节点
   
     分隔文本节点：
   
     spilitText()方法：接收一个位置值，然后分隔节点
   
5. Comment类型：
   
   Comment节点的特征：
   
   * nodeType 的值为8；
   * nodeName 的值为"#comment"；
   * nodeValue 的值是注释的内容；
   * parentNode 可能是Document 或Element；
   * 不支持（没有）子节点。
   
   Comment类型与Text类型继承自相同的基类：也可以通过nodeValue或data属性来取得注释的内容
   
   ```js
   let divs = document.getElementsByTagName('div');
   let div = divs[0];
   let comment = div.firstChild;
   alert(comment.nodeValue);
   ```
   
   创建comment节点：`document.createComment()`
   
6. CDATASection类型：

   该类型只针对XML的文档，表示CDATA区域。继承自Text类型，拥有处理splitText()之外的所有字符串操作方法。

   节点特征：

   * nodeType 的值为4；
   * nodeName 的值为"#cdata-section"；
   * nodeValue 的值是CDATA 区域中的内容；
   * parentNode 可能是Document 或Element；
   * 不支持（没有）子节点。
   
   在真正的XML文档中，可以用`document.createCDataSection()`创建CDATA区域
   
7. DocumentType类型：

   特征：

   * nodeType 的值为10；
   * nodeName 的值为doctype 的名称；
   * nodeValue 的值为null；
   * parentNode 是Document；
   * 不支持（没有）子节点。
   
8. DocumentFragment类型：

   特征：

   * nodeType 的值为11；
   * nodeName 的值为"#document-fragment"；
   * nodeValue 的值为null；
   * parentNode 的值为null；
   * 子节点可以是Element、ProcessingInstruction、Comment、Text、CDATASection 或EntityReference。
   
   文档片段继承了Node的所有方法
   
9. Attr类型：

   特征：

   * nodeType 的值为2；
   * nodeName 的值是特性的名称；
   * nodeValue 的值是特性的值；
   * parentNode 的值为null；
   * 在HTML 中不支持（没有）子节点；
   * 在XML 中子节点可以是Text 或EntityReference。
   
   三个属性：name、value和specified

### DOM操作技术

1. 动态脚本：

   ```js
   function loadScriptString(code) {
       let script = document.createElement('script');
       script.type = "text/javascript";
       try{
               script.appendChild(document.createTextNode(code));
       }catch (ex) {
           script.text = code;
       }
       document.body.appendChild(script);
   }
   loadScriptString("function sayHi(){alert('hi');}");
   ```

2. 动态样式：

   `<link rel="stylesheet" type="text/css" href="styles.css">`

   ```js
   var link = document.createElement("link");
   link.rel = "stylesheet";
   link.type = "text/css";
   link.href = "style.css";
   var head = document.getElementsByTagName("head")[0];
   head.appendChild(link);
   ```

   ```html
   <style type="text/css">
   body {
   	background-color: red;
   }
   </style>
   ```

   ```js
   var style = document.createElement("style");
   style.type = "text/css";
   style.appendChild(document.createTextNode("body{background-color:red}"));
   var head = document.getElementsByTagName("head")[0];
   head.appendChild(style);
   ```

3. 操作表格：

   ```html
   <table border="1" width="100%">
       <tbody>
           <tr>
               <td>Cell 1,1</td>
               <td>Cell 2,1</td>
           </tr>
           <tr>
               <td>Cell 1,2</td>
               <td>Cell 2,2</td>
           </tr>
       </tbody>
   </table>
   ```

   HTML DOM为`table`、`tbody`、`tr`元素添加了一些属性和方法：

   * caption：保存着对`<caption>`元素（如果有）的指针。
   * tBodies：是一个`<tbody>`元素的HTMLCollection。
   * tFoot：保存着对`<tfoot>`元素（如果有）的指针。
   * tHead：保存着对`<thead>`元素（如果有）的指针。
   * rows：是一个表格中所有行的HTMLCollection。
   * createTHead()：创建`<thead>`元素，将其放到表格中，返回引用。
   * createTFoot()：创建`<tfoot>`元素，将其放到表格中，返回引用。
   * createCaption()：创建`<caption>`元素，将其放到表格中，返回引用。
   * deleteTHead()：删除`<thead>`元素。
   * deleteTFoot()：删除`<tfoot>`元素。
   * deleteCaption()：删除`<caption>`元素。
   * deleteRow(pos)：删除指定位置的行。
   * insertRow(pos)：向rows 集合中的指定位置插入一行。
   为`<tbody>`元素添加的属性和方法如下。
   * rows：保存着`<tbody>`元素中行的HTMLCollection。
   * deleteRow(pos)：删除指定位置的行。
   * insertRow(pos)：向rows 集合中的指定位置插入一行，返回对新插入行的引用。为`<tr>`元素添加的属性和方法如下。
   * cells：保存着`<tr>`元素中单元格的HTMLCollection。
   * deleteCell(pos)：删除指定位置的单元格。
   * insertCell(pos)：向cells 集合中的指定位置插入一个单元格，返回对新插入单元格的引用。
   
   ```js
   //创建table
   var table = document.createElement("table");
   table.border = 1;
   table.width = "100%";
   
   //创建tbody
   var tbody = document.createElement("tbody");
   table.appendChild(tbody);
   
   //创建第一行
   tbody.insertRow(0);
   tbody.rows[0].insertCell(0);
   tbody.rows[0].cells[0].appendChild(document.createTextNode("Cell 1,1"));
   tbody.rows[0].insertCell(1);
   tbody.rows[0].cells[1].appendChild(document.createTextNode("Cell 2,1"));
   
   //创建第二行
   tbody.insertRow(1);
   tbody.rows[1].insertCell(0);
   tbody.rows[1].cells[0].appendChild(document.createTextNode("Cell 1,2"));
   tbody.rows[1].insertCell(1);
   tbody.rows[1].cells[1].appendChild(document.createTextNode("Cell 2,2"));
   
   //将表格添加到文档主体中
   document.body.appendChild(table);
   ```
   
4. NodeList及其"近亲"NamedNodeMap和HTMLCollection都是==动态==的



