from rest_framework.generics import ListAPIView

from django.shortcuts import get_object_or_404    
from .models import Post, Comment, Category, Discussion, Report, Subcategory
from .serializers import (PostSerializer, CommentSerializer, CategorySerializer, SearchSerializer, DiscussionSerializer, ReportSerializer,
                          SubcategorySerializer)
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework import status, filters
# Create your views here.


class DiscussionView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        discussions = Discussion.objects.all().order_by('-created_at')
        serializer = DiscussionSerializer(discussions, many=True)

        return Response(serializer.data)

    def post(self, request):
        serializer = DiscussionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            # print(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DiscussionDetailView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        return get_object_or_404(Discussion, pk=pk)

    def get(self, request, pk):
        discussion = self.get_object(pk)
        serializer = DiscussionSerializer(discussion)
        return Response(serializer.data)

    def put(self, request, pk):
        discussion = self.get_object(pk)
        if discussion.user != request.user:
            return Response({'error': 'You do not have permission to edit this discussion.'}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = DiscussionSerializer(discussion, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        discussion = self.get_object(pk)
        if discussion.user != request.user:
            return Response({'error': 'You do not have permission to delete this discussion.'}, status=status.HTTP_403_FORBIDDEN)
        discussion.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PostListView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    def get(self,request):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = PostSerializer(data=request.data)      
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)    
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class PostDetailView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        return get_object_or_404(Post, pk=pk)
    
    def get(self, request, pk):
        try:
            post = Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = PostSerializer(post)
        return Response(serializer.data)

    def put(self, request, pk):
        post = self.get_object(pk)
        serializer = PostSerializer(post, data=request.data)    
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  
    
    def delete(self, request, pk):
        post = self.get_object(pk)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CommentListView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    def get(self,request,post_id):
        post = get_object_or_404(Post,id=post_id)
        comments = post.comments.all().order_by('-created_at')
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)
    
    def post(self,request,post_id):
        post = get_object_or_404(Post,id=post_id)
        data = request.data.copy()
        data['post']=post.id
        serializer = CommentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 

class CommentDetailView(APIView):

    def get_object(self, pk):
        return get_object_or_404(Post, pk=pk)
    
    def get(self, request, comment_id):
        comment = self.get_object(comment_id)
        serializer = CommentSerializer(comment)
        return Response(serializer.data)
    
    def put(self, request, comment_id):
        comment = self.get_object(comment_id)
        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, comment_id):
        comment = self.get_object(comment_id)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        

class CategoryListCreateView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self,request):
        categories = Category.objects.all().order_by('-created_at')
        serializer = CategorySerializer(categories, many=True, context={'request':request})
        return Response(serializer.data)
    
    def post(self,request):
        serializer = CategorySerializer(data=request.data, context={'request':request})
        if serializer.is_valid():
            category = serializer.save()
            serializer = CategorySerializer(category, context = {'request':request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)


class CategoryFollowToggleView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def post(self,request,category_id):
        category = Category.objects.get(id=category_id)
        user = request.user
        if user in category.followers.all():
            category.followers.remove(user)
            return Response({'message': 'Unfollowed'}, status=status.HTTP_200_OK)
        else:
            category.followers.add(user)
            return Response({'message': 'Followed'}, status=status.HTTP_200_OK)


class LatestPostListView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        posts = Post.objects.all().order_by('-created_at')[:3]
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

class SearchView(ListAPIView):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = SearchSerializer
    filter_backends = [filters.SearchFilter,filters.OrderingFilter]
    search_fields = ['category__title', 'title', 'description']
    ordering_fields = ['created_at', 'like', 'dislike', 'share']
    ordering = ['-created_at']

class ReportView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def post(self,request,post_id):
        post = Post.objects.get(id=post_id)
        user= request.user
        if Report.objects.filter(post=post, user=user).exists():
            return Response({'error': 'You have already submitted a report for this post.'}, status=status.HTTP_400_BAD_REQUEST)
        data= request.data.copy()
        data['user'] = user.id
        serializer = ReportSerializer(data=data)
        if serializer.is_valid():
            serializer.save(user=user, post=post)
            response_data = {
                "success": True,
                "message": "Report submitted successfully",
                "data": serializer.data
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        response_data={
            "success": False,
            "message": "Failed to submit report",
            "errors": serializer.errors
        }
        return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
    
class SubcategoryAPIView(APIView):
    def get(self,request):
        subcategories = Subcategory.objects.all()
        serializer = SubcategorySerializer(subcategories, many=True)
        return Response(serializer.data)
    def post(self,request):
        serializer = SubcategorySerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Retrieve, Update, Delete
class SubCategoryDetailAPIView(APIView):

    def get_objects(self,pk):
        return Subcategory.objects.get(pk=pk)
    
    def get(self,request,pk):
        subcategories = self.get_objects(pk)
        serializer = SubcategorySerializer(subcategories)
        return Response(serializer.data)
    
    def put(self,request,pk):
        subcategories = self.get_objects(pk)
        serializer = SubcategorySerializer(subcategories, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,pk):
        subcategories = self.get_objects(pk)
        subcategories.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    

        































