from django.urls import path
from .views import Auth

urlpatterns = [
    path('signin/', Auth.Signin.as_view(), name='signin'),
    path('signup/', Auth.Signup.as_view(), name='signup'),
]