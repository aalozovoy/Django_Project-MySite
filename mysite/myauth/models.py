from django.contrib.auth.models import User
from django.db import models



def user_avatar_dir_path(instance: 'Profile', filename: str) -> str:
    '''кастомная функция (путь к файлу)'''
    return f'profiles/profile_{instance.user}/avatar/{filename}'

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    agreement_accepted = models.BooleanField(default=False)
    avatar = models.ImageField(null=True, blank=True, upload_to=user_avatar_dir_path)


