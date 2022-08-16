from crypt import methods
from distutils.log import error
from pydoc import describe
import re
from django.shortcuts import render
from rest_framework.response import Response
# for api creation its like a middleware
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from django.http import JsonResponse
from rest_framework.permissions import AllowAny
import json
from django.contrib.auth.models import User
from drf_yasg.utils import swagger_auto_schema


@api_view(['POST'])
@swagger_auto_schema(operation_description="Send username password email and confirm password as a post to api")
@permission_classes([AllowAny])
def user_registration_api(request):
    errors = []
    keys = request.data.keys()
    if request.method == 'POST':
        if not 'username' in keys:
            errors.append('username field is required')
        if not 'email' in keys:
            errors.append('email field is required')
        if not 'password' in keys:
            errors.append('password is required')
        if not 'password2' in keys:
            errors.append('confirm password is required')

        if len(errors) < 1:
            try:
                newuser = User.objects.create(
                    username=request.data['username'],
                    email=request.data['email'],
                )
                newuser.set_password(request.data['password2'])
                newuser.save()
            except Exception as e:
                return Response({'message': 'Network Error', 'created': False})
            return Response({"created": True, "userdetails": {"id": newuser.id, "username": newuser.username, "email": newuser.email}})
        else:
            return Response({'errors': errors, 'created': False})
