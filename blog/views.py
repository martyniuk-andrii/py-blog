from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.views import generic

from blog.models import Post, Commentary
from .forms import CommentForm


def index(request: HttpRequest) -> HttpResponse:
    posts = Post.objects.all().order_by("-created_time")

    paginator = Paginator(posts, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {"post_list": page_obj.object_list, "page_obj": page_obj}

    return render(request, "blog/index.html", context=context)


class PostDetailView(generic.DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = CommentForm()
        return context


class CommentCreateView(LoginRequiredMixin, generic.CreateView):
    model = Commentary
    form_class = CommentForm

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.user = self.request.user
        comment.post_id = self.kwargs["pk"]
        comment.save()

        return redirect("blog:post-detail", pk=self.kwargs["pk"])
