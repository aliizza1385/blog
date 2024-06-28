from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify
from datetime import datetime


class User(AbstractUser):
    image = models.ImageField(upload_to='static/user/')


class Tag(models.Model):
    name = models.CharField(max_length=255)


class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, null=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.slug:
            now = datetime.now()
            self.slug = slugify(self.name)+"-"+str(now.year)+"-"+str(now.month)+"-"+str(
                now.day)+"-"+str(now.minute)+"-"+str(now.second)+"-"+str(now.microsecond)
            self.save()


class Post(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField(help_text="Content of the post")
    author = models.CharField(max_length=255, default='alireza',null=True)
    image = models.ImageField(upload_to='photo')
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=0)
    tag = models.ManyToManyField(Tag)
    likes_count = models.PositiveIntegerField(default=0) 


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class ReplyComment(models.Model):
    parent_comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='replies')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

# class Like(models.Model):
#     post = models.ForeignKey(Post, on_delete=models.CASCADE)
#     count = models
