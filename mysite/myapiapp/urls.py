from django.urls import path

from .views import (hello_world_view,
                    GroupsListViews)

app_name = "myapiapp"

urlpatterns = [
    path("hello/", hello_world_view, name="hello"),
    path("groups/", GroupsListViews.as_view(), name="groups"),
]

