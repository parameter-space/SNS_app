from django.shortcuts import render
from django.views import View
from django.http import HttpResponse
from .models import Post
from rest_framework.permissions import IsAuthenticated


class PostListView(View):
    def get(self, request):
        posts = Post.objects.all()
        return render(request, 'post/list.html', {'posts': posts})

class PostCreateView(View):
    def get(self, request):
        return render(request, 'post/create.html')
    

class PostDetailView(View):
    def get(self, request, pk):
        try:
            post = Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return HttpResponse("<h1>404 Not Found</h1>")
        return render(request, 'post/detail.html', {'post': post})
    

class PostUpdateView(View):
    permission_classes = [IsAuthenticated]
    def get(self, request, pk): # 페이지를 get 방식으로 가져오기만 하고 랜더링 된 페이지에서 변경사항을 바꾼 다음에 api를 통해 update 요청
        try:
            post = Post.objects.get(pk=pk) 
        except Post.DoesNotExist: # 조회 실패 예외처리
            return HttpResponse("<h1>404 Not Found</h1>")
        
        if post.author != request.user: 
            return HttpResponse("<h1>403 Forbidden</h1>")
        return render(request, 'post/update.html', {'post': post})