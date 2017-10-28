
from django.shortcuts import get_object_or_404

from rest_framework import generics, status, response, exceptions

from .models import Post, Comment, Like
from .serializers import PostSerializer, CommentSerializer, LikeSerializer
from .permissions import ManualGetAuthentication


class BlogPostsApi(generics.ListCreateAPIView):
    """
    api to return queryset of posts/create post
    """
    model = Post
    page_size = 10
    serializer_class = PostSerializer
    permission_classes = [ManualGetAuthentication, ]
    queryset = model.objects.all()

    def perform_save(self, serializer):
        serializer.save()


class BlogPostsDetailApi(generics.RetrieveUpdateDestroyAPIView):
    """
    api too return detail/update/destroy a post object
    """
    model = Post
    serializer_class = PostSerializer
    permission_classes = [ManualGetAuthentication, ]
    lookup_url_kwargs = "post_id"

    def get_object(self):
        return get_object_or_404(self.model, id=self.kwargs[self.lookup_url_kwargs])

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if self.request.user != instance.created_by:
            raise exceptions.PermissionDenied
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return response.Response(serializer.data, status=status.HTTP_200_OK)

    def perform_update(self, serializer):
        serializer.save()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if self.request.user != instance.created_by:
            raise exceptions.PermissionDenied
        instance.delete = True
        instance.save()
        return response.Response(data="Success", status=status.HTTP_200_OK)


class BlogPostCommentsApi(generics.ListCreateAPIView):
    """
    api to return queryset of posts/create post
    """
    model = Comment
    page_size = 10
    serializer_class = CommentSerializer
    permission_classes = [ManualGetAuthentication, ]
    queryset = model.objects.all()
    lookup_url_kwargs = "post_id"

    def get_queryset(self):
        post = get_object_or_404(Post, id=self.kwargs[self.lookup_url_kwargs])
        return self.queryset.filter(post=post)


class BlogPostCommentsDetailApi(generics.RetrieveUpdateDestroyAPIView):
    """
    api too return detail/update/destroy a post object
    """
    model = Comment
    serializer_class = CommentSerializer
    permission_classes = [ManualGetAuthentication, ]
    lookup_url_kwargs = "post_id"
    lookup_field = "comment_id"

    def get_object(self):
        post = get_object_or_404(Post, id=self.kwargs[self.lookup_url_kwargs])
        queryset = self.model.objects.filter(post=post)
        comment = get_object_or_404(queryset, id=self.kwargs[self.lookup_field])
        return comment

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if self.request.user != instance.created_by:
            raise exceptions.PermissionDenied
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return response.Response(serializer.data, status=status.HTTP_200_OK)

    def perform_update(self, serializer):
        serializer.save()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if self.request.user != instance.created_by or self.request.user != instance.post.created_by:
            raise exceptions.PermissionDenied
        instance.delete = True
        instance.save()
        return response.Response(data="Success", status=status.HTTP_200_OK)


class BlogPostLikesApi(generics.GenericAPIView):
    """
    api to return likes on post and create/destroy likes on a post
    """
    model = Like
    serializer_class = LikeSerializer
    permission_classes = [ManualGetAuthentication, ]
    lookup_url_kwargs = "post_id"

    def get_object(self):
        post = get_object_or_404(Post, id=self.kwargs[self.lookup_url_kwargs])
        likes = self.model.objects.filter(post=post)
        if likes.exists():
            return likes
        return None

    def get(self, request, *args, **kwargs):
        post = get_object_or_404(Post, id=self.kwargs[self.lookup_url_kwargs])
        likes = self.model.objects.filter(post=post)
        serializer = self.get_serializer(likes, many=True)
        return response.Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance is not None:
            instance.delete()
            return response.Response(data="unliked successfully.", status=status.HTTP_200_OK)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return response.Response(serializer.data, status=status.HTTP_200_OK)
