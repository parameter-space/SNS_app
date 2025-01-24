from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True, null=True)
    author = models.ForeignKey("account.CustomUser", on_delete=models.CASCADE, related_name='posts') 
    image = models.ImageField(upload_to='posts/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    like_count = models.PositiveIntegerField(default=0)
    like_list = models.ManyToManyField("account.CustomUser", null=True, blank=True, help_text="id of liked users")
    comment_count = models.PositiveIntegerField(default=0)
    def __str__(self):
        return f"{self.title} ({self.id})"


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    author = models.ForeignKey("account.CustomUser", on_delete=models.CASCADE, related_name='comments')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.author.username} commented on {self.post.title}'