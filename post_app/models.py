from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='posts/', null=True, blank=True)

    like = models.PositiveIntegerField(default=0)
    dislike = models.PositiveIntegerField(default=0)
    share = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title



class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f'Comment on {self.post.title} by {self.created_at.strftime("%Y-%m-%d %H:%M:%S")}'