import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "soilcore.settings")
django.setup()

from django.db import connection

# Delete soilcore migration history
with connection.cursor() as cursor:
    cursor.execute("DELETE FROM django_migrations WHERE app='soilcore'")
    print("✅ soilcore migration history cleared.")
