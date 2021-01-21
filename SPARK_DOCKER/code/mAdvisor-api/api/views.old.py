from django.shortcuts import render
from django.http import HttpResponse

from rest_framework.decorators import renderer_classes, api_view
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

# Create your views here.

def showme(request):
    return HttpResponse("Alright, this is a test");

@api_view(['GET'])
@renderer_classes((JSONRenderer,))
def jack(request):
    return Response({'name': "prakash raman"});
