from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView, ListView
from django.views import View
from .models import Category, Tag, Article, Link, Me


# Create your views here.
class IndexView(View):

    def get(self, request, *args, **kwargs):
        context = {}
        allArticles = Article.objects.order_by('-mod_date')
        paginator = Paginator(allArticles, 5)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['page'] = page_obj
        context['showArticles'] = page_obj.object_list
        context['mostViewedArticles'] = Article.objects.order_by('-views')[:5]
        context['recentArticles'] = Article.objects.order_by('-pub_date')[:5]
        context['categories'] = Category.objects.all()
        context['tags'] = Tag.objects.all()
        context['links'] = Link.objects.all()
        return render(request, 'blogapp/index.html', context)


class AboutView(DetailView):
    model = Me
    context_object_name = 'me'
    template_name = 'blogapp/about.html'

    def get_object(self, queryset=None):
        me = Me.objects.all()[0]
        return me


class ArticleView(DetailView):
    model = Article
    context_object_name = 'article'
    template_name = 'blogapp/article.html'

    def get_object(self, queryset=None):
        slug = self.kwargs['article_name']
        article = get_object_or_404(Article, name_slug=slug)
        return article

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['now'] = "Hello world"
        return context


class CategoryView(ListView):
    model = Category
    context_object_name = 'categories'
    template_name = 'blogapp/categories.html'


class DetailCategoryView(ListView):
    model = Article
    context_object_name = 'articles'
    template_name = 'blogapp/detail_category.html'

    def get_queryset(self, **kwargs):
        cate = get_object_or_404(Category, name_slug=self.kwargs['category_name'])
        return super(DetailCategoryView, self).get_queryset().filter(category=cate)


class TagView(ListView):
    model = Tag
    context_object_name = 'tags'
    template_name = 'blogapp/tags.html'


class DetailTagView(ListView):
    model = Article
    context_object_name = 'articles'
    template_name = 'blogapp/detail_tag.html'

    def get_queryset(self, **kwargs):
        tag = get_object_or_404(Tag, name_slug=self.kwargs['tag_name'])
        return super(DetailTagView, self).get_queryset().filter(tag=tag)


class ArchiveView(ListView):
    model = Article
    context_object_name = 'articles'
    template_name = 'blogapp/archive.html'
    paginate_by = 20


class LinkView(ListView):
    model = Link
    context_object_name = 'links'
    template_name = 'blogapp/links.html'
    paginate_by = 10
