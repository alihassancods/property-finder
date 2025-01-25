import os
import django
from faker import Faker
from decimal import Decimal

from django.utils.text import slugify
from property.models import User, Agent, Community, Property, PropertyImage

fake = Faker()

# Create users and agents
agents = []
for i in range(15):
    username = fake.unique.user_name()
    user = User.objects.create_user(
        username=username,
        password="password123",
        role="agent",
        contact_number=fake.phone_number(),
    )
    agent = Agent.objects.create(
        user=user,
        profile_picture="agents/profile_pictures/levi.webp",
        full_name=fake.name(),
        country=fake.country(),
        phone=fake.phone_number(),
        whatsapp_number=fake.phone_number(),
        about=fake.text(max_nb_chars=200),
        email=fake.unique.email(),
        languages=fake.language_name(),
    )
    agents.append(agent)

# Create communities
communities = []
for i in range(30):
    community = Community.objects.create(
        name=fake.city(),
        location=fake.address(),
        images="agents/profile_pictures/levi.webp",
        agent=agents[i % len(agents)],
        description=fake.text(max_nb_chars=300),
        slug=slugify(fake.unique.slug()),
    )
    communities.append(community)

# Create properties
property_types = ["residential", "commercial"]
facility_types = ["villa", "apartment", "compound"]
for i in range(100):
    property = Property.objects.create(
        title=fake.sentence(nb_words=4),
        description=fake.text(max_nb_chars=300),
        price=Decimal(fake.random_int(min=100000, max=1000000)),
        location=fake.address(),
        slug=slugify(fake.unique.slug()),
        property_type=fake.random.choice(property_types),
        facility_type=fake.random.choice(facility_types),
        size=Decimal(fake.random_int(min=1000, max=5000)),
        bedrooms=fake.random_int(min=1, max=5),
        bathrooms=fake.random_int(min=1, max=3),
        community=communities[i % len(communities)],
        agent=agents[i % len(agents)],
        is_for_sale=(i % 2 == 0),
        is_for_rent=(i % 2 != 0),
    )
    # Add property image
    PropertyImage.objects.create(property=property, image="agents/profile_pictures/levi.webp")

print("Dummy data created successfully!")
