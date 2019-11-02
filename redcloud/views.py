from django.shortcuts import render
from django.views.generic import ListView,DetailView, CreateView, UpdateView, DeleteView, RedirectView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Post
from .models import Comment
from .forms import CommentForm
from django.views.generic.edit import FormMixin
from django.shortcuts import get_object_or_404
from taggit.models import Tag

def landingpage(request):
    return render(request, 'redcloud/firstview.html')

def home(request, tag_slug = None):
    posts = Post.objects.all()
    tagz = Post.tags.all()

    if tag_slug:
        tagz = get_object_or_404(Tag, slug = tag_slug)
        posts = posts.filter(tags__in = [tagz])

    context = {'posts': posts,'tagz': tagz}
    return render(request, 'redcloud/home.html', context)

def firstview(request):
    return render(request, 'redcloud/first.html')


class PostListView(ListView):
    model = Post
    template_name = 'redcloud/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    def get_context_data(self, **kwargs):
        context = super(PostListView, self).get_context_data(**kwargs)
        context['posts'] = Post.objects.all()
        context['tagz'] = Post.tags.all()
        return context
"""
def post_detail(request, pk):
    post = get_object_or_404(Post, pk= pk)
    context = { 'object': post}
    return render(request, 'redcloud/post_detail.html', context)
"""
class PostDetailView(FormMixin, DetailView):
    model = Post
    form_class = CommentForm
    success_url = '/home'
    def get_succes_url(self):
        the_pk = self.object.pk
        print('------------------------')
        print(the_pk)
        return reverse('post-detail', kwargs = {'pk':self.object.pk})

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        context['form'] = CommentForm(initial={'post': self.object})
        context['comments']= self.object.comments.filter(active = True)
        return context

    def post(self, request, *args, **kwargs):
        self.the_post= self.get_object()
        print(self.the_post.comments.count())
        form = self.get_form()
        if form.is_valid():
            #form.instance.commentor = self.request.user
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
    def form_valid(self, form):
        #new_comment = None
        self.object=form.save(commit=False)
        #print(type(self.object))
        self.object.commentor = self.request.user
        self.object.post = self.the_post
        self.object = form.save()
        return super().form_valid(form)
"""class LikeRedirectView(RedirectView):

    permanent = False
    query_string = True
    pattern_name = 'article-detail'

    def get_redirect_url(self, *args, **kwargs):
        article = get_object_or_404(Post, pk=kwargs['pk'])
        print(article)
        return super().get_redirect_url(*args, **kwargs) """
class PostLikeToggle(RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        obj  = get_object_or_404(Post, pk=kwargs['pk'])

        user = self.request.user
        print(user)
        if user.is_authenticated:
            if user in obj.likes.all():
                obj.likes.remove(user)
            else:
                obj.likes.add(user)
        return obj.get_absolute_url()

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content', 'image']
    def form_valid(self, form):
        #overwriting the form_valid method to make the author of the post to be the user that sends the post request on the form
        form.instance.author = self.request.user
        #after obtaining tha author of the post...run the form_valid method on the parent class
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title','content']
    def form_valid(self, form):
        #overwriting the form_valid method to make the author of the post to be the user that sends the post request on the form
        form.instance.author = self.request.user
        #after obtaining tha author of the post...run the form_valid method on the parent class
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        else:
            return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        else:
            return False


def about(request):
    return render(request,'redcloud/about.html')


