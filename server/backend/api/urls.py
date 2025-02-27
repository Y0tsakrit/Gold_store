from django.urls import path
from .views import System

urlpatterns = [
    path('signin/', System.Signin.as_view(), name='signin'),
    path('signup/', System.Signup.as_view(), name='signup'),
    path('signout/', System.Logout.as_view(), name='signout'),
    path('products/', System.ShowProduct.as_view(), name='show_product'),
    path('create-product/', System.CreateProduct.as_view(), name='create_product'),
    path('register-retail/', System.RegisterRetail.as_view(), name='register_retail'),
    path('register-manufactory/', System.RegisterManufactory.as_view(), name='register_manufactory'),
    path('purchase/', System.Purchase_retails.as_view(), name='purchase'),
    path('sell/', System.Sell.as_view(), name='sell'),
]