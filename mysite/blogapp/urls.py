from django.contrib.auth.views import LoginView
from django.urls import path

from blogapp.views import ArticleListView

app_name = "blogapp"

urlpatterns = [
    path("", ArticleListView.as_view(), name="article"),
]

