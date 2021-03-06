from django.views.generic import View

from .forms import TagForm, PostForm
from .utils import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Q


def vacancy_list(request):
    #  Поиск на странице по 'title' и 'body'
    search_query = request.GET.get('search', '')

    if search_query:
        posts = Post.objects.filter(Q(title__icontains=search_query) | Q(body__icontains=search_query))
    else:
        posts = Post.objects.all()

    paginator = Paginator(posts, 4)  # Определяем пагинацию, количество постов на странице

    page_number = request.GET.get('page', 1)  # Извлекаем 'page', в случае если страница не будет найдена, будет выведена первая
    page = paginator.get_page(page_number)

    is_paginated = page.has_other_pages()

    if page.has_previous():
        prev_url = '?page={}'.format(page.previous_page_number())
    else:
        prev_url = ''

    if page.has_next():
        next_url = '?page={}'.format(page.next_page_number())
    else:
        next_url = ''

    context = {
        'page_object': page,
        'is_paginated': is_paginated,
        'next_url': next_url,
        'prev_url': prev_url
    }



    return render(request, 'website/vacancy.html', context=context)


class PostDetail(ObjectDetailMixin, View):
    model = Post
    template = 'website/post_detail.html'


class PostCreate(LoginRequiredMixin, ObjectCreateMixin, View):
    model_form = PostForm
    template = 'website/post_create.html'
    raise_exception = True


class PostUpdate(LoginRequiredMixin, ObjectUpdateMixin, View):
    model = Post
    model_form = PostForm
    template = 'website/post_update_form.html'
    raise_exception = True


class PostDelete(LoginRequiredMixin, ObjectDeleteMixin, View):
    model = Post
    template = 'website/post_delete_form.html'
    redirect_url = 'vacancy_url'
    raise_exception = True


def tags_list(request):
    tags = Tag.objects.all()
    return render(request, 'website/tags_list.html', context={'tags': tags})


class TagDetail(ObjectDetailMixin, View):
    model = Tag
    template = 'website/tag_detail.html'


class TagCreate(LoginRequiredMixin, ObjectCreateMixin, View):
    model_form = TagForm
    template = 'website/tag_create.html'
    raise_exception = True


class TagUpdate(LoginRequiredMixin, ObjectUpdateMixin, View):
    model = Tag
    model_form = TagForm
    template = 'website/tag_update_form.html'
    raise_exception = True


class TagDelete(LoginRequiredMixin, ObjectDeleteMixin, View):
    model = Tag
    template = 'website/tag_delete_form.html'
    redirect_url = 'tags_list_url'
    raise_exception = True


