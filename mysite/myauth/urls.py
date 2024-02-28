from django.contrib.auth.views import LoginView
from django.urls import path
# from .views import login_view

from .views import (get_cookie_view,
                    set_cookie_view,
                    get_session_view,
                    set_session_view,
                    MyLogoutView,
                    AboutMeView,
                    RegisterView,
                    FooBarView,
                    UserListView,
                    UserDetailsView,
                    UploadAvatarView,
                    HelloView)


app_name = "myauth"

urlpatterns = [
    path("login/",
         LoginView.as_view(template_name="myauth/login.html",
                           redirect_authenticated_user=True,
                           ),
        name="login"),
    path("hello/", HelloView.as_view(), name="hello"),
    path("logout/", MyLogoutView.as_view(), name="logout"),
    path("about_me/", AboutMeView.as_view(), name="about_me"),
    path("about_me/<int:pk>/upload_avatar/", UploadAvatarView.as_view(), name="upload_avatar"),
    path("register/", RegisterView.as_view(), name="register"),
    path("users_list/", UserListView.as_view(), name="users_list"),
    path("users_list/<int:pk>/", UserDetailsView.as_view(), name="user_detail"),
    path("cookie/get/", get_cookie_view, name="cookie_get"),
    path("cookie/set/", set_cookie_view, name="cookie_set"),
    path("session/get/", get_session_view, name="session_get"),
    path("session/set/", set_session_view, name="session_set"),
    path("foo-bar/", FooBarView.as_view(), name="foo-bar"),
]
'''
template_name="myauth/login.html" - необходимо указать шаблон (откорректировать шаблон {{ form.as_p }})
LOGIN_REDIRECT_URL = '/admin/' - указывается в settings (куда переходить)
redirect_authenticated_user=True - чтобы не вводить данные каждый раз
'''
