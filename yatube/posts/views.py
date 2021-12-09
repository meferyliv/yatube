from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from yatube.settings import PAG_VALUE
from .forms import CommentForm, PostForm
from .models import Follow, Group, Post


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
    author_following = author.following.all()
    following = False
    authors_list = []
    for names in author_following:
        authors = names.user
        authors_list.append(authors)
    if request.user in authors_list:
        following = True
    paginator = Paginator(posts, PAG_VALUE)
    page_nubmer = request.GET.get('page')
    page_obj = paginator.get_page(page_nubmer)
    context = {
        'author': author,
        'page_obj': page_obj,
        'following': following
    }
    template = 'posts/profile.html'
    return render(request, template, context)


def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    comments = post.comments.all()
    form = CommentForm()
    context = {
        'post': post,
        'post_id': post_id,
        'comments': comments,
        'form': form
    }
    template = 'posts/post_detail.html'
    return render(request, template, context)


@login_required
def post_create(request):
    template = 'posts/create_post.html'
    form = PostForm(request.POST or None, files=request.FILES or None,)
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
            form = PostForm(
                request.POST or None,
                files=request.FILES or None,
                instance=post_edit
            )
            if form.is_valid():
                form.save()
                return redirect('posts:post_detail', post_id)
        form = PostForm(instance=post_edit)
        template = 'posts/create_post.html'
        context = {"form": form, "is_edit": is_edit, 'post_id': post_id}
        return render(request, template, context)
    return redirect('posts:post_detail', post_id)


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect('posts:post_detail', post_id=post_id)


@login_required
def follow_index(request):
    list_post = Post.objects.filter(author__following__user=request.user).all()
    paginator = Paginator(list_post, PAG_VALUE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj
    }
    template = 'posts/follow.html'
    return render(request, template, context)


@login_required
def profile_follow(request, username):
    user = get_object_or_404(User, username=request.user)
    author = get_object_or_404(User, username=username)
    check_already_follow = Follow.objects.filter(user=user, author=author).count()
    if author == request.user or check_already_follow == 1:
        return redirect('posts:profile', username=username)
    Follow.objects.create(user=request.user, author=author)
    return redirect('posts:profile', username=username)


@login_required
def profile_unfollow(request, username):
    author = get_object_or_404(User, username=username)
    if author != request.user:
        Follow.objects.filter(user=request.user, author=author).delete()
    return redirect('posts:profile', username=username)
