from django.contrib.auth import authenticate, login

from .utils import JsonResponse

import json

def login_ajax(request):
  if not ('username' in request.POST and 'password' in request.POST):
    return JsonReponse({ 'errors': { 'non_field_errors': ['Please enter username and password'] } })
  user = authenticate(username=request.POST['username'],password=request.POST['password'])
  if not user:
    return JsonResponse({ 'errors': { 'non_field_errors': ['Username and password do not match.'] } })
  login(request,user)
  return JsonResponse({ 'user': {'id': user.id, 'username': user.username } })
