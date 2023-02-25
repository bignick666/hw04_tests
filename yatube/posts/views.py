from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, \
    redirect

from django.contrib.auth.decorators import login_required

from .models import Group, Post, User, Comment, Follow

from .forms import PostForm, CommentForm
from .utils import get_pag


def index(request):
    context = get_pag(Post.objects.all(), request)
    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = group.post.all()
    context = {
        'group': group,
        'posts': posts,
    }
    context.update(get_pag(group.post.all(), request))
    return render(request, 'posts/group_list.html', context)


def profile(request, username):
    author = get_object_or_404(User, username=username)
    following = False
    if request.user.is_authenticated:
        following = Follow.objects.filter(
            user=request.user,
            author=author
        ).exists()
    context = {
        'author': author,
        'following': following
    }
    context.update(get_pag(author.post.all(), request))
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    form = CommentForm(request.POST or None)
    comment = Comment.objects.filter(post=post)
    author_posts_count = Post.objects.filter(author=post.author)
    return render(request, 'posts/post_detail.html', {
        'post': post,
        'author_posts_count': author_posts_count,
        'form': form,
        'comments': comment
    })


@login_required
def post_create(request):
    form = PostForm(request.POST or None,
                    files=request.FILES or None
                    )
    if form.is_valid():
        new_post = form.save(commit=False)
        new_post.author = request.user
        new_post.save()
        return redirect('posts:profile', username=request.user)
    return render(request, 'posts/create.html', {'form': form})


@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.author == request.user:
        if request.method == 'POST':
            form = PostForm(request.POST,
                            files=request.FILES,
                            instance=post)
            if form.is_valid():
                form.save()
                return redirect('posts:post_detail',
                                post_id=post_id
                                )
            else:
                raise ValueError
        else:
            form = PostForm(instance=post)
            return render(request,
                          'posts/create.html',
                          {'form': form, 'is_edit': True})
    else:
        return redirect('posts:post_detail', post_id=post_id)


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect('posts:post_detail', post_id=post_id)


@login_required
def follow_index(request):
    posts = Post.objects.filter(author__following__user=request.user)
    follow = True
    context = {
        'posts': posts,
        'follow': follow
    }
    context.update(get_pag(posts.all(), request))
    return render(request, 'posts/follow.html', context)


@login_required
def profile_follow(request, username):
    author = get_object_or_404(User, username=username)
    if (
            author != request.user
            and not Follow.objects.filter(user=request.user,
                                          author=author).exists()
    ):
        Follow.objects.create(user=request.user, author=author)
        return redirect('posts:profile', username)
    return redirect('posts:profile', username)


@login_required
def profile_unfollow(request, username):
    author = get_object_or_404(User, username=username)
    Follow.objects.filter(user=request.user, author=author).delete()
    return redirect("posts:profile", username)
