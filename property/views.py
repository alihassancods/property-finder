
# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate,logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import *
from .models import *
def logout_view(request):
    if request.user.is_authenticated:
        logout(request)  # Logs out the user
        request.session.flush()  # Clears all session data
    return redirect('home')  # Redirect to the homepage
from django.db import IntegrityError

# def signup_view(request):
#     if request.method == 'POST':
#         # Extract form data from the request
#         username = request.POST.get('username')
#         email = request.POST.get('email')
#         first_name = request.POST.get('first_name')
#         last_name = request.POST.get('last_name')
#         contact_number = request.POST.get('contact_number')
#         password1 = request.POST.get('password1')
#         password2 = request.POST.get('password2')
#         role = request.POST.get('role')

#         # Initialize an error dictionary
#         errors = {}

#         # Validate passwords
#         if password1 != password2:
#             errors['password'] = "Passwords do not match."

#         # Check if the username already exists
#         if User.objects.filter(username=username).exists():
#             errors['username'] = "This username is already taken."

#         # Additional email validation (optional)
#         if User.objects.filter(email=email).exists():
#             errors['email'] = "An account with this email already exists."

#         # If there are any errors, re-render the form with the errors
#         if errors:
#             return render(request, 'property/signup.html', {'errors': errors})

#         # Create the user
#         try:
#             user = User.objects.create_user(
#                 username=username,
#                 email=email,
#                 first_name=first_name,
#                 last_name=last_name,
#                 password=password1
#             )
#             # You can save additional user-related data here if needed
#             # For example, if you have a Profile model:
#             # Profile.objects.create(user=user, contact_number=contact_number, role=role)
#             user.save()

#             return redirect('login')  # Redirect to the login page or any other page
#         except IntegrityError:
#             errors['general'] = "An error occurred while creating your account. Please try again."
#             return render(request, 'property/signup.html', {'errors': errors})

#     # Render the signup page for GET requests
#     return render(request, 'property/signup.html')

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
            redirect_back = request.POST.get('redirect_back', None)
            if redirect_back:
                return redirect(str(redirect_back))
            else:
                return redirect('home')
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'property/login.html', {'form': form})

def agent_profile_setup_view(request):
    if not(request.user.is_authenticated):
        return redirect('home')

    if request.method == 'POST':
        form = AgentProfileForm(request.POST, request.FILES)
        if form.is_valid():
            agent = form.save(commit=False)
            agent.user = request.user
            agent.save()
            request.user.is_agent=True
            messages.success(request, "Agent profile setup completed.")
            return redirect('home')
    else:
        form = AgentProfileForm()
    return render(request, 'property/agentProfileSetup.html', {'form': form})

def buy_properties(request):
    properties = Property.objects.filter(is_for_sale=True)
    print(len(properties))
    paginator = Paginator(properties,5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    try:
        page_obj = paginator.get_page(page_number)
    except (PageNotAnInteger, ValueError):
        # If page is not an integer, deliver the first page
        page_obj = paginator.page(1)
    except EmptyPage:
        # If page is out of range, deliver the last page
        page_obj = paginator.page(paginator.num_pages)
    for property in properties:
        images = property.images.all()
        for image in images:
            print(image.image)
    
    return render(request, template_name='property/buy.html', context={'dataSet': properties,'page_obj':page_obj})
def sell_properties(request):  
    return render(request, template_name='property/sell.html')
def rent_properties(request):
    properties = Property.objects.filter(is_for_rent=True)
    paginator = Paginator(properties,5) 
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    try:
        page_obj = paginator.get_page(page_number)
    except (PageNotAnInteger, ValueError):
        # If page is not an integer, deliver the first page
        page_obj = paginator.page(1)
    except EmptyPage:
        # If page is out of range, deliver the last page
        page_obj = paginator.page(paginator.num_pages)
    for property in properties:
        images = property.images.all()
        for image in images:
            print(image.image)                                                                                      
    return render(request, template_name='property/rent.html',context={'dataSet': properties,'page_obj':page_obj})


def community_create_view(request):
    if request.user.is_authenticated:
        if request.user.is_agent:
            if request.method == 'POST':
                form = CommunityForm(request.POST)
                if form.is_valid():
                    form.save()
                    return redirect('community_list')
            else:
                form = CommunityForm()
            return render(request, 'property/community_create.html', {'form': form})
        else:
            return redirect('home')
    else:
        return redirect('login')

def commercial_properties(request): 
    properties = Property.objects.filter(property_type="commercial")
    paginator = Paginator(properties,5)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    try:
        page_obj = paginator.get_page(page_number)
    except (PageNotAnInteger, ValueError):
        # If page is not an integer, deliver the first page
        page_obj = paginator.page(1)
    except EmptyPage:
        # If page is out of range, deliver the last page
        page_obj = paginator.page(paginator.num_pages)
    for property in properties:
        images = property.images.all()
        for image in images:
            print(image.image)
    
    return render(request, template_name='property/commercial.html', context={'dataSet': properties,'page_obj':page_obj})
def agent_list(request):
    agents = Agent.objects.all()
    paginator = Paginator(agents, 5)  
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    try:
        page_obj = paginator.get_page(page_number)
    except (PageNotAnInteger, ValueError):
        # If page is not an integer, deliver the first page
        page_obj = paginator.page(1)
    except EmptyPage:
        # If page is out of range, deliver the last page
        page_obj = paginator.page(paginator.num_pages)                                                                                 
    return render(request, template_name='property/agents.html',context={'data':agents,'page_obj':page_obj})
def community_list(request):                                                                           
    communities = Community.objects.all()
    return render(request, template_name='property/communities.html',context={'data':communities})
def home_view(request):
    if request.user.is_authenticated:
        return render(request, template_name='property/home.html',context={'user':request.user})
    else:
        return render(request, template_name='property/home.html')

def property_create_view(request):
    if request.method == 'POST':
        # images = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False)
        form = PropertyForm(request.POST, request.FILES)

        if form.is_valid():
            formWhichNoOneSaved = form.save()
            images = request.FILES.getlist('images')  # Get the list of images
            for image in images:
                new_image = PropertyImage(property=formWhichNoOneSaved, image=image)
                new_image.save()
            
                

            return redirect('buy_properties')  # Replace with your property list view name
    else:
        form = PropertyForm()
    return render(request, 'property/property_create.html', {'form': form})

def community_update_view(request, pk):
    if request.user.is_authenticated:
        if request.user.is_agent:
            community_instance = Community.objects.get(id=pk)
            if request.method == 'POST':
                form = CommunityForm(request.POST, request.FILES, instance=property_instance)
                if form.is_valid():
                    form.save()
                    return redirect('community_list')  # Replace with your property list view name
            else:
                form = CommunityForm(instance=community_instance)
            return render(request, 'property/community_update.html', {'form': form})
        else:
            return redirect('buy_properties')
    else:
        return redirect('login')
def property_update_view(request, pk):
    if request.user.is_authenticated:
        if request.user.is_agent:
            property_instance = Property.objects.get(id=pk)
            if request.method == 'POST':
                form = PropertyForm(request.POST, request.FILES, instance=property_instance)
                if form.is_valid():
                    form.save()
                    return redirect('buy_properties')  # Replace with your property list view name
            else:
                form = PropertyForm(instance=property_instance)
            return render(request, 'property/property_update.html', {'form': form})
        else:
            return redirect('buy_properties')
    else:
        return redirect('login')

def property_list_view(request):
    properties = Property.objects.all()
    return render(request, 'property/property_list.html', {'properties': properties})
def community_delete_view(request, pk):
    if request.user.is_authenticated:
        if request.user.is_agent:
            community = Community.objects.get(id=pk)
            community.delete()
            return redirect('dashboard')
        else:
            return redirect('buy_properties')
    else:
        return redirect('login')
    


def property_delete_view(request, pk):
    if request.user.is_authenticated:
        if request.user.is_agent:
            property = Property.objects.get(id=pk)
            property.delete()
            return redirect('dashboard')
        else:
            return redirect('buy_properties')
    else:
        return redirect('login')
    

def property_detail_view(request, community, property_name):
    property_instance = Property.objects.filter(community__slug="hmc-community", title=property_name)
    # property_instance = Property.objects.get(id=pk)
    print(property_instance)
    return render(request, 'property/property_detail.html', {'property': property_instance})

from django.db.models import Q
from .models import Property, Community, Agent
def searchbar(request):
    return render(request, 'property/search.html')
from django.shortcuts import render
from django.db.models import Q
from .models import Property

def search_properties(request):
    search_query = request.GET.get("search_query", "").strip()
    property_type = request.GET.get("property_type", None)
    buy_or_rent = request.GET.get("buy_or_rent", None)
    beds = request.GET.get("beds", None)
    price_sort = request.GET.get("price_sort", None)

    # Get all properties
    properties = Property.objects.all()

    # Text-based search (title, description, location, community)
    if search_query:
        properties = properties.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(location__icontains=search_query) |
            Q(community__name__icontains=search_query)
        )

    # Filter by property type
    if property_type and property_type != "all":
        properties = properties.filter(property_type=property_type)

    # Filter by buy or rent
    if buy_or_rent == "buy":
        properties = properties.filter(is_for_sale=True)
    elif buy_or_rent == "rent":
        properties = properties.filter(is_for_rent=True)

    # Filter by number of bedrooms
    if beds and beds.isdigit():
        properties = properties.filter(bedrooms=int(beds))

    # Sort by price
    if price_sort == "low-high":
        properties = properties.order_by("price")
    elif price_sort == "high-low":
        properties = properties.order_by("-price")

    return render(request, "property/search-results.html", {"properties": properties})

from django.core.paginator import Paginator
from django.shortcuts import render


def dashboard(request):
    userReq = request.user
    if userReq.is_authenticated:
        if userReq.is_agent:
            agent = Agent.objects.get(user=userReq)
            print(agent)
            properties = agent.properties.all()
            communities = agent.communities.all()

            return render(request, 'property/dashboard.html', {'properties': properties,'communities':communities})
        else:
            return redirect('home')
    else:
        return redirect('login')
    return render(request, 'property/dashboard.html')
def inbox(request):                                                                                            
    return render(request, 'property/inbox.html')
def community_detail_view(request, pk):
    community_instance = Community.objects.get(id=pk)
    return render(request, 'property/community_detail.html', {'community': community_instance})