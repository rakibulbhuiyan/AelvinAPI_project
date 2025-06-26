from rest_framework import serializers
from .models import Post, Comment, Category


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = ('created_at','id', 'like', 'dislike', 'share')  

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('created_at','id')

class CategorySerializer(serializers.ModelSerializer):

    is_following = serializers.SerializerMethodField()
    total_followers = serializers.ReadOnlyField()

    class Meta:
        model = Category
        fields = ['id', 'title', 'description', 'image', 'created_at', 'is_following', 'total_followers']

    def get_is_following(self, obj):
        user = self.context['request'].user
        return user.is_authenticated and obj.followers.filter(id=user.id).exists()


