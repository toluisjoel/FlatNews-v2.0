from django.views.generic.edit import  DeleteView, UpdateView, CreateView
from  django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView
from django.utils.text import slugify
from django.urls import reverse_lazy
from django.db.models import Count
from .models import Post, Comment
from .forms import CommentForm


class CreatePostView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ('title', 'body', 'thumbnail', 'tags','status',)
    template_name = 'blog/post/create_post.html'
    success_url = reverse_lazy('account:post_manager')

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.slug = slugify(form.instance.title)
        return super().form_valid(form)


class PostListView(ListView):
    model = Post
    object_list = Post.published.all()
    template_name = 'blog/post/post_list.html'


@login_required
def post_detail(request, published_date, slug, pk):
    post = get_object_or_404(Post, published_date=published_date, slug=slug, id=pk)
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

    context = {'post': post, 'comment_form': comment_form, 'new_comment': new_comment, 'comments': comments,'similar_posts': similar_posts}
    return render(request, 'blog/post/post_detail.html', context)


class EditPostView(LoginRequiredMixin, UpdateView):
    model = Post
    fields = ('title', 'body', 'thumbnail', 'tags','status',)
    template_name = 'blog/edit.html'
    success_url = reverse_lazy('account:dashboard')


class DeletePostView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'blog/delete.html'
    success_url = reverse_lazy('account:post_manager')


# comment views
class EditCommentView(UpdateView):
    model = Comment
    fields = ('body',)
    template_name = 'blog/edit.html'
    success_url = reverse_lazy('blog:home')


class DeleteCommentView(DeleteView):
    model = Comment
    template_name = 'blog/delete.html'
    success_url = reverse_lazy('blog:home')
