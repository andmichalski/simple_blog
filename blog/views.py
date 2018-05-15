# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db.models import Count
from django.views.generic import View, ListView, DetailView, FormView, TemplateView
from .models import Post, Comment
from .forms import CommentForm
from django.views.generic.detail import SingleObjectMixin
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
# Create your views here.


class MainList(ListView):
    model = Post
    template_name = "blog/index.html"
    paginate_by = 10

    def get_queryset(self):
        queryset = Post.objects.annotate(num_comments=Count('comment'))
        return queryset

class PostDisplay(DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super(PostDisplay, self).get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(to_post=self.kwargs.get('pk'))
        context['form'] = CommentForm()
        return context

class PostComment(SingleObjectMixin, FormView):
    template_name = "blog/post_detail.html"
    form_class = CommentForm
    model = Comment

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(PostComment, self).post(self, request, *args, **kwargs)

    def form_valid(self, form):
        text = form.cleaned_data['text']
        author = form.cleaned_data['author']
        post = Post.objects.get(id=self.kwargs['pk'])
        to_post = post
        comment = Comment(text=text, author=author, to_post=to_post)
        comment.save()
        return super(PostComment, self).form_valid(form)

    def get_success_url(self):
        return reverse('post_detail', kwargs={'pk': self.object.pk})

class PostDetail(View):

    def get(self, request, *args, **kwargs):
        view = PostDisplay.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = PostComment.as_view()
        return view(request, *args, **kwargs)

    # TODO see django doc and analyze: https://docs.djangoproject.com/en/1.8/topics/class-based-views/mixins/#using-formmixin-with-detailview

class AboutMeView(TemplateView):

    template_name = "blog/about_me.html"