from django.urls import path
from .views import (PostListView,PostDetailView,CommentListView,CommentDetailView,
                    CategoryListCreateView, CategoryFollowToggleView,LatestPostListView)

urlpatterns = [
    path('posts/', PostListView.as_view(), name='post-list-create'),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post-detail'),

    path('posts/<int:post_id>/comments/', CommentListView.as_view(), name='comment-list-create'),
    path('comments/<int:comment_id>/', CommentDetailView.as_view(), name='comment-detail'),

    path('categories/', CategoryListCreateView.as_view(), name='category-list-create'),
    path('categories/<int:category_id>/follow/', CategoryFollowToggleView.as_view(), name='category-follow-toggle'),


    path('latest-posts/', LatestPostListView.as_view(), name='latest-posts'),

]
