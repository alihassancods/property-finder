from django.contrib import admin
from .models import User, Property, Agent, Community,PropertyImage
class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    extra = 1
# Custom User Admin
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'is_agent', 'contact_number')
    list_filter = ('role', 'is_agent')
    search_fields = ('username', 'email', 'contact_number')
# Property Admin
@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('title', 'location', 'slug','price', 'property_type', 'facility_type', 'agent', 'is_for_sale', 'is_for_rent')
    list_filter = ('property_type', 'facility_type', 'is_for_sale', 'is_for_rent')
    search_fields = ('title', 'location', 'description')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [PropertyImageInline]

    def agent_name(self, obj):
        return obj.agent.full_name if obj.agent else 'No Agent'
    agent_name.short_description = 'Agent'

# Agent Admin
@admin.register(Agent)
class AgentAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'phone', 'country', 'properties_listed', 'communities_active_in')
    search_fields = ('full_name', 'email', 'phone', 'country')
# Community Admin
@admin.register(Community)
class CommunityAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'properties_count','slug')
    search_fields = ('name', 'location')
    prepopulated_fields = {'slug': ('name',)}

    def properties_count(self, obj):
        return obj.properties.count()
    properties_count.short_description = 'Properties Count'

"""
make models.py file for the django project regarding webapp of freelance platform. The user are of two types freelancer and employer. Freelancer has profile having profile picture,description,displayName,username,gigs having data inside it to be shown in analytics, the data is impressions,clicks and sales along with monthly data to be used in graph, also the top keywords of the gig. Gig has thumbnail, title, skills to be used in gig,description,price of gig and the choice that its fixed price or hourly price.
"""