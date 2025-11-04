from . import views
from django.urls import path

urlpatterns = [
    # View the user's cart
    path('cart/', views.cart, name='cart'),

    # Add an item to the cart
    path('cart/add/', views.add_to_cart, name='add_to_cart'),

    # Update quantity of a specific cart item
    path('cart/update/<int:item_id>/', views.update_cart, name='update_cart'),

    # Remove an item from the cart
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),

    # Process the checkout of selected cart items
    path('checkout/', views.process_checkout, name='process_checkout'),

    # View details of a specific order
    path('orders/<int:order_id>/', views.order_detail, name='order_detail'),

    # Cancel an order (if it is still processing)
    path('cancel-order/<int:pk>/', views.cancel_order, name='cancel_order'),

    # Initiate a return request for a delivered order
    path('order/<int:pk>/return/', views.initiate_return, name='initiate_return'),

    # Mark an order as returned (simplified logic)
    path('return-order/<int:pk>/', views.return_order, name='return_order'),

    # List all orders made by the user
    path('my-orders/', views.my_orders, name='my_orders'),
]
