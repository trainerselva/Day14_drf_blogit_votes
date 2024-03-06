from rest_framework import serializers
from .models import Post
from .models import Vote

# Create a serializer for the Post model
# class PostSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Post
#         fields = ['id', 'title', 'url', 'poster', 'created']


# PostSerializer containing read-only fields
class PostSerializer(serializers.ModelSerializer):
    poster = serializers.ReadOnlyField(source="poster.username")
    poster_id = serializers.ReadOnlyField(source="poster.id")
    votes = serializers.SerializerMethodField()
    
    class Meta:
        model = Post
        fields = ['id', 'title', 'url', 'poster', 'poster_id', 'created',
                  'votes']
        
    def get_votes(self, post):
        return Vote.objects.filter(post=post).count()


# Add a serializer for Vote model
class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ['id']