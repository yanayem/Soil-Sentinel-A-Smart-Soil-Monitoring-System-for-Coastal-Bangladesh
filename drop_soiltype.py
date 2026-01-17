import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "soilcore.settings")
django.setup()

from soilcore.models import SoilType

# Delete all SoilType entries
deleted_count, _ = SoilType.objects.all().delete()
print(f"✅ Deleted {deleted_count} SoilType entries.")
