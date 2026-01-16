import os
import sys
import django
import serial
import time
from collections import deque
from django.utils import timezone

# ------------------------
# Django setup
# ------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "soilcore.settings")
django.setup()

from django.contrib.auth.models import User
from soildata.models import Device, DeviceReading

# ------------------------
# Arduino Serial Setup
# ------------------------
ARDUINO_PORT = "COM6"
BAUD_RATE = 9600

try:
    ser = serial.Serial(ARDUINO_PORT, BAUD_RATE, timeout=1)
    print(f"✅ Connected to Arduino on {ARDUINO_PORT}")
except serial.SerialException as e:
    print(f"❌ Could not connect to {ARDUINO_PORT}: {e}")
    raise SystemExit

# ------------------------
# Select device
# ------------------------
user = User.objects.first()
if not user:
    raise Exception("No users found! Create a superuser first.")

device, created = Device.objects.get_or_create(
    name="My Soil Sensor",
    defaults={"user": user, "is_active": True}
)

print(f"📡 Reading data from device: {device.name}")
print("⏱️ Saving data every 45 seconds (Ctrl+C to stop)")

# ------------------------
# Settings
# ------------------------
READ_INTERVAL_SECONDS = 15      # 🔥 READ & SAVE EVERY 15 SECONDS
BUFFER_SIZE = 5                 # rolling average buffer

raw_buffer = deque(maxlen=BUFFER_SIZE)

# ------------------------
# Read & Save Loop
# ------------------------
try:
    while True:
        start_time = time.time()

        # Collect data for smoothing
        while time.time() - start_time < READ_INTERVAL_SECONDS:
            try:
                line = ser.readline().decode("utf-8").strip()
            except Exception:
                continue

            if not line:
                continue

            try:
                clean = line.replace("%", "").strip()
                first_part = clean.split(",")[0].strip()

                if not first_part.replace(".", "", 1).isdigit():
                    continue

                raw_value = float(first_part)
                raw_buffer.append(raw_value)

            except Exception:
                continue

            time.sleep(0.2)  # small delay to avoid CPU overuse

        if not raw_buffer:
            print("⚠️ No data received in last 45 seconds")
            continue

        smooth_raw = round(sum(raw_buffer) / len(raw_buffer), 2)
        current_time = timezone.now()

        try:
            DeviceReading.objects.create(
                device=device,
                moisture=smooth_raw,
                updated_at=current_time
            )
            print(
                f"💾 Saved at {current_time.strftime('%H:%M:%S')} | "
                f"Moisture={smooth_raw}"
            )
        except Exception as e:
            print(f"⚠️ Database save failed: {e}")

except KeyboardInterrupt:
    print("\n🛑 Stopped by user")

finally:
    if ser.is_open:
        ser.close()
        print("🔌 Serial connection closed")
