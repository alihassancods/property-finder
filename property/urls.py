from django.urls import path
from .views import *

urlpatterns = [
    path('', home_view, name='home'),
    path('signup/', signup_view, name='signup'),
    path('profile_setup/', agent_profile_setup_view, name='profile_setup'),
    path('login/', login_view, name='login'),
    path('buy/', buy_properties, name='buy_properties'),
    path('sell/', sell_properties, name='sell_properties'),
    path('rent/', rent_properties, name='rent_properties'),
    path('commercial/', commercial_properties, name='commercial_properties'),
    path('agents/', agent_list, name='agent_list'),
    path('communities/', community_list, name='community_list'),
    path('property/create/', property_create_view, name='property_create'),
    path('property/update/<int:pk>/', property_update_view, name='property_update'),
    path('property/list/', property_list_view, name='property_list'),  # Add this line
    path('property/<int:pk>/', property_detail_view, name='property_detail'),
    path('searchbar/', searchbar, name='searchbar'),
    path('search/', search_properties, name='search'),
    
]
