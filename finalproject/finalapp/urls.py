from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    # Registration and Payment URLs
    path('register/', views.register, name='register'),

    # Chat-related URLs
    path('chat/', views.chat_list, name='chat_list'),
    path('chat/<int:chat_id>/', views.chat_detail, name='chat_detail'),
    path('chat/send/<int:user_id>/', views.send_chat_request, name='send_chat_request'),
    path('chat/accept/<int:chat_id>/', views.accept_chat_request, name='accept_chat_request'),
    path('chat/reject/<int:chat_id>/', views.reject_chat_request, name='reject_chat_request'),
    path('chat/send_message/<int:chat_id>/', views.send_message, name='send_message'),

    path('login/', views.login_view, name='login'),
    path('dashboard/', views.user_dashboard, name='user_dashboard'),
    path('profile/view/', views.view_profile, name='view_profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('profile/print_all/', views.print_all_details, name='print_all_details'),
    path('payment/', views.payment, name='payment'),
    path('search/', views.search, name='search'),
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/approve/<int:user_id>/', views.admin_approval, name='admin_approval'),
]
