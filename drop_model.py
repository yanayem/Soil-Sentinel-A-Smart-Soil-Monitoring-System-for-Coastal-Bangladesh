import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "soilcore.settings")
django.setup()

from soilcore.models import SoilType

SoilType.objects.all().delete()
print("✅ All SoilType entries deleted successfully!")
