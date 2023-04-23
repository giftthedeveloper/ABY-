from django.shortcuts import render
from django.contrib.auth import authenticate, login
from rest_framework import viewsets
from rest_framework.response import Response
from django.views.generic import TemplateView

class LoginView(TemplateView):
    template_name = 'frontend/login.html'

class SignUpView(TemplateView):
    template_name = 'frontend/signup.html'
