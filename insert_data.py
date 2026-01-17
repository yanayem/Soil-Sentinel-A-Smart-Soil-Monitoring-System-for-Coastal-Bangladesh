import os
import django
import random

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "soilcore.settings")
django.setup()

from soilcore.models import SoilType

# Real soil names in Bangladesh
base_soil_names = [
    "Alluvial Soil", "Red Soil", "Laterite Soil", "Peaty Soil", "Saline Soil",
    "Sandy Soil", "Clay Soil", "Loamy Soil", "Black Soil", "Silty Soil"
]

# Sample crops in Bangladesh
bangladesh_crops = [
    "Rice", "Wheat", "Maize", "Jute", "Sugarcane", "Potato", "Tomato", "Onion",
    "Chili", "Cabbage", "Spinach", "Lettuce", "Pumpkin", "Brinjal", "Mustard",
    "Lentil", "Chickpea", "Soybean", "Banana", "Papaya", "Guava", "Mango",
    "Jackfruit", "Coconut", "Betel Leaf", "Watermelon", "Cucumber", "Radish",
    "Carrot", "Garlic", "Cauliflower", "Bitter Gourd", "Snake Gourd", "Ridge Gourd",
    "Bottle Gourd", "Pointed Gourd", "Taro", "Sweet Potato", "Colocasia",
    "Spinach (Amaranth)", "Kohlrabi", "Fenugreek", "Celery", "Beetroot", "Turnip",
    "Okra", "Field Bean", "Green Gram", "Black Gram", "Mung Bean", "Cowpea",
    "Sesame", "Sunflower", "Groundnut", "Pumpkin (Local)", "Tomato (Local)",
    "Brinjal (Local)", "Chili (Local)"
]

# Create 1000 SoilType entries using real soil names
for i in range(1, 1001):
    soil_name = random.choice(base_soil_names)
    ph_min = round(random.uniform(4.5, 7.0), 1)
    ph_max = round(random.uniform(ph_min + 0.5, 8.5), 1)
    moisture_min = round(random.uniform(15, 50), 1)
    moisture_max = round(random.uniform(moisture_min + 10, 80), 1)
    temp_min = round(random.uniform(10, 30), 1)
    temp_max = round(random.uniform(temp_min + 5, 45), 1)
    humidity_min = round(random.uniform(30, 60), 1)
    humidity_max = round(random.uniform(humidity_min + 10, 95), 1)
    salinity_min = round(random.uniform(0.0, 1.0), 1)
    salinity_max = round(random.uniform(salinity_min + 0.1, 2.0), 1)

    # Pick 5–15 random crops for each soil type
    crops = ", ".join(random.sample(bangladesh_crops, random.randint(5, 15)))

    SoilType.objects.create(
        name=f"{soil_name}",  # Real soil name + unique number
        ph_min=ph_min,
        ph_max=ph_max,
        moisture_min=moisture_min,
        moisture_max=moisture_max,
        temp_min=temp_min,
        temp_max=temp_max,
        humidity_min=humidity_min,
        humidity_max=humidity_max,
        salinity_min=salinity_min,
        salinity_max=salinity_max,
        crops=crops
    )

print("✅ 1000 real SoilType entries added successfully!")
