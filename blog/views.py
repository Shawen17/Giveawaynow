from django.shortcuts import render,get_object_or_404, redirect
from .models import Blog,Comment
from .forms import CommentForm
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect,HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator





def all_blogs(request):
    blogs = Blog.objects.order_by('-id')[:12]
    genre=Blog.objects.values('genre').distinct()
    category=list(genre)
    category=[(i['genre']) for i in category]
    blog_count = Blog.objects.count
    return render(request,'blog/blog_index.html',{'blogs':blogs,'blog_count':blog_count,'category':category})


def detail(request,blog_id):
    
    posts = get_object_or_404(Blog, pk= blog_id)
    blog_desc = Blog.objects.all()
    comments = posts.comments.filter(active=True).order_by('-created')[:30]
    comment_form =CommentForm()
    return render(request,'blog/viewblog.html',{'posts':posts,'comments':comments,
                'comment_form':comment_form,'blog_desc':blog_desc})
       
def list_blog(request):
    blogs=Blog.objects.all().order_by('-date')
    p=Paginator(blogs,10)
    page_number=request.GET.get('page')
    try:
        page_obj=p.get_page(page_number)
    except PageNotAnInterger:
        page_obj=p.page(1)
    except EmptyPage:
        page_obj=p.page(p.num_pages)

    return render(request,'blog/all_blog.html',{'blogs':blogs,'page_obj':page_obj})


def post_comment(request,blog_id):
    posts= get_object_or_404(Blog,pk=blog_id)
    
    if request.method=='POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment=comment_form.save(commit=False)
            new_comment.post= posts
            new_comment.save()
        return HttpResponseRedirect('view')    
        
    else:
        comment_form= CommentForm()
        return render(request,'blog/viewblog.html',{'comment_form':comment_form})


@csrf_exempt
def category(request,category):
    cat=str(category)
    blog_count=Blog.objects.filter(genre=cat).count
    blogs=Blog.objects.filter(genre=cat)
    p=Paginator(blogs,10)
    page_number=request.GET.get('page')
    try:
        page_obj=p.get_page(page_number)
    except PageNotAnInterger:
        page_obj=p.page(1)
    except EmptyPage:
        page_obj=p.page(p.num_pages)
    return render(request,'blog/blog_genre.html',{'page_obj':page_obj,'cat':cat,'blog_count':blog_count})