from django.urls import path
from .views import PostListView,PostDetailView,CommentListView,CommentDetailView

urlpatterns = [
    path('posts/', PostListView.as_view(), name='post-list-create'),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post-detail'),

    path('posts/<int:post_id>/comments/', CommentListView.as_view(), name='comment-list-create'),
    path('comments/<int:comment_id>/', CommentDetailView.as_view(), name='comment-detail'),
]
