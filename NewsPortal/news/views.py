from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post
from .filters import PostFilter
from .forms import PostForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

class PostsList(ListView):
    model = Post
    ordering = '-datetime_in'
    template_name = 'news.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class PostsDetail(DetailView):
    model = Post
    template_name = 'news_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class PostsSearch(PostsList):
    template_name = 'news_search.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context

class NewsCreate(PermissionRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    template_name = 'post_create.html'
    permission_required = ('news.add_post')

    def form_valid(self, form):
        post = form.save(commit=False)
        post.type = Post.news
        return super().form_valid(form)

class NewsUpdate(PermissionRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'post_create.html'
    permission_required = ('news.change_post')

    def form_valid(self, form):
        post = form.save(commit=False)
        post.type = Post.news
        return super().form_valid(form)

class ArticlesCreate(PermissionRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    template_name = 'post_create.html'
    permission_required = ('news.add_post')

    def form_valid(self, form):
        post = form.save(commit=False)
        post.type = Post.article
        return super().form_valid(form)

class ArticlesUpdate(PermissionRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'post_create.html'
    permission_required = ('news.change_post')

    def form_valid(self, form):
        post = form.save(commit=False)
        post.type = Post.article
        return super().form_valid(form)

class PostDelete(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')
