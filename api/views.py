from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.core.mail import EmailMessage
from django.contrib.auth.tokens import default_token_generator
from django.contrib import messages
from django.conf import settings
from django.urls import reverse
from django.views.generic import TemplateView
from django.contrib.auth import authenticate, login



class SignUpView(TemplateView):
    template_name = 'frontend/signup.html'
    
    def post(self, request, *args, **kwargs):

        #get the form data
        name = request.POST.get("name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        password_confirm = request.POST.get("password_confirm")

        #alidating the form details
        if not name or not email or not password or not password_confirm:
            messages.error(request, f'Please fill in all required fields')
            return (request, self.template_name)
        
        #validate passwords
        if password != password_confirm:
            messages.error(request, f'Passwords do not match')
            return (request, self.template_name)
        
        #  validating unique email for all users
        if User.objects.filter(email=email).exists():
            messages.error(request, f'Email already registered')
            return render(request, self.template_name)
                          
        #creating a user instance from the form data
        user = User(name=name, email=email)
        user.set_password(password)
        user.is_active = False  #I set the user to False because i want to verify users with email 
        user.save()

        #email verification
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        current_site = get_current_site(request)
        mail_subject = 'Activate your account'
        message = render_to_string('frontend/email_activation.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': uid,
            'token': token,
        })
        to_email = email
        email = EmailMessage(mail_subject, message, to=[to_email])
        email.send()
        messages.success(request, 'Please check your email to activate your account.')
        return redirect('login')  
    

class LoginView(TemplateView):
    template_name = 'frontend/login.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        # Get the login details
        email = request.POST.get("email")
        password = request.POST.get("password")


        #check if user is authenticated
        user = authenticate(request, email=email, password=password)

        if user is not None:
            # Log in the user
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid email or password.')
            return render(request, self.template_name)


class HomeView(TemplateView):
    template_name = 'frontend/home.html'