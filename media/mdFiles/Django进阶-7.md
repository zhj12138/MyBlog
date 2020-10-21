# 表单集

```python
>>> ArticleFormSet = formset_factory(ArticleForm)
```

如你所见，它只显示一个空表单。显示的空表单数量由 `额外` 参数控制。默认情况下，[`formset_factory()`](https://docs.djangoproject.com/zh-hans/3.0/ref/forms/formsets/#django.forms.formsets.formset_factory) 定义了一个额外表单；下面的例子将创建一个表单集类来显示两个空白表单

```python
>>> ArticleFormSet = formset_factory(ArticleForm, extra=2)
```

#### 限制表单的最大数量

```python
ArticleFormSet = formset_factory(ArticleForm, extra=2, max_num=1)
```

### Formset验证

```python
>>> from django.forms import formset_factory
>>> from myapp.forms import ArticleForm
>>> ArticleFormSet = formset_factory(ArticleForm)
>>> data = {
...     'form-TOTAL_FORMS': '1',
...     'form-INITIAL_FORMS': '0',
...     'form-MAX_NUM_FORMS': '',
... }
>>> formset = ArticleFormSet(data)
>>> formset.is_valid()
True


>>> data = {
...     'form-TOTAL_FORMS': '2',
...     'form-INITIAL_FORMS': '0',
...     'form-MAX_NUM_FORMS': '',
...     'form-0-title': 'Test',
...     'form-0-pub_date': '1904-06-16',
...     'form-1-title': 'Test',
...     'form-1-pub_date': '', # <-- this date is missing but required
... }
>>> formset = ArticleFormSet(data)
>>> formset.is_valid()
False
>>> formset.errors
[{}, {'pub_date': ['This field is required.']}]
```

我们可以使用` total_error_count `方法来检查formset中有多少错误

```python
formset.has_changed()
```

formset中有些必要的数据( `form-TOTAL_FORMS` , `form-INITIAL_FORMS` 以及 `form-MAX_NUM_FORMS` )。这些数据是 `ManagementForm` 所必须的。它被formset用来管理formset中所有表单

`BaseFormSet` 有一对与 `ManagementForm` 密切相关的方法， `total_form_count` 和 `initial_form_count` 。

`total_form_count` 返回该formset内表单的总和。 `initial_form_count` 返回该formset内预填充的表单数量，同时用于定义需要多少表单。

#### validate_max

如果方法 [`formset_factory()`](https://docs.djangoproject.com/zh-hans/3.0/ref/forms/formsets/#django.forms.formsets.formset_factory) 有设置参数 `validate_max=True` ，验证还会检查数据集内表单的数量，减去那些被标记为删除的表单数量，剩余数量需小于等于 `max_num` 。

`validate_min`

### 表单的排序和删除

`BaseFormSet.can_order`

默认值： `False`

让你创建能排序的formset:

`BaseFormSet.can_delete`

默认值： `False`

让你创建能删除指定表单的formset

###  添加额外字段

```python
>>> class BaseArticleFormSet(BaseFormSet):
...     def add_fields(self, form, index):
...         super().add_fields(form, index)
...         form.fields["my_field"] = forms.CharField()
```

### 传递自定义参数

```python
>>> from django.forms import BaseFormSet
>>> from django.forms import formset_factory
>>> from myapp.forms import ArticleForm

>>> class MyArticleForm(ArticleForm):
...     def __init__(self, *args, user, **kwargs):
...         self.user = user
...         super().__init__(*args, **kwargs)

>>> ArticleFormSet = formset_factory(MyArticleForm)
>>> formset = ArticleFormSet(form_kwargs={'user': request.user})
```

### 自定义前缀

在已渲染的HTML页面中，表单集中的每个字段都包含一个前缀。这个前缀默认是 `'form'` ，但可以使用formset的 `prefix` 参数来自定义。

例如，在默认情况下，您可能会看到:

```python
<label for="id_form-0-title">Title:</label>
<input type="text" name="form-0-title" id="id_form-0-title">
```

但使用 `ArticleFormset(prefix='article')` 的话就会变为：

```python
<label for="id_article-0-title">Title:</label>
<input type="text" name="article-0-title" id="id_article-0-title">
```

### 在视图和模板中使用formset

```python
from django.forms import formset_factory
from django.shortcuts import render
from myapp.forms import ArticleForm

def manage_articles(request):
    ArticleFormSet = formset_factory(ArticleForm)
    if request.method == 'POST':
        formset = ArticleFormSet(request.POST, request.FILES)
        if formset.is_valid():
            # do something with the formset.cleaned_data
            pass
    else:
        formset = ArticleFormSet()
    return render(request, 'manage_articles.html', {'formset': formset})
```

```python
<form method="post">
    {{ formset.management_form }}
    <table>
        {% for form in formset %}
        {{ form }}
        {% endfor %}
    </table>
</form>
```

```python
<form method="post">
    <table>
        {{ formset }}
    </table>
</form>
```

### 手动渲染 `can_delete` 和 `can_order`[¶](https://docs.djangoproject.com/zh-hans/3.0/topics/forms/formsets/#manually-rendered-can-delete-and-can-order)

如果您在模板中手动渲染字段，您可以用 `{{ form.DELETE }}` 来渲染参数 `can_delete` 。

```python
<form method="post">
    {{ formset.management_form }}
    {% for form in formset %}
        <ul>
            <li>{{ form.title }}</li>
            <li>{{ form.pub_date }}</li>
            {% if formset.can_delete %}
                <li>{{ form.DELETE }}</li>
            {% endif %}
        </ul>
    {% endfor %}
</form>
```

同样，如果formset能排序( `can_order=True` )，可以用 `{{ form.ORDER }}` 来渲染它。

### 使用多个formset

```python
from django.forms import formset_factory
from django.shortcuts import render
from myapp.forms import ArticleForm, BookForm

def manage_articles(request):
    ArticleFormSet = formset_factory(ArticleForm)
    BookFormSet = formset_factory(BookForm)
    if request.method == 'POST':
        article_formset = ArticleFormSet(request.POST, request.FILES, prefix='articles')
        book_formset = BookFormSet(request.POST, request.FILES, prefix='books')
        if article_formset.is_valid() and book_formset.is_valid():
            # do something with the cleaned_data on the formsets.
            pass
    else:
        article_formset = ArticleFormSet(prefix='articles')
        book_formset = BookFormSet(prefix='books')
    return render(request, 'manage_articles.html', {
        'article_formset': article_formset,
        'book_formset': book_formset,
    })
```

### 从模型创建表单

```python
from django.db import models
from django.forms import ModelForm

TITLE_CHOICES = [
    ('MR', 'Mr.'),
    ('MRS', 'Mrs.'),
    ('MS', 'Ms.'),
]

class Author(models.Model):
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=3, choices=TITLE_CHOICES)
    birth_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.name

class Book(models.Model):
    name = models.CharField(max_length=100)
    authors = models.ManyToManyField(Author)

class AuthorForm(ModelForm):
    class Meta:
        model = Author
        fields = ['name', 'title', 'birth_date']

class BookForm(ModelForm):
    class Meta:
        model = Book
        fields = ['name', 'authors']
```

大致等同于

```python
from django import forms

class AuthorForm(forms.Form):
    name = forms.CharField(max_length=100)
    title = forms.CharField(
        max_length=3,
        widget=forms.Select(choices=TITLE_CHOICES),
    )
    birth_date = forms.DateField(required=False)

class BookForm(forms.Form):
    name = forms.CharField(max_length=100)
    authors = forms.ModelMultipleChoiceField(queryset=Author.objects.all())
```

#### save_m2m()

```python
# Create a form instance with POST data.
>>> f = AuthorForm(request.POST)

# Create, but don't save the new author instance.
>>> new_author = f.save(commit=False)

# Modify the author in some way.
>>> new_author.some_field = 'some_value'

# Save the new instance.
>>> new_author.save()

# Now, save the many-to-many data for the form.
>>> f.save_m2m()
```

只有在您使用 `save(commit=False)` 的时候才需要调用 `save_m2m()` 。当您在表单上使用 `save()` 时，无需调用其他方法，所有数据（包括多对多数据）都会被保存

将 `fields` 属性设置为特殊值 `'__all__'` 以表明需要使用模型中的所有字段

将 `ModelForm` 中Meta类的 `exclude` 属性设置为表单中需要排除的字段列表





