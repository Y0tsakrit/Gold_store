from django.urls import path
from .views import System, Deposit

urlpatterns = [
    # Authentication routes
    path('signin/', System.Signin.as_view(), name='signin'),
    path('signup/', System.Signup.as_view(), name='signup'),
    path('signout/', System.Logout.as_view(), name='logout'),
    
    # Product management routes
    path('products/', System.ShowProduct.as_view(), name='show_product'),
    path('create-product/', System.CreateProduct.as_view(), name='create_product'),
    
    # User registration routes
    path('register-retail/', System.RegisterRetail.as_view(), name='register_retail'),
    path('register-manufactory/', System.RegisterManufactory.as_view(), name='register_manufactory'),
    path('manufactories/', System.Show_list_manufactory.as_view(), name='show_list_manufactory'),
    
    # Transaction routes
    path('purchase-retail/', System.Purchase_retails.as_view(), name='purchase_retail'),
    path('purchase-customer/', System.Purchase_customer.as_view(), name='purchase_customer'),
    path('sell/', System.Sell.as_view(), name='sell'),
    path('deposit/', Deposit.as_view(), name='deposit'),
    
    # User inventory and transaction routes
    path('inventory/', System.Show_item_inventory.as_view(), name='show_inventory'),
    path('transactions/', System.Show_item_transaction.as_view(), name='show_transactions'),
    path('retail-products/', System.Show_item_sell.as_view(), name='show_item_sell'),
]