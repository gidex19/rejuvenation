from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import UserRegistrationForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from django.views.generic import View, RedirectView
from .models import UserFollowers
from django.shortcuts import get_object_or_404
from redcloud.models import Post


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')

    else:
        form = UserRegistrationForm()
    return render(request, 'users/register.html', {'form': form})
"""
def otherprofile(request, pk):
    post = get_object_or_404(Post, pk= pk)
    context = { 'post': post}
    return render(request, 'users/oprofile.html', context)
"""
class FollowToggle(RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        obj  = get_object_or_404(Post, pk=kwargs['pk'])
        visitor = self.request.user
        author = obj.author
        if visitor == author:
            print('you cant follow yourself')
            return obj.get_follow_url()
        else:

            user_follower, created = UserFollowers.objects.get_or_create(user=author)
            #b = user_follower.followers.filter(username = self.request.user )
            #print(user_follower)
            fol = user_follower.followers.all()
            #print(fol)
            #user_follower, created = UserFollowers.objects.get_or_create(user=author)
            if visitor in fol:
                following = True
                user_follower.followers.remove(visitor)
            else:
                following = False
                user_follower.followers.add(visitor)

            user_follower.count = user_follower.followers.count()
            user_follower.save()
            print(user_follower.followers.all())
            print(user_follower.count)
            return obj.get_follow_url()



@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your profile has been updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm( instance = request.user)
        p_form = ProfileUpdateForm( instance = request.user.profile)
    context ={'u_form':u_form, 'p_form':p_form}
    return render(request, 'users/profile.html', context)

