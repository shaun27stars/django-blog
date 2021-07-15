from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import ListView
from django.views import View
from .models import Post
from .forms import CommentForm
# class-based views


class PostListView(ListView):
    model = Post
    template_name = "blog/posts.html"
    ordering = ['-date']
    context_object_name = 'posts'


class PostIndexView(PostListView):
    template_name = 'blog/index.html'

    def get_queryset(self):
        return super().get_queryset()[:3]


class PostDetailView(View):
    model = Post
    template_name = 'blog/post_detail.html'

    def render_context(self, request, post, comment_form):
        saved_for_later = post.slug in request.session.get("saved-posts", [])
        return render(request, "blog/post-detail.html", {
            "post": post,
            "comment_form": comment_form,
            "saved_for_later": saved_for_later
        })

    def get(self, request, slug):
        post = Post.objects.get(slug=slug)
        return self.render_context(request, post, CommentForm())

    def post(self, request, slug):
        post = Post.objects.get(slug=slug)
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            # Have to update the related model with non-form info
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect(reverse('post-detail', args=[slug]))
        return self.render_context(request, post, comment_form)


class SavedPostsView(View):
    def get(self, request):
        saved_slugs = request.session.get("saved-posts", [])
        posts = Post.objects.filter(slug__in=saved_slugs)
        print(saved_slugs)
        return render(request, "blog/saved-posts.html", {
            "posts": posts
        })

    def post(self, request):
        saved_posts = request.session.get("saved-posts", [])
        slug = request.POST.get("post_slug")
        if slug not in saved_posts:
            saved_posts.append(slug)
        else:
            saved_posts.remove(slug)
        request.session["saved-posts"] = saved_posts
        return redirect(reverse("index"))


# # function-based views
# def index(request):
#     latest_posts = Post.objects.order_by('-date')[:3]
#     return render(request, 'blog/index.html', {"posts": latest_posts})


# def posts(request):
#     return render(request, 'blog/posts.html', {"posts": Post.objects.order_by('-date')})


# def post_detail(request, slug):
#     post = get_object_or_404(Post, slug=slug)
#     return render(request, 'blog/post_detail.html', {"post": post})
