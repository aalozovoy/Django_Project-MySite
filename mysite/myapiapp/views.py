from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView
from django.contrib.auth.models import Group
from .serializers import GroupSerializers

from rest_framework.generics import GenericAPIView, ListCreateAPIView
from rest_framework.mixins import ListModelMixin

@api_view()
def hello_world_view(request: Request) -> Response:
    return Response({'massage': 'Hello world!'})

class GroupsListViews(ListCreateAPIView):
    '''для получения списка групп'''
    queryset = Group.objects.all()
    serializer_class = GroupSerializers

# class GroupsListViews(GenericAPIView, ListModelMixin):
#     '''для получения списка групп'''
#     queryset = Group.objects.all()
#     serializer_class = GroupSerializers
#     def get(self, request: Request) -> Response:
#         return self.list(request)

