# 查询

`all()`返回的 `QuerySet` 包含了数据表中所有的对象。虽然，大多数情况下，你只需要完整对象集合的一个子集。

要创建一个这样的子集，你需要通过添加过滤条件精炼原始`QuerySet`。两种最常见的精炼 `QuerySet` 的方式是：

- `filter(**kwargs)`

  返回一个新的 `QuerySet`，包含的对象满足给定查询参数。

- `exclude(**kwargs)`

  返回一个新的 `QuerySet`，包含的对象**不**满足给定查询参数。

```python
Entry.objects.filter(pub_date__year=2006)
```

精炼 `QuerySet` 的结果本身还是一个`QuerySet`，所以能串联精炼过程

`get()`检索单个对象，接收参数和`filter()`类似

```python
Entry.objects.all()[:5]	# 限制条目数， 不支持负索引
```

为了获取从前 10 个对象中，每隔一个抽取的对象组成的列表:

```python
Entry.objects.all()[:10:2]
```

基本的查询关键字参数遵照 `field__lookuptype=value`

查询子句中指定的字段必须是模型的一个字段名。不过也有个例外，在 `ForeignKey` 中，你可以指定以 `_id` 为后缀的字段名。这种情况下，value 参数需要包含 foreign 模型的主键的原始值

```python
Entry.objects.filter(blog_id=4)
```

`exact`

```python
>>> Blog.objects.get(id__exact=14)  # Explicit form
>>> Blog.objects.get(id=14)         # __exact is implied
# 两种方式等价
```

`iexact`

不区分大小写的匹配

`contains`

大小写敏感的包含测试

`startswith`, `endswith`

以……开头和以……结尾的查找。当然也有大小写不敏感的版本，名为 `istartswith`和 `iendswith`。

要筛选出所有关联条目同时满足标题含有 *"Lennon"* 且发布于 2008 （同一个条目，同时满足两个条件）年的博客

```python
Blog.objects.filter(entry__headline__contains='Lennon', entry__pub_date__year=2008)
```

要筛选所有条目标题包含 *"Lennon"* 或条目发布于 2008 年的博客

```python
Blog.objects.filter(entry__headline__contains='Lennon').filter(entry__pub_date__year=2008)
```

### 过滤器可以为模型指定字段

将模型字段值与同一模型中的另一字段做比较

Django 提供了 `F 表达式` 实现这种比较。 `F()` 的实例充当查询中的模型字段的引用

要查出所有评论数大于 pingbacks 的博客条目，我们构建了一个 `F()` 对象，指代 pingback 的数量，然后在查询中使用该 `F()` 对象:

```python
>>> from django.db.models import F
>>> Entry.objects.filter(number_of_comments__gt=F('number_of_pingbacks'))
```

### 主键 (`pk`) 查询快捷方式

出于方便的目的，Django 提供了一种 `pk` 查询快捷方式， `pk` 表示主键 "primary key"。

示例 `Blog` 模型中，主键是 `id` 字段，所以这 3 个语句是等效的:

```python
>>> Blog.objects.get(id__exact=14) # Explicit form
>>> Blog.objects.get(id=14) # __exact is implied
>>> Blog.objects.get(pk=14) # pk implies id__exact
```

```python
# Get blogs entries with id 1, 4 and 7
>>> Blog.objects.filter(pk__in=[1,4,7])

# Get all blog entries with id > 14
>>> Blog.objects.filter(pk__gt=14)
```

### 通过 `Q` 对象完成复杂查询

```python
from django.db.models import Q
Q(question__startswith='What')
```

```python
Q(question__startswith='Who') | Q(question__startswith='What')
```

```
Poll.objects.get(
    Q(question__startswith='Who'),
    Q(pub_date=date(2005, 5, 2)) | Q(pub_date=date(2005, 5, 6))
)
```

### 删除对象

通常，删除方法被命名为 `delete()`。该方法立刻删除对象，并返回被删除的对象数量和一个包含了每个被删除对象类型的数量的字典

所有 `QuerySet`都有 `delete()` 方法，它会删除 `QuerySet` 中的所有成员

### 复制模型实例

```python
blog = Blog(name='My blog', tagline='Blogging is easy')
blog.save() # blog.pk == 1

blog.pk = None
blog.save() # blog.pk == 2
```

继承
```python
class ThemeBlog(Blog):
    theme = models.CharField(max_length=200)

django_blog = ThemeBlog(name='Django', tagline='Django is easy', theme='python')
django_blog.save() # django_blog.pk == 3
```

```python
django_blog.pk = None
django_blog.id = None
django_blog.save() # django_blog.pk == 4
```

`ManyTOManyField`

在复制条目后，你必须为新条目设置多对多关联关系。

```python
entry = Entry.objects.all()[0] # some previous entry
old_authors = entry.authors.all()
entry.pk = None
entry.save()
entry.authors.set(old_authors)
```

对于 `OneToOneField` 关联，你必须拷贝关联对象，并将其指定给新对象的关联字段，避免违反一对一唯一性约束

```python
detail = EntryDetail.objects.all()[0]
detail.pk = None
detail.entry = entry
detail.save()
```

## 一次修改多个对象

有时候，你想统一设置 `QuerySet` 中的所有对象的某个字段。你可以通过 `update()`达到目的

```python
# Update all the headlines with pub_date in 2007.
Entry.objects.filter(pub_date__year=2007).update(headline='Everything is the same')
```

你**仅**能用此方法设置非关联字段和 `ForeignKey` 字段。要修改非关联字段，需要用常量提供新值。要修改 `ForeignKey`字段，将新值置为目标模型的新实例

```python
>>> b = Blog.objects.get(pk=1)

# Change every Entry so that it belongs to this Blog.
>>> Entry.objects.all().update(blog=b)
```

调用更新方法时也能使用 `F 表达式`基于同一模型另一个字段的值更新某个字段。这在基于计数器的当前值增加其值时特别有用

你可以通过 `foreign-key` 属性获取和设置值。如你所想，对外键的修改直到你调用 `save()` 后才会被存入数据库

若模型有 `ForeignKey`，外键关联的模型实例将能访问 `Manager`，后者会返回第一个模型的所有实例。默认情况下，该 `Manager`名为 `FOO_set`， `FOO` 即源模型名的小写形式。`Manager` 返回 `QuerySets`

可以在定义  `ForeignKey` 时设置 `related_name` 参数重写这个 `FOO_set` 名。例如，若修改 `Entry` 模型为 `blog = ForeignKey(Blog, on_delete=models.CASCADE, related_name='entries')`

```python
from django.db import models

class Entry(models.Model):
    #...
    objects = models.Manager()  # Default Manager
    entries = EntryManager()    # Custom Manager

b = Blog.objects.get(id=1)
b.entry_set(manager='entries').all()
```

```python
b.entry_set(manager='entries').is_published()
```

```python
Entry.objects.filter(blog=b) # Query using object instance
Entry.objects.filter(blog=b.id) # Query using id from instance
Entry.objects.filter(blog=5) # Query using id directly
```