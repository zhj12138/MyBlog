from django.db import models


# Create your models here.
class Article(models.Model):
    pub_date = models.DateTimeField()
    mod_date = models.DateTimeField()
    title = models.CharField(max_length=128)
    outline = models.CharField(max_length=512)
    file = models.FileField(upload_to='mdFiles')
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)

    def __str__(self):
        return self.title


class Category(models.Model):
    name = models.CharField(max_length=128)
    articles = models.ManyToManyField(Article)
    article_num = models.IntegerField(default=0)
    cre_date = models.DateTimeField()
    mod_data = models.DateTimeField()
    brief_introduction = models.TextField()
    total_views = models.IntegerField()
    total_likes = models.IntegerField()

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=128)
    articles = models.ManyToManyField(Article)
    article_num = models.IntegerField(default=0)
    total_views = models.IntegerField(default=0)
    total_likes = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Link(models.Model):
    name = models.CharField(max_length=128)
    url = models.URLField()

    def __str__(self):
        return self.name


class Me(models.Model):
    name = models.CharField(max_length=128)
    email = models.EmailField()
    brief_introduction = models.TextField()
    interests = models.CharField(max_length=128)
    school = models.CharField(max_length=128)
    company = models.CharField(max_length=128)
    address = models.CharField(max_length=128)

    def __str__(self):
        return self.name

