from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('addtoshopcart/<int:id>', views.addtoshopcart, name='addtoshopcart'),   
    path('updateshopcart/<int:id>', views.updateshopcart, name='updateshopcart'),
    path('deletefromcart/<int:id>', views.deletefromcart, name='deletefromcart'),
    path('orderproduct/', views.orderproduct, name='orderproduct'),
    path('order-completed/', views.order_completed, name="order-completed")
]