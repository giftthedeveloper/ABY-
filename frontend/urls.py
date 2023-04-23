
from django.contrib import admin
from django.urls import path
from api.views import SignUpView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    #path('login/', LoginView.as_view(), name='login'),
    path('signup/', SignUpView.as_view(), name="signup"),

]
