from rest_framework import viewsets, status
from .models import Post, Comment
from .serializers import PostSerializer, PostReadSerializer
from account.models import CustomUser
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer 
    read_serializer_class = PostReadSerializer 
    permission_classes = [IsAuthenticatedOrReadOnly] 

    """serializer 선택"""
    def get_serializer_class(self):
        if self.action == 'list'or self.action == 'retrieve':
            return self.read_serializer_class
        return self.serializer_class
    
    """author로 필터링 할지, title로 필터링 할지, 필터링을 안할지 분류"""
    def get_queryset(self): 
        queryset = self.queryset
        
        authour_id = self.request.query_params.get('author_id', None) 
        if authour_id:
            queryset = queryset.filter(author_id=authour_id)
        
        title = self.request.query_params.get('title', None)
        if title:
            queryset = queryset.filter(title__icontains=title)

        return queryset
    

    """Post를 생성할 때 user 정보를 직접 json으로 넘겨주지 않고 request에서 user정보를 받아서 post에 저장하는 방식을 사용한다."""
    def perform_create(self, serializer): 
        serializer.save(author=self.request.user) 

    def create(self, request, *args, **kwargs): # 오버라이딩 전 create 메서드와 차이 없음
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    """업데이트 메서드"""
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False) 
        instance = self.get_object() # 여기서 instance는 생성자에서 받아온 post 객체이다.
        if instance.author != self.request.user: 
            return Response(status=status.HTTP_403_FORBIDDEN)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)
    
    """삭제 메서드"""
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.author != self.request.user: 
            return Response(status=status.HTTP_403_FORBIDDEN)
        self.perform_destroy(instance)

        return Response(status=status.HTTP_204_NO_CONTENT)