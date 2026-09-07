import django_filters
from .models import UserProfile

class UserProfileFilter(django_filters.FilterSet):
    member_id = django_filters.CharFilter(field_name='user__id', lookup_expr='exact', label="Member ID")
    username = django_filters.CharFilter(field_name='user__username', lookup_expr='icontains', label="Username")

    class Meta:
        model = UserProfile
        fields = ['member_id', 'username']
