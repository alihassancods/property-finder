
# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import *
from .models import *

def signup_view(request):
    if request.method == 'POST':
        form = UserSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            role = form.cleaned_data['role']
            login(request, user)
            print(role)
            if role == "agent":
                return redirect('profile_setup')
            else:
                return redirect('home')
        else:
            messages.error(request, "Error in form submission.")
    else:
        form = UserSignupForm()
    return render(request, 'property/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'property/login.html', {'form': form})

def agent_profile_setup_view(request):
    if not(request.user.is_authenticated):
        print("hello")
        return redirect('home')

    if request.method == 'POST':
        form = AgentProfileForm(request.POST, request.FILES)
        if form.is_valid():
            agent = form.save(commit=False)
            agent.user = request.user
            agent.save()
            messages.success(request, "Agent profile setup completed.")
            return redirect('home')
    else:
        form = AgentProfileForm()
    return render(request, 'property/agentProfileSetup.html', {'form': form})

def buy_properties(request):
    properties = Property.objects.filter(is_for_sale=True)
    for property in properties:
        images = property.images.all()
        for image in images:
            print(image.image)
    
    return render(request, template_name='property/buy.html', context={'dataSet': properties})
def sell_properties(request):  
    return render(request, template_name='property/sell.html')
def rent_properties(request):
    properties = Property.objects.filter(is_for_rent=True)
    for property in properties:
        images = property.images.all()
        for image in images:
            print(image.image)                                                                                      
    return render(request, template_name='property/rent.html',context={'dataSet': properties})
def commercial_properties(request):                                                                                     
    return render(request, template_name='property/commercial.html')
def agent_list(request):                                                                                 
    return render(request, template_name='property/agents.html')
def community_list(request):                                                                           
    return render(request, template_name='property/communities.html')
def home_view(request):
    return render(request, template_name='property/home.html')

def property_create_view(request):
    if request.method == 'POST':
        images = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False)
        if form.is_valid():
            form.save()
            images = request.FILES.getlist('images')  # Get the list of images
            for image in images:
                PropertyImage.objects.create(property=property_instance, image=image)

            return redirect('buy_properties')  # Replace with your property list view name
    else:
        form = PropertyForm()
    return render(request, 'property/property_create.html', {'form': form})

def property_update_view(request, pk):
    property_instance = get_object_or_404(Property, pk=pk)
    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES, instance=property_instance)
        if form.is_valid():
            form.save()
            return redirect('buy_properties')  # Replace with your property list view name
    else:
        form = PropertyForm(instance=property_instance)
    return render(request, 'property/property_update.html', {'form': form})

def property_list_view(request):
    properties = Property.objects.all()
    return render(request, 'property/property_list.html', {'properties': properties})

def property_detail_view(request, pk):
    property_instance = get_object_or_404(Property, pk=pk)
    return render(request, 'property/property_detail.html', {'property': property_instance})

from django.db.models import Q
from .models import Property, Community, Agent
def searchbar(request):
    return render(request, 'property/search.html')
def search_properties(request):
    # Get the search inputs from the GET request
    search_query = request.GET.get("search_query", "").strip()
    property_type = request.GET.get("property_type", "")
    buy_or_rent = request.GET.get("buy_or_rent", "")
    beds = request.GET.get("beds", "")
    price_sort = request.GET.get("price_sort", "")
    
    # Base queryset for properties
    properties = Property.objects.all()

    # Filter by search query
    if search_query:
        properties = properties.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(location__icontains=search_query) |
            Q(community__name__icontains=search_query)
        )
    
    # Filter by property type
    if property_type and property_type != "property-type":
        properties = properties.filter(facility_type=property_type)
    
    # Filter by buy or rent
    if buy_or_rent == "buy":
        properties = properties.filter(is_for_sale=True)
    elif buy_or_rent == "rent":
        properties = properties.filter(is_for_rent=True)
    
    # Filter by bedrooms
    if beds and beds != "beds-baths":
        try:
            beds_count = int(beds[0])  # Extract the number of beds
            properties = properties.filter(bedrooms=beds_count)
        except ValueError:
            pass  # Ignore invalid input
    
    # Sort by price
    if price_sort == "low-high":
        properties = properties.order_by("price")
    elif price_sort == "high-low":
        properties = properties.order_by("-price")
    
    # Render the search results
    return render(request, "property/search-results.html", {"properties": properties})
