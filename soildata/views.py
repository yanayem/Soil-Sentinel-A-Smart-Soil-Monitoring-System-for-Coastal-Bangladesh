from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Device, DeviceReading
from account.models import UserProfile
from django.utils import timezone
from django.http import HttpResponse
from django.template.loader import render_to_string
from .models import Device, DeviceReading
from django.http import JsonResponse
from soilcore.models import SoilType



# -------------------------
# Dashboard view
# -------------------------
import json

@login_required
def dashboard(request):
    user = request.user
    profile, _ = UserProfile.objects.get_or_create(user=user)

    # Latest 7 moisture readings
    readings = list(
        DeviceReading.objects.filter(device__user=user)
        .order_by('-updated_at')[:7]
    )

    # For Chart.js (reverse to show oldest -> newest)
    readings_chart = readings[::-1]

    chart_labels = json.dumps([r.updated_at.strftime("%H:%M") for r in readings[::-1]])
    chart_data = json.dumps([r.moisture for r in readings[::-1]])

    return render(request, "dashboard.html", {
        "user": user,
        "profile": profile,
        "readings": readings[::-1],  
        "chart_labels": chart_labels,
        "chart_data": chart_data
    })

# -------------------------
# Soil Moisture view
# -------------------------
@login_required
def soil_moisture(request):
    device = Device.objects.filter(user=request.user, is_active=True).first()
    if device:
        readings = DeviceReading.objects.filter(device=device).order_by('-updated_at')[:50]
        
        for r in readings:
            r.local_time = timezone.localtime(r.updated_at)
    else:
        readings = []
    return render(request, "soil_moisture.html", {"readings": readings})

# -------------------------
# API to get moisture data
# -------------------------

@login_required
def api_moisture(request):
    device = Device.objects.filter(user=request.user, is_active=True).first()
    readings = []
    if device:
        qs = DeviceReading.objects.filter(device=device).order_by('-updated_at')[:50]
        for r in qs:
            readings.append({
                "time": timezone.localtime(r.updated_at).strftime("%I:%M %p %d-%m-%Y"),
                "moisture": r.moisture
            })

    latest = readings[0] if readings else {"time": "--", "moisture": 0}
    return JsonResponse({"latest": latest, "readings": readings})

# -------------------------
# Alerts view
# -------------------------
from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from soildata.models import Device, DeviceReading

@login_required
def alerts(request):
    device = Device.objects.filter(user=request.user, is_active=True).first()
    MIN_MOISTURE = 20
    MAX_MOISTURE = 80
    alert_list = []

    if device:
        readings = DeviceReading.objects.filter(device=device).order_by('-updated_at')[:50]
        for r in readings:
            local_time = timezone.localtime(r.updated_at).strftime("%I:%M %p %d-%m-%Y")
            if r.moisture < MIN_MOISTURE:
                alert_list.append({
                    "time": local_time,
                    "moisture": r.moisture,
                    "type": "Low Moisture",
                    "message": f"Soil moisture is too low ({r.moisture}%)"
                })
            elif r.moisture > MAX_MOISTURE:
                alert_list.append({
                    "time": local_time,
                    "moisture": r.moisture,
                    "type": "High Moisture",
                    "message": f"Soil moisture is too high ({r.moisture}%)"
                })
            else:
                alert_list.append({
                    "time": local_time,
                    "moisture": r.moisture,
                    "type": "Normal",
                    "message": f"Soil moisture is normal ({r.moisture}%)"
                })

    # -------------------------
    # AJAX request for live refresh
    # -------------------------
    if request.GET.get("ajax"):
        # Only render the alerts container part
        html = render_to_string("alerts_content.html", {"alerts": alert_list})
        return HttpResponse(html)

    # -------------------------
    # Normal full page render
    # -------------------------
    return render(request, "alerts.html", {"alerts": alert_list})

# -------------------------
# Crop Advisor view
# -------------------------
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Device, DeviceReading
from account.models import UserProfile
from django.utils import timezone
from django.http import HttpResponse
from django.template.loader import render_to_string
from .models import Device, DeviceReading
from django.http import JsonResponse
from soilcore.models import SoilType



# -------------------------
# Dashboard view
# -------------------------
import json

@login_required
def dashboard(request):
    user = request.user
    profile, _ = UserProfile.objects.get_or_create(user=user)

    # Latest 7 moisture readings
    readings = list(
        DeviceReading.objects.filter(device__user=user)
        .order_by('-updated_at')[:7]
    )

    # For Chart.js (reverse to show oldest -> newest)
    readings_chart = readings[::-1]

    chart_labels = json.dumps([r.updated_at.strftime("%H:%M") for r in readings[::-1]])
    chart_data = json.dumps([r.moisture for r in readings[::-1]])

    return render(request, "dashboard.html", {
        "user": user,
        "profile": profile,
        "readings": readings[::-1],  
        "chart_labels": chart_labels,
        "chart_data": chart_data
    })

# -------------------------
# Soil Moisture view
# -------------------------
@login_required
def soil_moisture(request):
    device = Device.objects.filter(user=request.user, is_active=True).first()
    if device:
        readings = DeviceReading.objects.filter(device=device).order_by('-updated_at')[:50]
        
        for r in readings:
            r.local_time = timezone.localtime(r.updated_at)
    else:
        readings = []
    return render(request, "soil_moisture.html", {"readings": readings})

# -------------------------
# API to get moisture data
# -------------------------

@login_required
def api_moisture(request):
    device = Device.objects.filter(user=request.user, is_active=True).first()
    readings = []
    if device:
        qs = DeviceReading.objects.filter(device=device).order_by('-updated_at')[:50]
        for r in qs:
            readings.append({
                "time": timezone.localtime(r.updated_at).strftime("%I:%M %p %d-%m-%Y"),
                "moisture": r.moisture
            })

    latest = readings[0] if readings else {"time": "--", "moisture": 0}
    return JsonResponse({"latest": latest, "readings": readings})

# -------------------------
# Alerts view
# -------------------------
from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from soildata.models import Device, DeviceReading

@login_required
def alerts(request):
    device = Device.objects.filter(user=request.user, is_active=True).first()
    MIN_MOISTURE = 20
    MAX_MOISTURE = 80
    alert_list = []

    if device:
        readings = DeviceReading.objects.filter(device=device).order_by('-updated_at')[:50]
        for r in readings:
            local_time = timezone.localtime(r.updated_at).strftime("%I:%M %p %d-%m-%Y")
            if r.moisture < MIN_MOISTURE:
                alert_list.append({
                    "time": local_time,
                    "moisture": r.moisture,
                    "type": "Low Moisture",
                    "message": f"Soil moisture is too low ({r.moisture}%)"
                })
            elif r.moisture > MAX_MOISTURE:
                alert_list.append({
                    "time": local_time,
                    "moisture": r.moisture,
                    "type": "High Moisture",
                    "message": f"Soil moisture is too high ({r.moisture}%)"
                })
            else:
                alert_list.append({
                    "time": local_time,
                    "moisture": r.moisture,
                    "type": "Normal",
                    "message": f"Soil moisture is normal ({r.moisture}%)"
                })

    # -------------------------
    # AJAX request for live refresh
    # -------------------------
    if request.GET.get("ajax"):
        # Only render the alerts container part
        html = render_to_string("alerts_content.html", {"alerts": alert_list})
        return HttpResponse(html)

    # -------------------------
    # Normal full page render
    # -------------------------
    return render(request, "alerts.html", {"alerts": alert_list})

# -------------------------
# Crop Advisor view
# -------------------------
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from soilcore.models import SoilType, SoilPrediction
from django.utils import timezone
import pytz

@login_required
def crop_advisor(request):
    recommendations = []
    tips = []
    alerts = []

    ph_value = None
    moisture_value = None
    temp_value = None
    humidity_value = None
    salinity_value = None

    dhaka_tz = pytz.timezone("Asia/Dhaka")

    if request.method == "POST":
        try:
            ph_value = float(request.POST.get("ph", 0))
            moisture_value = float(request.POST.get("moisture", 0))
            temp_value = float(request.POST.get("temp", 0))
            humidity_value = float(request.POST.get("humidity", 0))
            salinity_value = float(request.POST.get("salinity", 0))
        except (ValueError, TypeError):
            alerts.append("⚠️ Please enter valid numeric values.")

        # ---------------- Check input ranges ----------------
        # We'll get soils that match the input ranges
        soils = SoilType.objects.filter(
            ph_min__lte=ph_value, ph_max__gte=ph_value,
            moisture_min__lte=moisture_value, moisture_max__gte=moisture_value,
            temp_min__lte=temp_value, temp_max__gte=temp_value,
            humidity_min__lte=humidity_value, humidity_max__gte=humidity_value,
            salinity_min__lte=salinity_value, salinity_max__gte=salinity_value
        )

        if not soils.exists():
            alerts.append("⚠️ No matching soil type found for the given values.")
        else:
            soil_type = soils.first()  # Pick the first matching soil type

            # ---------------- Get recommendations ----------------
            if soil_type.crops:
                recommendations = [c.strip() for c in soil_type.crops.split(",")]

            if soil_type.location:
                tips.append(f"Location: {soil_type.location}")

            if soil_type.name:
                tips.append(f"Soil Type: {soil_type.name}")

            # ---------------- Save prediction ----------------
            SoilPrediction.objects.create(
                user=request.user,
                soil_type=soil_type,
                predicted_crops=", ".join(recommendations),
                ph=ph_value,
                moisture=moisture_value,
                temp=temp_value,
                humidity=humidity_value,
                salinity=salinity_value,
                created_at=timezone.now().astimezone(dhaka_tz)
            )

    return render(request, "crop_advisor.html", {
        "recommendations": recommendations,
        "tips": tips,
        "alerts": alerts,
        "ph_value": "",
        "moisture_value": "",
        "temp_value": "",
        "humidity_value": "",
        "salinity_value": "",
    })
