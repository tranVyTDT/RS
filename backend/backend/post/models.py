from django.db import models
from user.models import CustomUser
from constrain.choice import STATE
from django.utils import timezone
from django.db.models import Q


def file_directory_path(self, filename):
    return f'file/{self.author.id}/{filename}'

class Post(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    post_id = models.CharField(max_length=20, unique= True)
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=200, blank= True, null = True)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    state = models.CharField(max_length=100, choices=STATE, default= STATE[0][0])
    upload = models.FileField(upload_to = file_directory_path, null = True, blank= True)

    is_approve_staff = models.BooleanField(default=False)
    is_approve_director = models.BooleanField(default=False)
    approve_staff = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True, related_name="approve_staff")
    approve_director = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True, related_name="approve_director")

    def is_active(self):
        return self.is_approve_staff and self.is_approve_director

    @staticmethod
    def get_approve_staff(posts):
        return posts.filter(Q(is_approve_staff = True) & Q(is_approve_director = False))

    @staticmethod
    def get_approve_director(posts):
        return posts.filter(Q(is_approve_staff = True) & Q(is_approve_director = True))
    



