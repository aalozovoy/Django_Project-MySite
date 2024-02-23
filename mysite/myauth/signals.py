from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Profile
from django.contrib.auth.models import User

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()



# В данном коде определены два обработчика сигналов для модели User.
# Первая функция create_user_profile будет вызываться каждый раз после сохранения нового экземпляра модели User.
# В этой функции проверяется, был ли создан новый пользователь (параметр created) и, если да,
# создается новый объект модели Profile, связанный с этим пользователем.
#
# Вторая функция save_user_profile будет вызываться каждый раз после сохранения (обновления) объекта модели User.
# В этой функции сохраняются изменения в объекте Profile, связанном с пользователем instance.
#
# Таким образом, эти обработчики сигналов позволяют автоматически создавать и сохранять объекты модели Profile
# при создании и обновлении пользователей в Django.