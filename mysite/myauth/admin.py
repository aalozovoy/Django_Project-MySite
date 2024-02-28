from django.contrib import admin
from .models import Profile


admin.site.register(Profile) # регистрация модели
# class ProfileInline(admin.TabularInline):
#     ''' ProfileInline подключает встроенные записи '''
#     model = Profile.avatar
