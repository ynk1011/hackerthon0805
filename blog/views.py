from elections.models import Candidate
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Blog, Blogs, HashTag, Comment, Post
from .forms import BlogForm, CommentForm, ResponseForm
# from blog.models import Question
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, request
from django.views.generic import View
try:
    from django.utils import simplejson as json
except ImportError:
    import json
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

# Create your views here.


def home(request):
    # 모든 Post를 가져와 postlist에 저장
    postlist = Post.objects
    blog = Blog.objects  # query set
    # home.html 페이지를 열 때, 모든 Post인 postlist도 같이 가져옴
    return render(request, 'home.html', {'blogs': blog, 'postlist': postlist})

# 게시판섹션(구 board)의 게시글(posting)을 부르는 posting 함수
def posting(request, pk):
    # 게시글(Post) 중 pk(primary_key)를 이용해 하나의 게시글(post)를 검색
    #post_detail = get_object_or_404(Post, pk=post_id)
    post_detail = Post.objects.get(pk=pk)
    # posting.html 페이지를 열 때, 찾아낸 게시글(post)을 post라는 이름으로 가져옴
    return render(request, 'posting.html', {'post': post_detail})

def detail(request, blog_id):
    blog_detail = get_object_or_404(Blog, pk=blog_id)
    comments = Comment.objects.filter(post=blog_id)
    blog_hashtag = blog_detail.hashtag.all()
    if request.method == "POST":
        comment = Comment()
        # comment.author_name = request.POST['author']
        comment.post = blog_detail
        comment.comment_text = request.POST['body']
        comment.date = timezone.now()
        comment.save()
    return render(request, 'detail.html', {'blog': blog_detail, 'comments': comments, 'hashtags': blog_hashtag})


def new(request):  # 글 작성 페이지로 이동
    form = BlogForm()
    return render(request, 'new.html', {'form': form})


def create(request):
    form = BlogForm(request.POST, request.FILES)
    if form.is_valid():
        new_blog = form.save(commit=False)
        new_blog.pub_date = timezone.now()
        new_blog.save()
        hashtags = request.POST['hashtags']
        hashtag = hashtags.split(",")
        for tag in hashtag:
            ht = HashTag.objects.get_or_create(hashtag_name=tag)
            new_blog.hashtag.add(ht[0])
        return redirect('detail', new_blog.id)
    return redirect('home')


def edit(request, blog_id):
    blog_detail = get_object_or_404(Blog, pk=blog_id)
    return render(request, 'edit.html', {'blog': blog_detail})


def update(request, blog_id):
    blog_update = get_object_or_404(Blog, pk=blog_id)
    blog_update.title = request.POST['title']
    blog_update.body = request.POST['body']
    blog_update.save()
    return redirect('home')


def delete(request, blog_id):
    blog_delete = get_object_or_404(Blog, pk=blog_id)
    blog_delete.delete()
    return redirect('home')

#댓글...
def add_comment_to_post(request, blog_id):
    blog = get_object_or_404(Blog, pk=blog_id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = blog
            comment.save()
            return redirect('detail', blog_id)

    else:
        form = CommentForm()
    return render(request, 'add_comment_to_post.html', {'form': form})


def mypage(request):
    blog = Blog.objects  # query set
    return render(request, 'mypage.html', {'blogs': blog})



# survey

def main(request):
    return render(request, 'main.html')


def result(request):
    return render(request, 'result.html')

def index(request):
    sort = request.GET.get('sort','') #url의 쿼리스트링을 가져온다. 없는 경우 공백을 리턴한다

    if sort == Blog.objects.order_by('-update_date'):
        return render(request, 'blog/home.html', {'blogs' : Blogs})
    
    else:
        user = request.user
        card = Blogs.objects.filter(name_id = user).order_by('-update_date') #복수를 가져올수 있음
        return render(request, 'blog/home.html', {'blogs' : Blogs})
