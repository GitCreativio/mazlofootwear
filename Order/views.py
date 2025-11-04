from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.db import transaction
from django.db.models import Sum, F
from django.contrib import messages
from django.views.decorators.cache import never_cache
from django.core.cache import cache

from Shop.models import ProductVariant
from .models import Cart, Order, OrderItem
from .forms import CheckoutForm, ReturnForm

@transaction.atomic
def add_to_cart(request):
    """
    Adds a product variant to the user's cart.

    - Ensures the user is authenticated.
    - Validates quantity and stock availability.
    - If the item exists, updates the quantity; else creates a new cart item.
    """
    if not request.user.is_authenticated:
        return redirect(f"{reverse('home')}?next=add-to-cart")

    if request.method == 'POST':
        variant_id = request.POST.get('variant_id')
        quantity = int(request.POST.get('quantity', 1))

        try:
            variant = ProductVariant.objects.get(id=variant_id)

            if quantity <= 0:
                messages.error(request, "Invalid quantity")
                return redirect(request.META.get('HTTP_REFERER', '/'))

            if quantity > variant.stock:
                messages.error(request, f"Only {variant.stock} items available in stock")
                return redirect(request.META.get('HTTP_REFERER', '/'))

            cart_item, created = Cart.objects.get_or_create(
                user=request.user,
                variant=variant,
                defaults={'quantity': quantity}
            )

            if not created:
                new_quantity = cart_item.quantity + quantity
                if new_quantity > variant.stock:
                    messages.error(request, f"Total quantity exceeds available stock ({variant.stock})")
                    return redirect(request.META.get('HTTP_REFERER', '/'))

                cart_item.quantity = new_quantity
                cart_item.save()
                messages.success(request, "Cart quantity updated successfully")
            else:
                messages.success(request, "Item added to cart successfully")

            return redirect('cart')

        except ProductVariant.DoesNotExist:
            messages.error(request, "Product variant not found")
            return redirect('home')

    return redirect('home')


@never_cache
def cart(request):
    """
    Displays the user's cart with all added items and total cost.
    """
    if not request.user.is_authenticated:
        return redirect(f"{reverse('home')}?next=cart")

    cart_items = Cart.objects.filter(user=request.user)\
        .select_related('variant__product', 'variant__color', 'variant__size')\
        .prefetch_related('variant__product__images')

    total = sum(item.total_price for item in cart_items)

    context = {
        'cart_items': cart_items,
        'total': total
    }
    return render(request, 'cart.html', context)


def update_cart(request, item_id):
    """
    Updates the quantity of a cart item.

    - Checks against stock availability.
    - Updates cart if within allowed limits.
    """
    if request.method == 'POST':
        cart_item = get_object_or_404(Cart, id=item_id, user=request.user)
        new_quantity = int(request.POST.get('quantity', 1))

        if new_quantity > cart_item.variant.stock:
            messages.error(request, "Exceeds available stock")
        else:
            cart_item.quantity = new_quantity
            cart_item.save()
            messages.success(request, "Cart updated successfully")

        return redirect('cart')
    return redirect('cart')


def remove_from_cart(request, item_id):
    """
    Removes an item from the user's cart.
    """
    if request.method == 'GET':
        cart_item = get_object_or_404(Cart, id=item_id, user=request.user)
        cart_item.delete()
        messages.success(request, "Item removed from cart")
    return redirect('cart')


@transaction.atomic
def process_checkout(request):
    """
    Processes the checkout operation:

    - Creates an order from selected cart items.
    - Deducts product stock accordingly.
    - Saves order and order items.
    """
    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == 'POST':
        try:
            selected_ids = list(map(int, request.POST.get('selected_items', '').split(',')))
        except ValueError:
            messages.error(request, "Invalid selection")
            return redirect('cart')

        cart_items = Cart.objects.filter(
            id__in=selected_ids,
            user=request.user
        ).select_related('variant__product', 'variant')

        if not cart_items.exists():
            messages.error(request, "No valid items selected")
            return redirect('cart')

        form = CheckoutForm(request.POST)
        if form.is_valid():
            order = Order.objects.create(
                user=request.user,
                total_amount=sum(item.total_price for item in cart_items),
                **form.cleaned_data
            )

            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    variant=item.variant,
                    quantity=item.quantity,
                    price=item.variant.price
                )

                item.variant.stock -= item.quantity
                item.variant.save()

            cart_items.delete()
            messages.success(request, "Order placed successfully!")
            return redirect('order_detail', order_id=order.id)

        messages.error(request, "Please correct the errors below")
        return render(request, 'cart.html', {
            'form': form,
            'cart_items': Cart.objects.filter(user=request.user)
        })

    return redirect('cart')


def order_detail(request, order_id):
    """
    Displays details for a specific order.
    """
    if not request.user.is_authenticated:
        return redirect(f"{reverse('home')}?next=cart")

    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'order_detail.html', {'order': order})


def my_orders(request):
    """
    Lists all orders placed by the currently logged-in user.
    """
    if not request.user.is_authenticated:
        return redirect(f"{reverse('home')}?next=cart")

    orders = Order.objects.filter(user=request.user)
    return render(request, 'orders.html', {'orders': orders})


def cancel_order(request, pk):
    """
    Cancels an order if it's in 'Processing' status.
    """
    order = Order.objects.get(pk=pk, user=request.user)
    if order.order_status == 'Processing':
        order.order_status = 'Cancelled'
        order.save()
    return redirect('my_orders')


def initiate_return(request, pk):
    """
    Initiates a return request for a delivered order.

    - Validates delivery status.
    - Accepts return form submission.
    - Changes order status to 'Returned'.
    """
    order = get_object_or_404(Order, pk=pk, user=request.user)

    if order.order_status != 'Delivered':
        messages.error(request, "Only delivered orders can be returned.")
        return redirect('my_orders')

    if request.method == 'POST':
        form = ReturnForm(request.POST)
        if form.is_valid():
            return_request = form.save(commit=False)
            return_request.order = order
            return_request.user = request.user
            return_request.save()

            order.order_status = 'Returned'
            order.save()

            messages.success(request, f"Return request for Order #{order.id} has been submitted successfully.")
            return redirect('my_orders')
    else:
        form = ReturnForm()

    return render(request, 'return_form.html', {
        'form': form,
        'order': order
    })


def return_order(request, pk):
    """
    Marks a delivered order as returned.
    """
    order = Order.objects.get(pk=pk, user=request.user)
    if order.order_status == 'Delivered':
        order.order_status = 'Returned'
        order.save()
    return redirect('my_orders')
