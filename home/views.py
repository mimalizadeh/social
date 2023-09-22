from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.text import slugify
from django.views import View

from home.froms import PostCreateUpdateFrom, PostCreateForm
from home.models import Post
from django.contrib.auth.mixins import LoginRequiredMixin


class HomeView(View):
    def get(self, request):
        posts = Post.objects.all()
        return render(request, 'home/home.html', {'posts': posts})


class PostDetailView(View):
    def get(self, request, post_id, post_slug):
        post = get_object_or_404(Post, pk=post_id, slug=post_slug)
        return render(request, "home/detail.html", {'post': post})


class PostDeleteView(LoginRequiredMixin, View):
    def get(self, request, post_id):
        post = get_object_or_404(Post, pk=post_id)
        if post.user.id == request.user.id:
            post.delete()
            messages.success(request, "Post delete successfully", extra_tags="success")
        else:
            messages.error(request, "You can't delete this post", extra_tags='danger')
        return redirect('home:home')


class PostUpdateView(LoginRequiredMixin, View):
    form_class = PostCreateUpdateFrom

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.post_instance = None

    def setup(self, request, *args, **kwargs):
        self.post_instance = get_object_or_404(Post, pk=kwargs['post_id'])
        super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        post = self.post_instance
        if not post.user.id == request.user.id:
            messages.error(request, "You can't delete this Post")
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        post = self.post_instance
        form = self.form_class(instance=post)
        return render(request, 'home/update.html', {'form': form, 'post': post})

    def post(self, request, *args, **kwargs):
        post = self.post_instance
        form = self.form_class(request.POST, instance=post)
        if form.is_valid():
            new_post = form.save(commit=False)
            cd = form.cleaned_data
            new_post.slug = slugify(cd.get('body')[:30])
            new_post.save()
            messages.success(request, 'Post update success fully', extra_tags='success')
            return redirect('home:post_detail', post.id, post.slug)


class PostCreateView(LoginRequiredMixin, View):
    form_class = PostCreateForm

    def get(self, request):
        form = self.form_class
        return render(request, 'home/create.html', {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = request.user
            slug = slugify(cd['body'][:30])
            Post.objects.create(user=user, body=cd['body'], slug=slug)
            messages.success(request, "Post add successfully", extra_tags='success')
            return redirect('account:user_profile', request.user.id)

        return render(request, 'home/create.html', {'form': form})


class PostCreateViewTwo(LoginRequiredMixin, View):
    form_class = PostCreateUpdateFrom

    def get(self, request):
        form = self.form_class
        return render(request, 'home/create.html', {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            new_post = form.save(commit=False)
            new_post.slug = slugify(cd['body'][:30])
            new_post.user = request.user
            new_post.save()
            messages.success(request, 'Post add successfully', extra_tags='success')
            return redirect('home:post_detail', new_post.id, new_post.slug)

        return render(request, 'home/create.html', {'form': form})
