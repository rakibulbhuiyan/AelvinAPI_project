from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


class Post(models.Model):

    category = models.ForeignKey('Category', related_name='posts', on_delete=models.CASCADE, null=True, blank=True)

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


class Category(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='category_images/', blank=True, null=True)
    followers = models.ManyToManyField(User, related_name='followed_categories', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def total_followers(self):
        return self.followers.count()

class Subcategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories')
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='subcategory_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.category.title} → {self.title}"

class Discussion(models.Model):
    user = models.ForeignKey(User, related_name='discussions', on_delete=models.CASCADE)
    group_name = models.CharField(max_length=255)
    description = models.TextField()
    topic = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Discussion by {self.user.email} or {self.user}'
    

GENDER_CHOICES = (
    ('Male', 'Male'),
    ('Female', 'Female'),
    ('Other', 'Other'),
)

class Report(models.Model):
    
    user = models.ForeignKey(User, related_name='reports', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='reports', on_delete=models.CASCADE)
    submit_a_report = models.JSONField(default=list, blank=True, null=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'post']  # One report per post per user

    def __str__(self):
        return f"{self.user.username} reported on {self.post.title}"