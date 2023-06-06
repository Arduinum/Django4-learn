from django.shortcuts import render, get_object_or_404
from blog.models import Post
from django.http import Http404


def post_list(request):
    posts = Post.published.all()

    return render(
        request=request, 
        template_name='blog/post/list.html', 
        context={'posts': posts}
    )

def post_detail(request, id):
    # try:
    #     post = Post.published.get(id=id)
    # except Post.DoesNotExist:
    #     raise Http404('Post No found')
    
    post = get_object_or_404(
        Post, 
        id=id, 
        status=Post.Status.PUBLISHED
    )
    
    return render(
        request=request,
        template_name='blog/post/detail.html',
        context={'post': post}
    )
