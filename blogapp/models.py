from django.db import models


# Create your models here.
class Article(models.Model):
    pass


class Category(models.Model):
    pass
    articles = models.ManyToManyField(Article)


class Tag(models.Model):
    pass
    articles = models.ManyToManyField(Article)


class Link(models.Model):
    pass


class Me(models.Model):
    pass

