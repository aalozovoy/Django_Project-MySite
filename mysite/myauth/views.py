from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.models import AnonymousUser, User
from django.contrib.auth.views import LogoutView
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView, CreateView, ListView, DetailView, UpdateView

from .forms import ProfileForm
from .models import Profile
from django.views import View



class UserListView(ListView):
    template_name = 'myauth/user_list.html'
    model = User
    context_object_name = 'users'

class UserDetailsView(DetailView):
    template_name = 'myauth/user_detail.html'
    model = User
    context_object_name = 'user'

class AboutMeView(ListView):
    template_name = 'myauth/about_me.html'
    model = Profile
    context_object_name = 'profiles'

class UploadAvatarView(UserPassesTestMixin, UpdateView):
    def test_func(self):
        return self.request.user.is_staff or self.request.user.id == self.kwargs['pk']
    template_name = 'myauth/avatar_upload_form.html'
    model = Profile
    fields = ('avatar',)
    success_url = reverse_lazy('myauth:users_list')

    def get_object(self, queryset=None):
        pk = self.kwargs.get(self.pk_url_kwarg)
        user = User.objects.select_related("profile").get(pk=pk)
        try:
            return user.profile
        except Profile.DoesNotExist:
            return Profile.objects.create(user=user)


class RegisterView(CreateView):
    form_class = UserCreationForm # UserCreationForm - готовая форма
    template_name = 'myauth/register.html'
    success_url = reverse_lazy('myauth:about_me')

    def form_valid(self, form): # аутентификация
        response = super().form_valid(form)
        Profile.objects.create(user=self.object)
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(self.request,
                            username=username,
                            password=password)
        login(request=self.request, user=user)
        return response

class MyLogoutView(LogoutView):
    next_page = reverse_lazy('myauth:login')

@user_passes_test(lambda u: u.is_superuser)
def set_cookie_view(request: HttpRequest) -> HttpResponse:
    response = HttpResponse('Cookie set')
    response.set_cookie('fizz', 'buzz', max_age=3600)
    return response

def get_cookie_view(request: HttpRequest) -> HttpResponse:
    value = request.COOKIES.get('fizz', 'default value')
    return HttpResponse(f'Cookie value: {value!r}')

@permission_required('myauth.view_profale', raise_exception=True)
def set_session_view(request: HttpRequest) -> HttpResponse:
    request.session['foobar'] = 'spameggs'
    return HttpResponse('Session set!')

@login_required
def get_session_view(request: HttpRequest) -> HttpResponse:
    value = request.session.get('foobar', 'default value')
    return HttpResponse(f'Session value: {value!r}')

class FooBarView(View):
    def get(self, request: HttpRequest) -> JsonResponse:
        return JsonResponse({'foo': 'bar', 'spam': 'eggs'})







# РЕАЛИЗОВАННО В LoginView см. url
# def login_view(request: HttpRequest) -> HttpResponse:
#     if request.method == "GET":
#         if request.user.is_authenticated:
#             return redirect('/admin/')
#         return render(request, 'myauth/login.html')
#
#     username = request.POST['username']
#     password = request.POST['password']
#
#     user = authenticate(request, username=username, password=password) # аутентификация
#     if user is not None:
#         login(request, user)
#         return redirect('/admin/')
#     return render(request, 'myauth/login.html', {'Error:' 'Invalid username or password'})





