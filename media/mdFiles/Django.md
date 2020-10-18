# First Part

在`terminal`内输入以下指令即可查看`django`版本号

```
...\> py -m django --version
```

创建项目

```
django-admin startproject mysite
```

简易服务器

```
...\> py manage.py runserver
```

更换端口

```
...\> py manage.py runserver 8080
```

创建应用

```
...\> py manage.py startapp polls
```

在创建应用里的`views.py`中创建视图，简例：

```python
# polls/views.py
from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")
```

然后在`urls.py`（没有则新创建）中建立一个URL映射，简例：

```python
# polls/urls.py
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
]
```

接着在**工程文件**下的`urls.py`中指定`polls.urls`模块

```python
# mysite/urls.py
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('polls/', include('polls.urls')),
    path('admin/', admin.site.urls),
]
```

### path函数

接收4个参数，两个必须参数：`route` 和 `view`，两个可选参数：`kwargs` 和 `name`。

`route` 是一个匹配 URL 的准则（类似正则表达式）。当 Django 响应一个请求时，它会从 `urlpatterns` 的第一项开始，依次匹配列表中的项，直到找到匹配的项。

`view`：当 Django 找到了一个匹配的准则，就会调用这个特定的视图函数，并传入一个 `HttpRequest` 对象作为第一个参数，被“捕获”的参数以关键字参数的形式传入

`kwargs`：任意个关键字参数可以作为一个字典传递给目标视图函数

`name`：使你的 URL 取名能让你在 Django 的任意地方唯一地引用它

# Second Part

设置时区：在工程文件下的`settings.py`内找到`TIME_ZONE`，改为自己的时区。

建立数据表：

```
...\> py manage.py migrate
```

### 建立模型

在创建应用内的`models.py`中创建的类即可视为模型，简例：

```python
# polls/models.py
from django.db import models


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
```

### 激活模型

在工程文件下的`settings.py`中的`INSTALLED_APPS`中添加我们创建的应用，简例：

```python
# mysite/setting.py
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # My Apps
    'polls.apps.PollsConfig',
]
```

然后在终端中运行命令

```
...\> py manage.py makemigrations polls
```

它会将创建的模型存储在我们创建应用目录下的`migrations/0001_initial.py`中

查看迁移过程中的SQL语句

```
...\> py manage.py sqlmigrate polls 0001
```

- 数据库的表名是由应用名(`polls`)和模型名的小写形式( `question` 和 `choice`)连接而来。
- 主键(IDs)会被自动创建。
- 默认的，Django 会在外键字段名后追加字符串 `"_id"` 。
- 外键关系由 `FOREIGN KEY` 生成。
- `sqlmigrate` 命令并没有真正在数据库中的执行迁移 ，它只是把命令输出到屏幕上，让你看看 Django 认为需要执行哪些 SQL 语句。

自动执行数据库迁移并同步管理数据库结构的命令`migrate`

```
...\> py manage.py migrate
```

改变模型的三个步骤：

- 编辑 `models.py` 文件，改变模型。
- 运行 `python manage.py makemigrations`为模型的改变生成迁移文件。
- 运行 `python manage.py migrate` 来应用数据库迁移。

### API

进入python命令行

```
...\> py manage.py shell
```

```python
# Import the model classes we just wrote.
>>> from polls.models import Choice, Question  

# No questions are in the system yet.
>>> Question.objects.all()
<QuerySet []>

# Create a new Question.
# Support for time zones is enabled in the default settings file, so
# Django expects a datetime with tzinfo for pub_date. Use timezone.now()
# instead of datetime.datetime.now() and it will do the right thing.
>>> from django.utils import timezone
>>> q = Question(question_text="What's new?", pub_date=timezone.now())

# Save the object into the database. You have to call save() explicitly.
>>> q.save()

# Now it has an ID.
>>> q.id
1

# Access model field values via Python attributes.
>>> q.question_text
"What's new?"
>>> q.pub_date
datetime.datetime(2012, 2, 26, 13, 0, 0, 775217, tzinfo=<UTC>)

# Change values by changing the attributes, then calling save().
>>> q.question_text = "What's up?"
>>> q.save()

# objects.all() displays all the questions in the database.
>>> Question.objects.all()
<QuerySet [<Question: Question object (1)>]>
```

在模型中添加`__str__()`方法，也可以再添加自定义方法：

```python
# polls/models.py
from django.db import models
import datetime
from django.utils import timezone


# Create your models here.
class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    
    def __str__(self):
        return self.question_text
    
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    
    def __str__(self):
        return self.choice_text
```

再次打开`shell`

```python
>>> from polls.models import Choice, Question

# Make sure our __str__() addition worked.
>>> Question.objects.all()
<QuerySet [<Question: What's up?>]>

# Django provides a rich database lookup API that's entirely driven by
# keyword arguments.
>>> Question.objects.filter(id=1)
<QuerySet [<Question: What's up?>]>
>>> Question.objects.filter(question_text__startswith='What')
<QuerySet [<Question: What's up?>]>

# Get the question that was published this year.
>>> from django.utils import timezone
>>> current_year = timezone.now().year
>>> Question.objects.get(pub_date__year=current_year)
<Question: What's up?>

# Request an ID that doesn't exist, this will raise an exception.
>>> Question.objects.get(id=2)
Traceback (most recent call last):
    ...
DoesNotExist: Question matching query does not exist.

# Lookup by a primary key is the most common case, so Django provides a
# shortcut for primary-key exact lookups.
# The following is identical to Question.objects.get(id=1).
>>> Question.objects.get(pk=1)
<Question: What's up?>

# Make sure our custom method worked.
>>> q = Question.objects.get(pk=1)
>>> q.was_published_recently()
True

# Give the Question a couple of Choices. The create call constructs a new
# Choice object, does the INSERT statement, adds the choice to the set
# of available choices and returns the new Choice object. Django creates
# a set to hold the "other side" of a ForeignKey relation
# (e.g. a question's choice) which can be accessed via the API.
>>> q = Question.objects.get(pk=1)

# Display any choices from the related object set -- none so far.
>>> q.choice_set.all()
<QuerySet []>

# Create three choices.
>>> q.choice_set.create(choice_text='Not much', votes=0)
<Choice: Not much>
>>> q.choice_set.create(choice_text='The sky', votes=0)
<Choice: The sky>
>>> c = q.choice_set.create(choice_text='Just hacking again', votes=0)

# Choice objects have API access to their related Question objects.
>>> c.question
<Question: What's up?>

# And vice versa: Question objects get access to Choice objects.
>>> q.choice_set.all()
<QuerySet [<Choice: Not much>, <Choice: The sky>, <Choice: Just hacking again>]>
>>> q.choice_set.count()
3

# The API automatically follows relationships as far as you need.
# Use double underscores to separate relationships.
# This works as many levels deep as you want; there's no limit.
# Find all Choices for any question whose pub_date is in this year
# (reusing the 'current_year' variable we created above).
>>> Choice.objects.filter(question__pub_date__year=current_year)
<QuerySet [<Choice: Not much>, <Choice: The sky>, <Choice: Just hacking again>]>

# Let's delete one of the choices. Use delete() for that.
>>> c = q.choice_set.filter(choice_text__startswith='Just hacking')
>>> c.delete()
```

### Django管理

创建管理员账号

```
...\> py manage.py createsuperuser
```

在应用下的`admin.py`中添加后台接口

```python
# polls/admin.py
from django.contrib import admin
from .models import Question


# Register your models here.
admin.site.register(Question)
```

# Third Part

丰富原有的视图，在应用下的`views.py`中添加视图

```python
# polls/views.py
def detail(request, question_id):
    return HttpResponse("You're looking at question %s." % question_id)

def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)

def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)
```

映射到URL，即在应用下的`urls.py`中的`urlpatterns`中添加函数调用

```python
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:question_id>/', views.detail, name='detail'),
    path('<int:question_id>/results/', views.results, name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
]
```

`<int:question_id>`可以匹配用户的相应请求，并将整形的`question_id`参数传递给匹配成功的函数

### 写一个有用的视图

在视图中显示目标内容，修改应用下`views.py`中的内容

```python
# polls/views.py
from .models import Question

def index(request):
    latest_question_list = Question.objects.order_by('pub_date')[:5]
    output = ', '.join(q.question_text for q in latest_question_list)
    return HttpResponse(output)
```

用HTML文件来展示视图

在应用内创建一个`templates`目录，在该目录下再创建一个与应用名相同的子目录，再在该子目录下创建HTML文件

```html
<!--polls/templates/polls/index.html-->
{% if lastest_question_list %}
    <ul>
    {%  for question in latest_question_list %}
        <li>
            <a href="/polls/{{ question.id }}/">{{ question.question_text }}</a>
        </li>
    {% endfor %}
    </ul>
{% endif %}
```

在应用下的`views.py`中来使用模板

```python
from django.template import loader

def index(request):
    latest_question_list = Question.objects.order_by('pub_date')[:5]
    template = loader.get_template('polls/index.html')
    context = {
        'lastest_question_list': latest_question_list,
    }
    return HttpResponse(template.render(context, request))
```

用`render()`简化渲染操作

在应用下的`views.py`中来使用该函数

```python
from django.shortcuts import render
from .models import Question


def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)
```

#### 抛出404错误

在应用下的`views.py`中：

```python
from django.http import Http404

def detail(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request, 'polls/detail.html', {'question': question})
```

需要创建相应的`detail.html`文件

用`get_object_or_404()`函数简化操作

```python
from django.shortcuts import get_object_or_404, render

from .models import Question
# ...
def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})
```

`detail.html`

```python
<h1>{{ question.question_text }}</h1>
<ul>
{% for choice in question.choice_set.all %}
    <li>{{ choice.choice_text }}</li>
{% endfor %}
</ul>
```

修改`index.html`

```html
<li><a href="/polls/{{ question.id }}/">{{question.question_text }}</a></li>
```

$\rightarrow$

```html
<li><a href="{% url 'detail' question.id %}">{{ question.question_text }}</a></li>
```

添加命名空间，修改应用下的`urls.py`文件

```python
app_name = 'polls'
urlpatters =  ...
```

再接着修改html网页

```html
<!--index.html-->
<li><a href="{% url 'detail' question.id %}">{{question.question_text }}</a></li>
```

$\rightarrow$

```html
<li><a href="{% url 'polls:detail' question.id %}">{{ question.question_text }}</a></li>
```

# Fourth Part

创建一个实用的表单

```html
<h1>{{ question.question_text }}</h1>
{% if error_message %}
    <p><strong>{{ error_message }}</strong></p>
{% endif %}
<form action="{% url 'polls:vote' question.id %}" method="post">
    {% csrf_token %}
    {% for choice in question.choice_set.all %}
    <input type="radio" name="choice" id="choice{{ forloop.counter }}" value="{{ choice.id }}">
    <label for="choice{{ forloop.counter }}">{{ choice.choice_text }}</label><br>
    {% endfor %}
<input type="submit" value="Vote">
</form>
```

所有针对内部 URL 的 POST 表单都应该使用 `{% csrf_token %}`模板标签。

完善`vote()`函数

```python
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
```

完善`results`视图

```python
def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})
```

建立`results.html`：

```html
<h1>{{ question.question_text }}</h1>

<ul>
    {% for choice in question.choice_set.all %}
        <li>{{ choice.choice_text }} -- {{ choice.votes }} vote{{ choice.votes|pluralize }}</li>
    {% endfor %}
</ul>
<a href="{% url 'polls:detail' question.id %}">Vote again?</a>
```

### 改良之前的代码：

应用下的`urls.py`

```python
from django.urls import path

from . import views

app_name = 'polls'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
]
```

修改应用下的`views.py`文件

```python
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

from .models import Choice, Question


class IndexView(generic.ListView):
    template_name = 'polls/index.html'  # 指定名称
    context_object_name = 'latest_question_list'  # 自己指定context的名字， 而非默认的question_list

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
    ... # same as above, no changes needed.
```


