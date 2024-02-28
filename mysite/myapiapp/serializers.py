from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request

from django.contrib.auth.models import Group
from rest_framework import serializers




@api_view()
def hello_world_view(request: Request) -> Response:
   return Response({'massage': 'Hello world!'})

class GroupSerializers(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = 'pk', 'name'


