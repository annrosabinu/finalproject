from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import UserProfile, Package, ChatRequest
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
import random
import string

# Registration View
def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = ''.join(random.choices(string.digits, k=6))
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()

        profile = UserProfile(
            user=user,
            gender=request.POST['gender'],
            height=request.POST['height'],
            job_designation=request.POST['job_designation'],
            job_place=request.POST['job_place'],
            district=request.POST['district'],
            religion=request.POST['religion'],
            caste=request.POST['caste'],
            marriage_level=request.POST['marriage_level'],
            mother_name=request.POST['mother_name'],
            father_name=request.POST['father_name'],
            sibling_name=request.POST['sibling_name'],
            sibling_status=request.POST['sibling_status'],
            profile_pictures=request.FILES['profile_pictures'],
            package=Package.objects.first(),  # Example: Set to first available package
            expiry_date="2025-01-01"  # Example: Set expiry date
        )
        profile.save()

        send_mail(
            'Your Matrimony Registration',
            f'Your registration is successful. Your Member ID is {user.id} and password is {password}',
            'admin@matrimony.com',
            [email],
            fail_silently=False,
        )

        return redirect('payment')  # Redirect to payment page

    return render(request, 'register.html')

# Admin approval view
def admin_approval(request, user_id):
    user = UserProfile.objects.get(user_id=user_id)
    user.is_active = True  # Approve user to login
    user.save()
    return redirect('admin_dashboard')

# Search view
def search(request):
    query = request.GET.get('query')
    users = UserProfile.objects.filter(user__username__contains=query)
    return render(request, 'search.html', {'users': users})

# Payment view
def payment(request):
    if request.method == 'POST':
        # Handle payment logic here
        return render(request, 'user/registration_complete.html', {'message': 'Registration Complete, and your profile is checked and verified by the admin shortly'})

    return render(request, 'payment.html')

def send_chat_request(request, user_id):
    receiver = User.objects.get(id=user_id)
    sender = request.user

    # Check if there is an existing active chat request between sender and receiver
    if not ChatRequest.objects.filter(sender=sender, receiver=receiver, is_active=True).exists():
        ChatRequest.objects.create(sender=sender, receiver=receiver, message="Hi, I'd like to chat!")
    
    return redirect('chat_list') 

def accept_chat_request(request, chat_id):
    chat_request = ChatRequest.objects.get(id=chat_id)
    chat_request.is_accepted = True
    chat_request.save()
    
    return redirect('chat_detail', chat_id=chat_request.id)  # Redirect to the chat details page

def reject_chat_request(request, chat_id):
    chat_request = ChatRequest.objects.get(id=chat_id)
    chat_request.is_active = False
    chat_request.save()

    return redirect('chat_list')  # Redirect to the page listing the user's chat requests

def chat_list(request):
    chat_requests = ChatRequest.objects.filter(receiver=request.user, is_active=True)
    return render(request, 'chat/chat_list.html', {'chat_requests': chat_requests})

def chat_detail(request, chat_id):
    chat = ChatRequest.objects.get(id=chat_id)

    if chat.is_accepted:
        # Logic to retrieve and display the actual conversation between sender and receiver
        messages = ChatRequest.objects.filter(sender=chat.sender, receiver=chat.receiver) | \
                  ChatRequest.objects.filter(sender=chat.receiver, receiver=chat.sender)
        messages = messages.order_by('timestamp')
        
        return render(request, 'chat/chat_detail.html', {'chat': chat, 'messages': messages})
    else:
        # If the chat request hasn't been accepted, show a message
        return render(request, 'chat/chat_waiting.html', {'chat': chat})

def send_message(request, chat_id):
    chat = ChatRequest.objects.get(id=chat_id)
    if request.method == 'POST':
        message = request.POST['message']
        ChatRequest.objects.create(
            sender=request.user,
            receiver=chat.receiver if chat.sender == request.user else chat.sender,
            message=message,
        )
        return redirect('chat_detail', chat_id=chat.id)

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_superuser:
                return redirect('admin_dashboard')  # Redirect to admin dashboard if superuser
            else:
                return redirect('user_dashboard')  # Redirect to user dashboard
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'login.html')

from django.contrib.auth.decorators import login_required
from .models import Notification, ChatRequest, UserProfile

@login_required
def user_dashboard(request):
    user_profile = UserProfile.objects.get(user=request.user)
    notifications = Notification.objects.filter(user=request.user)  # Assuming notifications model exists
    chat_requests = ChatRequest.objects.filter(receiver=request.user, is_active=True)

    return render(request, 'user/dashboard.html', {
        'profile': user_profile,
        'notifications': notifications,
        'chat_requests': chat_requests,
    })

@login_required
def view_profile(request):
    user_profile = UserProfile.objects.get(user=request.user)
    return render(request, 'user/view_profile.html', {'profile': user_profile})


@login_required
def edit_profile(request):
    user_profile = UserProfile.objects.get(user=request.user)
    if request.method == 'POST':
        user_profile.gender = request.POST['gender']
        user_profile.height = request.POST['height']
        user_profile.job_designation = request.POST['job_designation']
        # Update other fields
        user_profile.save()
        return redirect('view_profile')
    
    return render(request, 'user/edit_profile.html', {'profile': user_profile})


@login_required
def print_all_details(request):
    user_profile = UserProfile.objects.get(user=request.user)
    return render(request, 'user/print_all_details.html', {'profile': user_profile})


from .models import Notification, ChatRequest

def payment(request):
    if request.method == 'POST':
        # Handle payment logic here
        # Assuming payment is successful:
        Notification.objects.create(
            user=request.user,
            message='Your payment was successful!',
        )
        return redirect('registration_complete')
    return render(request, 'payment.html')


from django.contrib.auth.decorators import user_passes_test
from .models import UserProfile

@user_passes_test(lambda u: u.is_superuser)  # Ensure only superuser can access
def admin_dashboard(request):
    pending_users = UserProfile.objects.filter(is_active=False)  # Get users awaiting approval
    return render(request, 'admin/admin_dashboard.html', {'pending_users': pending_users})


from django.shortcuts import redirect
from .models import UserProfile

@user_passes_test(lambda u: u.is_superuser)  # Ensure only superuser can access
def admin_approval(request, user_id):
    user = UserProfile.objects.get(user_id=user_id)
    user.is_active = True  # Approve user to login
    user.save()
    return redirect('admin_dashboard')


from django.shortcuts import redirect

def home(request):
    return redirect('login')  # Redirect to the login page directly



from .filters import UserProfileFilter

def search(request):
    user_filter = UserProfileFilter(request.GET, queryset=UserProfile.objects.all())
    return render(request, 'user/search.html', {'filter': user_filter})


