from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from yatube.settings import PAG_VALUE
from .forms import PostForm
from .models import Group, Post


def index(request):
    posts = Post.objects.all()
    paginator = Paginator(posts, PAG_VALUE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
    }
    template = 'posts/index.html'
    return render(request, template, context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = Post.objects.filter(group=group).all()
    paginator = Paginator(posts, PAG_VALUE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        'group': group,
    }
    template = 'posts/group_list.html'
    return render(request, template, context)


def profile(request, username):
    author = get_object_or_404(User, username=username)
    posts = author.posts.all()
    paginator = Paginator(posts, PAG_VALUE)
    page_nubmer = request.GET.get('page')
    page_obj = paginator.get_page(page_nubmer)
    context = {
        'author': author,
        'page_obj': page_obj,
    }
    template = 'posts/profile.html'
    return render(request, template, context)


def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    context = {
        'post': post,
        'post_id': post_id
    }
    return render(request, 'posts/post_detail.html', context)


@login_required
def post_create(request):
    template = 'posts/create_post.html'
    form = PostForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        form.save()
        return redirect('posts:profile', post.author)
    return render(request, template, {'form': form})


@login_required
def post_edit(request, post_id):
    is_edit = True
    post_edit = get_object_or_404(Post, pk=post_id)
    if post_edit.author == request.user:
        if request.method == 'POST':
            form = PostForm(request.POST, instance=post_edit)
            if form.is_valid():
                form.save()
                return redirect('posts:post_detail', post_id)
        form = PostForm(instance=post_edit)
        template = 'posts/create_post.html'
        context = {"form": form, "is_edit": is_edit, 'post_id': post_id}
        return render(request, template, context)
    return redirect('posts:post_detail', post_id)
