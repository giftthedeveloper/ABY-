from django.shortcuts import render
from django.contrib.auth import authenticate, login
from rest_framework import viewsets
from rest_framework.response import Response
from django.views.generic import TemplateView
from django.http import HttpResponse


class SignUpView(TemplateView):
    template_name = 'frontend/signup.html'
