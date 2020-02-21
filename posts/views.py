from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.core.paginator import Paginator
import datetime as dt

from .models import Post, User, Group
from .forms import PostForm


def index(request):
    post_list = Post.objects.order_by('-pub_date').all()
    paginator = Paginator(post_list, 10) #change number of shown posts if necessary
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, "index.html", {"page": page, "paginator": paginator})


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = Post.objects.filter(group=group).order_by("-pub_date")
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, "group.html", {"page": page, "paginator": paginator, "group": group})


@login_required
def new_post(request):
    title = 'Создать новую запись'
    submit = 'Добавить'
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.author = request.user
            new_post.save()
            return redirect('index')
            #return redirect('post', username=new_post.author.username, post_id=new_post.id)
    form = PostForm()
    return render(request, 'post_new.html', {'form': form, 'title': title, 'submit': submit})


def profile(request, username):
    profile = get_object_or_404(User, username=username)
    post_list = Post.objects.filter(author=profile.id).order_by("-pub_date")
    paginator = Paginator(post_list, 10) #change number of shown posts if necessary
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'profile.html', {'profile': profile, 'written_posts': post_list.count(), "page": page, "paginator": paginator})


def post_view(request, username, post_id):
    profile = get_object_or_404(User, username=username)
    post = get_object_or_404(Post, pk=post_id, author=profile.id)
    written_posts = Post.objects.filter(author=profile.id).count()
    return render(request, 'post.html', {'post': post, 'profile': profile, 'written_posts': written_posts,})


@login_required
def post_edit(request, username, post_id):

    if request.user.username != username:
        return redirect('post', username=username, post_id=post_id)

    post = get_object_or_404(Post, pk=post_id)
    title = 'Редактировать запись'
    submit = 'Сохранить'

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.pub_date = dt.datetime.today()
            new_post.save()
            return redirect('post', username=username, post_id=post_id)
    form = PostForm(instance=post)
    return render(request, 'post_new.html', {'form': form, 'title': title, 'submit': submit, 'post': post})


@login_required
def post_delete(request, username, post_id):
    if request.user.username != username:
        return redirect('post', username=username, post_id=post_id)

    profile = get_object_or_404(User, username=username)
    post = get_object_or_404(Post, pk=post_id, author=profile.id)
    if request.method == 'POST':
        post.delete()
        return redirect('profile', username=username)
    return render(request, 'post_delete.html', {'post': post, 'profile': profile})
