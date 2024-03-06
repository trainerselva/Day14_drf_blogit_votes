from django.shortcuts import render

# Create your views here.

# import required modules / packages
from rest_framework import generics
from rest_framework import permissions
from rest_framework.exceptions import ValidationError

from .models import Post
from .models import Vote

from .serializers import PostSerializer
from .serializers import VoteSerializer

from rest_framework import mixins
from rest_framework.response import Response
from rest_framework import status

# Create a class-based view to show a list of posts


class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        return serializer.save(poster=self.request.user)


# Create a class to create Votes
# class VoteCreate(generics.CreateAPIView):
#     serializer_class = VoteSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def get_queryset(self):
#         user = self.request.user
#         post = Post.objects.get(pk=self.kwargs['pk'])
#         return Vote.objects.filter(voter=user, post=post)

#     def perform_create(self, serializer):
#         if self.get_queryset().exists():
#             raise ValidationError('You have already voted for this post')
#         return serializer.save(voter=self.request.user,
#                                post=Post.objects.get(pk=self.kwargs['pk']))


# Adding mixins for delete operation
class VoteCreate(generics.CreateAPIView, mixins.DestroyModelMixin):
    serializer_class = VoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        post = Post.objects.get(pk=self.kwargs['pk'])
        return Vote.objects.filter(voter=user, post=post)

    def perform_create(self, serializer):
        if self.get_queryset().exists():
            raise ValidationError('You have already voted for this post')
        return serializer.save(voter=self.request.user,
                               post=Post.objects.get(pk=self.kwargs['pk']))

    def delete(self, request, *args, **kwargs):
        if self.get_queryset().exists():
            self.get_queryset().delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            raise ValidationError('You never voted for this post!!')


class PostRetrieveDestroy(generics.RetrieveDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def delete(self, request, *args, **kwargs):
        post = Post.objects.filter(pk=kwargs['pk'], 
                                   poster=self.request.user)
        if post.exists():
            return self.destroy(request, *args, **kwargs)
        else:
            raise ValidationError('This is not your post to delete!!')
