from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.conf import *
from multiselectfield import MultiSelectField

class User(AbstractUser):
    ROLES = [
        ('buyer', 'Buyer'),
        ('agent', 'Agent'),
    ]
    role = models.CharField(max_length=10, choices=ROLES, default='buyer')
    contact_number = models.CharField(max_length=15, blank=True, null=True)
    is_agent = models.BooleanField(default=False)  # Determines if the user is an agent

    # Add unique related_name attributes to avoid clashes
    groups = models.ManyToManyField(
        Group,
        related_name="custom_user_set",  # Unique related_name
        blank=True,
        help_text="The groups this user belongs to.",
    )
    user_permissions = models.ManyToManyField(  
        Permission,
        related_name="custom_user_permissions_set",  # Unique related_name
        blank=True,
        help_text="Specific permissions for this user.",
    )

class Agent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="agent_profile")
    full_name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    whatsapp_number = models.CharField(max_length=15, blank=True, null=True)
    profile_picture = models.ImageField(upload_to="agents/profile_pictures", blank=True, null=True)
    about = models.TextField(blank=True, null=True)
    email = models.EmailField(unique=True)
    languages = models.CharField(max_length=200, help_text="Comma-separated list of languages.")
    properties_listed = models.IntegerField(default=0)
    communities_active_in = models.IntegerField(default=0)

    def __str__(self):
        return self.full_name

class Community(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    images = models.ImageField(upload_to="communities/images")
    agent = models.ForeignKey(Agent, related_name="communities", on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField(null=True, blank=True,default="No description")
    def properties_count(self):
        return self.properties.count()

    def __str__(self):
        return self.name

class Property(models.Model):
    PROPERTY_TYPE_CHOICES = [
        ('residential', 'Residential'),
        ('commercial', 'Commercial'),
    ]

    FACILITY_CHOICES = [
        ('villa', 'Villa'),
        ('compound', 'Compound'),
        ('apartment', 'Apartment'),
        ('hotel_apartment', 'Hotel Apartment'),
        ('duplex', 'Duplex'),
    ]

    FACILITIES = [
        ('central_ac', 'Central A/C'),
        ('maids_room', "Maids Room"),
        ('balcony', "Balcony"),
        ('shared_pool', "Shared Pool"),
        ('shared_spa', "Shared Spa"),
        ('shared_gym', "Shared Gym"),
        ('concierge_service', "Concierge Service"),
        ('covered_parking', "Covered Parking"),
        ('view_of_water', "View of Water"),
        ('view_of_landmark', "View of Landmark"),
        ('pets_allowed', "Pets Allowed"),
        ('study', "Study"),
        ('private_garden', "Private Garden"),
        ('private_pool', "Private Pool"),
        ('private_gym', "Private Gym"),
        ('private_jacuzzi', "Private Jacuzzi"),
        ('built_in_wardrobes', "Built in Wardrobes"),
        ('walk_in_closet', "Walk-in Closet"),
        ('built_in_kitchen_appliances', "Built in Kitchen Appliances"),
        ('maid_service', "Maid Service"),
        ('childrens_play_area', "Children's Play Area"),
        ('childrens_pool', "Children's Pool"),
        ('barbecue_area', "Barbecue Area"),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    location = models.CharField(max_length=100)
    property_type = models.CharField(max_length=50, choices=PROPERTY_TYPE_CHOICES)
    facility_type = models.CharField(max_length=50, choices=FACILITY_CHOICES)
    size = models.DecimalField(max_digits=10, decimal_places=2, help_text="Size in square feet.")
    bedrooms = models.PositiveIntegerField()
    bathrooms = models.PositiveIntegerField()
    facilities = MultiSelectField(max_length=500,choices=FACILITIES, blank=True, null=True)
    community = models.ForeignKey(Community, related_name="properties", on_delete=models.SET_NULL, null=True, blank=True)
    agent = models.ForeignKey(Agent, related_name="properties", on_delete=models.SET_NULL, null=True, blank=True)
    is_for_sale = models.BooleanField(default=False)
    is_for_rent = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.title

class PropertyImage(models.Model):
    property = models.ForeignKey(Property, related_name='images', on_delete=models.CASCADE)
    image = models.FileField(upload_to="properties/images")

    def __str__(self):
        return f"Image for {self.property.title}"

