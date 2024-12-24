import random
from faker import Faker
from property.models import User, Property, PropertyImage, Agent, Community

# Initialize Faker
fake = Faker()

# Create dummy data
def populate_users(num_users=20):
    roles = ['buyer', 'seller', 'agent']
    for _ in range(num_users):
        user = User.objects.create_user(
            username=fake.user_name(),
            email=fake.email(),
            password='password123',
            role=random.choice(roles),
            contact_number=fake.phone_number(),
        )
        print(f"Created User: {user.username}")

def populate_agents(num_agents=10):
    for _ in range(num_agents):
        agent = Agent.objects.create(
            full_name=fake.name(),
            email=fake.unique.email(),
            phone=fake.phone_number(),
            company_name=fake.company(),
        )
        print(f"Created Agent: {agent.full_name}")

def populate_communities(num_communities=5):
    for _ in range(num_communities):
        community = Community.objects.create(
            name=fake.city(),
            location=fake.address(),
        )
        print(f"Created Community: {community.name}")

def populate_properties(num_properties=30):
    property_types = ['residential', 'commercial']
    for _ in range(num_properties):
        property = Property.objects.create(
            title=fake.catch_phrase(),
            description=fake.text(),
            price=round(random.uniform(100000, 5000000), 2),
            location=fake.city(),
            property_type=random.choice(property_types),
            is_for_sale=random.choice([True, False]),
            is_for_rent=random.choice([True, False]),
        )
        print(f"Created Property: {property.title}")

        # Add images to the property
        for _ in range(random.randint(1, 5)):  # 1 to 5 images per property
            image = PropertyImage.objects.create(
                property=property,
                image=fake.file_path(extension='jpg'),  # Fake file path for placeholder
            )
            print(f"  Added Image: {image.image} for {property.title}")

def run():
    print("Populating database with dummy data...")
    populate_users()
    populate_agents()
    populate_communities()
    populate_properties()
    print("Database population complete.")

# Run the script
run()
