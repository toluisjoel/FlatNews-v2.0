from  django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.text import slugify
from .models import Post, Comment
from django.urls import reverse_lazy
from django.views.generic.edit import  DeleteView, UpdateView, CreateView
from django.views.generic import DetailView, ListView
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


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post/post_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(body=self.object)
        context['form'] = CommentForm()
        return context


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
