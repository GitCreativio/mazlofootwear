
from constants import *
from django.contrib import messages
import random
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import get_user_model, login as auth_login, logout
from .forms import UserProfileForm, ProfilePictureForm
from .models import UserProfile, Address
from Order.models import Order
from django.urls import reverse
from django.core.cache import cache


CACHE_TIMEOUT = 300  # seconds (5 minutes)

# Create your views here.

def user_login(request):
    """
    Handle user login via email-based OTP authentication.

    If the user exists, generate and send an OTP via email.
    If the user does not exist, create a new user and send OTP.
    Redirect to the OTP verification page after OTP is sent.
    """
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        email = request.POST.get('email')
        request.session['email'] = email
        username = request.POST.get('username')

        user = get_user_model().objects.filter(email=email).first()

        otp = ''.join(random.choices('0123456789', k=4))
        request.session['otp'] = otp
        mail_subject = 'Quick! Your Mazlo Footwear OTP is Waiting for You!'
        message = f'Your OTP is {otp}. Do not share this code with anyone.'
        send_mail(mail_subject, message, 'your_email@example.com', [email])

        if not user:
            user = get_user_model().objects.create_user(username=username, email=email)

        return redirect('otp_verify')

    return render(request, 'login.html')


def otp_verify(request):
    """
    Verify the OTP entered by the user.

    If correct, authenticate and log in the user.
    If incorrect, display an error message.
    """
    if request.user.is_authenticated:
        return redirect('home')
    
    if 'otp' not in request.session:
        return redirect('login')
    
    if request.method == 'POST':
        entered_otp = ''.join([
            request.POST.get('otp1', ''),
            request.POST.get('otp2', ''),
            request.POST.get('otp3', ''),
            request.POST.get('otp4', '')
        ])
        
        stored_otp = request.session.get('otp')

        if entered_otp == stored_otp:
            del request.session['otp']
            email = request.session['email']

            if not email:
                messages.error(request, EMAIL_NOT_FOUND)
                return redirect('login')
            
            user = get_object_or_404(get_user_model(), email=email)
            auth_login(request, user)
            messages.success(request, LOGIN_SUCCESS)

            mail_subject = 'Welcome to Mazlo Footwear!'
            mail_message = (
                'Welcome to Mazlo Footwear! Your login has been successfully completed. '
                'Step into a world of style and comfort with our exclusive collections. '
                'Happy shopping!'
            )
            send_mail(mail_subject, mail_message, 'your_email@example.com', [email])

            return redirect('home')
        else:
            messages.error(request, INVALID_OTP)

    return render(request, 'otp.html')


def resend_otp(request):
    """
    Resend a new OTP to the user's email stored in session.

    Used when the user requests to resend the OTP.
    """
    email = request.session.get('email')
    
    if not email:
        messages.error(request, UNABLE_RESEND_OTP)
        return redirect('login')

    otp = ''.join(random.choices('0123456789', k=4))
    request.session['otp'] = otp

    mail_subject = 'Resend OTP – Mazlo Footwear'
    message = f'Your new OTP is {otp}. Do not share this code with anyone.'
    send_mail(mail_subject, message, 'your_email@example.com', [email])

    messages.success(request, NEW_OTP)
    return redirect('otp_verify')


def profile(request):
    """
    Display and edit the authenticated user’s profile.

    - Redirects anonymous users to home with ?next=profile.
    - Caches UserProfile, recent orders, and addresses for CACHE_TIMEOUT seconds.
    - Handles profile updates via POST and displays success messages.
    """
    if not request.user.is_authenticated:
        return redirect(f"{reverse('home')}?next=profile")

    user = request.user

    # Cache user profile
    profile_cache_key = f"user_profile_{user.id}"
    profile = cache.get(profile_cache_key)
    if profile is None:
        profile, created = UserProfile.objects.get_or_create(user=user)
        cache.set(profile_cache_key, profile, CACHE_TIMEOUT)

    # Cache recent orders
    orders_cache_key = f"recent_orders_{user.id}"
    recent_orders = cache.get(orders_cache_key)
    if recent_orders is None:
        recent_orders = list(Order.objects.filter(user=user)
                             .order_by('-order_date')[:3])
        cache.set(orders_cache_key, recent_orders, CACHE_TIMEOUT)

    # Cache addresses
    addresses_cache_key = f"addresses_{user.id}"
    addresses = cache.get(addresses_cache_key)
    if addresses is None:
        addresses = list(Address.objects.filter(user=user))
        cache.set(addresses_cache_key, addresses, CACHE_TIMEOUT)

    if request.method == 'POST':
        user_form = UserProfileForm(request.POST, instance=user)
        profile_form = ProfilePictureForm(
            request.POST, request.FILES, instance=profile
        )
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()

            # Invalidate caches so updates show immediately
            cache.delete(profile_cache_key)

            messages.success(request, "Profile updated successfully!")
            return redirect('profile')
    else:
        user_form = UserProfileForm(instance=user)
        profile_form = ProfilePictureForm(instance=profile)

    profile_picture_url = profile.profile_picture.url if profile.profile_picture else ''

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'profile_picture_url': profile_picture_url,
        'profile': profile,
        'recent_orders': recent_orders,
        'addresses': addresses,
    }
    return render(request, 'profile.html', context)


def user_logout(request):
    """
    Log out the current user and redirect to the home page.
    """
    if request.user.is_authenticated:
        logout(request)
    return redirect('home')


def add_address(request):
    """
    Add a new Address for the authenticated user via POST,
    then invalidate the address cache.
    """
    if request.method == 'POST' and request.user.is_authenticated:
        address = Address(
            user=request.user,
            address=request.POST['address'],
            city=request.POST['city'],
            state=request.POST['state'],
            zip_code=request.POST['zip_code'],
            phone_number=request.POST['phone_number']
        )
        address.save()

        # Invalidate address cache so new address appears immediately
        cache.delete(f"addresses_{request.user.id}")

        messages.success(request, "Address added successfully!")
    return redirect('profile')


def delete_address(request, address_id):
    """
    Delete the specified Address for the authenticated user,
    then invalidate the address cache.
    """
    try:
        address = Address.objects.get(id=address_id, user=request.user)
        address.delete()
        cache.delete(f"addresses_{request.user.id}")
        messages.success(request, "Address deleted successfully!")
    except Address.DoesNotExist:
        messages.error(request, "Address not found.")
    return redirect('profile')
