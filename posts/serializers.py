
from django.shortcuts import get_object_or_404

from rest_framework import serializers

from auth.serializers import ProfileMiniSerializer
from .models import Post, Comment, Like


class PostSerializer(serializers.ModelSerializer):

    created_by = ProfileMiniSerializer(read_only=True)

    def validate(self, attrs):
        view = self.context.get("view")
        attrs["created_by"] = view.request.user
        return attrs

    class Meta:
        model = Post
        exclude = ("delete", )


class CommentSerializer(serializers.ModelSerializer):

    post = PostSerializer(read_only=True)
    created_by = ProfileMiniSerializer(read_only=True)

    def validate(self, attrs):
        view = self.context.get("view")
        post = get_object_or_404(Post, id=view.kwargs[view.lookup_url_kwargs])
        attrs["post"] = post
        attrs["created_by"] = view.request.user
        return attrs

    class Meta:
        model = Comment
        exclude = ("delete", )


class LikeSerializer(serializers.ModelSerializer):

    def validate(self, attrs):
        view = self.context.get("view")
        post = get_object_or_404(Post, id=view.kwargs[view.lookup_url_kwargs])
        attrs["post"] = post
        attrs["created_by"] = view.request.user
        return attrs

    class Meta:
        model = Like
        fields = "__all__"
        read_only_fields = ('post', 'created_by')
