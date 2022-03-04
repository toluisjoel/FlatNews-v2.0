from .models import Post, Comment
from django import forms
from tinymce.widgets import TinyMCE

class TinyMCEWidget(TinyMCE):
    def use_required_attribute(self, *args):
        return False


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'body', 'thumbnail', 'tags','status',)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)
        widgets = {
            'body': forms.Textarea(attrs={'placeholder': 'Your Message'}),
        }
