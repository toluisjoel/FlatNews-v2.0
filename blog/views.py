from django.contrib.postgres.search import SearchHeadline, SearchVector, SearchQuery
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from .forms import PostForm, CommentForm
from django.utils.text import slugify
from django.contrib import messages
from django.db.models import Count
from .models import Post, Comment
from django.urls import reverse
from taggit.models import Tag


def home(request, tag_slug=None):
    object_list = Post.published.all()

    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])

        context = {'tag': tag, 'object_list': object_list}
        return render(request, 'blog/post/tags_by_id.html', context)

    paginator = Paginator(object_list, 12)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    query = request.GET.get('query')
    if query:
        # object_list = Post.published.filter(title__icontains=query)
        # object_list = Post.published.annotate(search=SearchVector('title', 'body')).filter(search=SearchQuery(query))
        object_list = Post.published.annotate(headline=SearchHeadline('body', SearchQuery(query), start_sel='<b><u><em><i>', stop_sel='</i></em></u></b>'))

    context = {'posts': posts, 'page': page, 'tag': tag, 'queryset': object_list}
    return render(request, 'blog/post/post_list.html', context)


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post, published_date__year=year, published_date__month=month, published_date__day=day)

    comments = post.comments.filter(active=True)
    new_comment = None
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.author = request.user
            new_comment.post = post
            new_comment.save()
    else:
        comment_form = CommentForm()

    # list of similar posts
    post_tags_id = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_id).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-tags', '-published_date')[:6]

    context = {'post': post, 'comment_form': comment_form, 'new_comment': new_comment, 'comments': comments,
               'similar_posts': similar_posts}
    return render(request, 'blog/post/post_detail.html', context)


@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.author = request.user
            form.instance.slug = slugify(form.instance.title)
            form.save()
            messages.info(request,'Your post might be taken down if it doesn\'t meet our community standards. You fit do am comrade, mafo 🙂')
            return redirect(reverse('blog:post_detail',args=[form.instance.published_date.year, form.instance.published_date.month, form.instance.published_date.day, form.instance.slug]))
    else:
        form = PostForm()

    context = {'form': form}
    return render(request, 'blog/post/create_post.html', context)


def edit_post(request, pk):
    post = Post.objects.get(id=pk)
    form = PostForm(instance=post)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            #form.instance.thumbnail = 
            form.save()
            messages.success(request, 'Your post has been updated')
            return redirect(reverse('account:dashboard'))
    
    context = {'form': form, 'title': 'post'}
    return render(request, 'blog/edit.html', context)


def delete_post(request, pk):
    post = Post.objects.get(id=pk)
    if request.method == 'POST':
        post.delete()
        return redirect(reverse('account:dashboard'))
    
    context = {'title': 'post'}
    return render(request, 'blog/delete.html', context)


# comment views
def edit_comment(request, pk):
    comment = Comment.objects.get(id=pk)
    form = CommentForm(instance=comment)
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your comment has been updated, go back')

    context = {'form': form, 'title': 'comment'}
    return render(request, 'blog/edit.html', context)


def delete_comment(request, pk):
    comment = Comment.objects.get(id=pk)
    if request.method == 'POST':
        comment.delete()

    context = {'title': 'comment'}
    return render(request, 'blog/delete.html', context)

# search
def search(request):
    qs = Post.published.all()
    query = request.GET.get('query')
    if query:
        qs = Post.published.filter(title__icontains=query)
        qs = Post.published.annotate(search=SearchVector('title', 'body')).filter(search=SearchQuery(query))
        return render(request, 'main.html', {'queryset': qs})

def error_404(request, exception):
    data = {}
    return render(request, 'blog/404.html', data)