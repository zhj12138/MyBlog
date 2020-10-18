from django.shortcuts import render
from django.views.generic import DetailView, ListView
from django.views import View


# Create your views here.
class IndexView(View):
    pass

    def get(self, request):
        return render(request, 'blogapp/index.html')


class AboutView(DetailView):
    pass


class ArticleView(View):
    pass


class CategoryView(ListView):
    pass


class DetailCategoryView(ListView):
    pass


class TagView(ListView):
    pass


class DetailTagView(ListView):
    pass


class ArchiveView(ListView):
    pass


class LinkView(ListView):
    pass
