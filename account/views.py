from django.urls import reverse
from .forms import UserRegistrationForm, UserEditForm, ProfileEditForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.contrib import messages
from blog.models import Post
from .models import Profile
from django.views import generic
from django.contrib.auth.models import User


def register_user(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password1'])
            new_user.save()
            Profile.objects.create(user=new_user)
            context = {'new_user': new_user}
            return render(request, 'account/register_done.html', context)
    else:
        user_form = UserRegistrationForm()

    context = {'user_form': user_form}
    return render(request, 'account/register.html', context)


@login_required
def dashboard(request):
    return render(request, 'account/dashboard.html', {})


@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)

        if profile_form.is_valid() and user_form.is_valid():
            profile_form.save() and user_form.save()
            messages.success(request, "Your profile has been successfully updated")
        else:
            messages.error(request, "There was an error updating your profile, try again")
        return redirect(reverse('account:dashboard'))

    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)

    context = {'user_form': user_form, 'profile_form': profile_form}
    return render(request, 'account/edit.html', context)


class DeleteView(generic.DeleteView):
    model = User
    template_name = 'blog/delete.html'
    success_url = '/blog'


@login_required
def post_manager(request):
    published_posts = Post.published.filter(author=request.user)
    draft_posts = Post.draft.filter(author=request.user)
    return render(request, 'blog/post/post_manager.html',
                  {'published_posts': published_posts, 'draft_posts': draft_posts})
