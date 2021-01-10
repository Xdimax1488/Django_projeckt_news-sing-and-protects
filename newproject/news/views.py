from django.shortcuts import render
from django.core.paginator import Paginator
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from .models import *
from .filters import NewsFilter
from .forms import PostForm


class NewsList(ListView):
    model = Post
    template_name = 'News.html'
    context_object_name = 'News'
    ordering = ['-datetime']
    paginate_by = 1
    form_class = PostForm


class NewsDetail(DetailView):
    model = Post
    template_name = 'New.html'
    context_object_name = 'New'
    queryset = Post.objects.all()


class PostSearch(ListView):
    model = Post
    template_name = 'search.html'
    context_object_name = 'search'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = NewsFilter(self.request.GET, queryset=self.get_queryset())
        return context


class PostCreate(PermissionRequiredMixin,CreateView):
    model = Post
    template_name = 'post_create.html'
    form_class = PostForm
    permission_required = ('News.add_post', 'News.view_post')


class PostUpdateView(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    model = Post
    template_name = 'post_edit.html'
    form_class = PostForm
    login_url = 'login/'
    redirect_file_name = '/'
    permission_required = ('News.change_post', 'News.view_post')


class PostDeleteView(PermissionRequiredMixin, DeleteView):
    model = Post
    template_name = 'post_delete.html'
    queryset = Post.objects.all()
    success_url = '/News/'
    permission_required = ['News.delete_post', 'News.view_post']
