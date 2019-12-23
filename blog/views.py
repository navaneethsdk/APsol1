from django.shortcuts import render,get_object_or_404
from .models import Posts,Comment
from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView,DeleteView
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect,HttpResponse

# Create your views here.


def home(request):
    return render(request,'blog/home.html', context={'posts': Posts.objects.all()})


def about(request):
    return render(request, 'blog/about.html', {'title':'about'})


def like_post(request):
    post = get_object_or_404(Posts, id=request.POST.get('post_id'))
    is_liked = False
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        is_liked = True
    else:
        post.likes.add(request.user)
        is_liked=True
    return HttpResponseRedirect(post.get_absolute_url())


def post_detail(request,id):
    post = get_object_or_404(Posts, id=id)
    comment = Comment.objects.filter(post=post,reply=None).order_by('-id')
    is_liked = False
    if post.likes.filter(id=request.user.id).exists():
        is_liked = True

    if request.method == 'POST':
        comment_form = CommentForm(request.POST or None)
        if comment_form.is_valid():
            content = request.POST.get('content')
            reply_id = request.POST.get('comment_id')
            comment_qs = None
            if reply_id:
                comment_qs = Comment.objects.get(id=reply_id)
            comment = Comment.objects.create(post=post,user= request.user,content=content,reply= comment_qs)
            comment.save()
            return HttpResponseRedirect(post.get_absolute_url())
    else:
        comment_form = CommentForm()


    context = {
        'post': post,
        'is_liked': is_liked,
        'total_likes': post.total_likes(),
        'comments': comment,
        'comment_form': comment_form
    }
    return render(request, 'blog/posts_detail.html',context)


class ListPostView(ListView):
    model = Posts
    template_name = 'blog/home.html'  # default: <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date']
    paginate_by = 5


class UserListPostView(ListView):
    model = Posts
    template_name = 'blog/user_post.html'  # default: <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Posts.objects.filter(author=user).order_by('-date')


class DetailPostView(DetailView):
    model = Posts


class CreatePostView(LoginRequiredMixin, CreateView):
    model = Posts
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    # success_url = 'blog-home' to get redirected to home after creating a post


class UpdatePostView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Posts
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class DeletePostView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Posts
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class CommentForm(forms.ModelForm):
    content = forms.CharField(label="",widget=forms.Textarea(attrs={'class':'form-control','placeholder':'Text goes here..','rows':'4','cols':50}))
    class Meta:
        model = Comment
        fields = {'content',}

