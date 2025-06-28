from rest_framework import serializers
from .models import Post, Comment, Category, Discussion


class DiscussionSerializer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField() 
    class Meta:
        model = Discussion
        fields = '__all__'
        read_only_fields = ['user', 'created_at']

    def get_user_name(self, obj):
        return  obj.user.email


class PostSerializer(serializers.ModelSerializer):

    category_name = serializers.CharField(write_only=True, required=False)
    category = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = ('created_at','id', 'like', 'dislike', 'share')  
    def get_category(self, obj):
        return obj.category.title if obj.category else None
    
    def create(self,validate_data):
        category_name = validate_data.pop('category_name', None)
        if category_name:
            category,created = Category.objects.get_or_create(title=category_name)
            validate_data['category'] = category
        return Post.objects.create(**validate_data)



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


class SearchSerializer(serializers.Serializer):
    category_name = serializers.CharField(source='category__title', required=False)

    class Meta:
        model = Post
        fields = ['category_name']  
        read_only_fields = ('id', 'created_at', 'like', 'dislike', 'share')
