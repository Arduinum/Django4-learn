from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from blog.models import Post


def post_list(request):
    post_list = Post.published.all()
    paginator = Paginator(post_list, 3)
    page_number = request.GET.get('page', 1)
    
    
    try:
        posts = paginator.page(page_number)
    # вне диапазона
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)  # выдать последнюю страницу
    # номер страницы не целое число
    except PageNotAnInteger:
        posts = paginator.page(1)  # выдать 1 страницу

    return render(
        request=request, 
        template_name='blog/post/list.html', 
        context={'posts': posts}
    )

def post_detail(request, year, month, day, post):
    
    post = get_object_or_404(
        Post,  
        status=Post.Status.PUBLISHED,  
        publish__year=year,
        publish__month=month,
        publish__day=day,
        slug=post,
    )

    return render(
        request=request,
        template_name='blog/post/detail.html',
        context={'post': post}
    )
