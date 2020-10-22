from django.db import models


# Create your models here.
# from uuslug import slugify
from uuslug import slugify

from blogapp.convert import md2html, getOutline


class Article(models.Model):
    pub_date = models.DateTimeField(auto_now_add=True)
    mod_date = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=128, unique=True)
    outline = models.CharField(max_length=512, blank=True)
    file = models.FileField(upload_to='mdFiles')
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    name_slug = models.SlugField(unique=True, blank=True)
    image = models.ImageField(upload_to='img', blank=True)

    def save(self, *args, **kwargs):
        if not self.outline:
            self.outline = getOutline(self.file.read().decode('utf-8'))
        self.name_slug = slugify(self.title)
        super(Article, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    def getFileText(self):
        return md2html(self.file.read().decode('utf-8'))

    # def addLike(self):
    #     print('add like')
    #
    # def deleteLike(self):
    #     print('delete like')


class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)
    articles = models.ManyToManyField(Article)
    article_num = models.IntegerField(default=0)
    cre_date = models.DateTimeField(auto_now_add=True)
    mod_date = models.DateTimeField(auto_now=True)
    brief_introduction = models.TextField(blank=True)
    total_views = models.IntegerField(default=0)
    total_likes = models.IntegerField(default=0)
    name_slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        self.name_slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)
        self.article_num = len(self.articles.all())
        self.total_views = sum([article.views for article in self.articles.all()])
        self.total_likes = sum([article.likes for article in self.articles.all()])
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'categories'


class Tag(models.Model):
    name = models.CharField(max_length=128, unique=True)
    articles = models.ManyToManyField(Article)
    article_num = models.IntegerField(default=0)
    total_views = models.IntegerField(default=0)
    total_likes = models.IntegerField(default=0)
    name_slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        self.name_slug = slugify(self.name)
        super(Tag, self).save(*args, **kwargs)
        self.article_num = len(self.articles.all())
        self.total_views = sum([article.views for article in self.articles.all()])
        self.total_likes = sum([article.likes for article in self.articles.all()])
        super(Tag, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Link(models.Model):
    name = models.CharField(max_length=128, unique=True)
    url = models.URLField()
    brief_introduction = models.TextField(blank=True)
    name_slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        self.name_slug = slugify(self.name)
        super(Link, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Me(models.Model):
    name = models.CharField(max_length=128)
    email = models.EmailField()
    brief_introduction = models.TextField()
    interests = models.CharField(max_length=128, blank=True)
    school = models.CharField(max_length=128, blank=True)
    company = models.CharField(max_length=128, blank=True)
    address = models.CharField(max_length=128, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "We"

