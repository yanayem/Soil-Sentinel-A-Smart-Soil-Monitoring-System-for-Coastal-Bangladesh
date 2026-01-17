from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import SoilType, SoilPrediction, Newsletter
import os
import numpy as np
from io import BytesIO
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from sklearn.preprocessing import MultiLabelBinarizer, StandardScaler
import pytz
from django.utils import timezone

# ---------------- BASE ----------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ---------------- PATHS ----------------
MODEL_PATH = os.path.join(BASE_DIR, "crop_prediction_model.h5")
MLB_PATH = os.path.join(BASE_DIR, "crop_mlb_classes.npy")
SCALER_PATH = os.path.join(BASE_DIR, "crop_scaler.npy")

# ---------------- LAZY MODEL LOADER ----------------
model = None
mlb = None
scaler = None

def get_model():
    global model, mlb, scaler
    if model is None:
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(f"Model file not found: {MODEL_PATH}")
        model = load_model(MODEL_PATH)

        mlb_classes = np.load(MLB_PATH, allow_pickle=True)
        mlb = MultiLabelBinarizer(classes=mlb_classes)

        scaler_mean = np.load(SCALER_PATH)
        scaler_std = np.ones_like(scaler_mean)
        scaler = StandardScaler()
        scaler.mean_ = scaler_mean
        scaler.scale_ = scaler_std
    return model, mlb, scaler

# ========================= HOME / ABOUT =========================
def homepage(request):
    return render(request, 'home.html')

def aboutpage(request):
    return render(request, 'about.html')

def terms_privacy(request):
    return render(request, 'terms_privacy.html')

# ========================= NEWSLETTER =========================
def subscribe_newsletter(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            if Newsletter.objects.filter(email=email).exists():
                messages.error(request, "⚠️ This email is already subscribed.")
            else:
                Newsletter.objects.create(email=email)
                messages.success(request, "✅ Thank you for subscribing!")
        else:
            messages.error(request, "⚠️ Please enter a valid email.")
    return redirect(request.META.get('HTTP_REFERER', '/'))

# ========================= SOIL TYPES (READ-ONLY) =========================
def soil_type_page(request):
    query = request.GET.get("q", "")
    if query:
        soil_types = SoilType.objects.filter(name__icontains=query)
    else:
        soil_types = SoilType.objects.all()
    return render(request, "soil_types.html", {"soil_types": soil_types, "query": query})

# ========================= CROP PREDICTION =========================
@login_required
def crop_prediction(request):
    last_predictions = SoilPrediction.objects.filter(user=request.user).order_by('-created_at')[:10]
    dhaka_tz = pytz.timezone("Asia/Dhaka")

    if request.method == "POST":
        try:
            ph = float(request.POST.get("ph", 0))
            moisture = float(request.POST.get("moisture", 0))
            temp = float(request.POST.get("temp", 0))
            humidity = float(request.POST.get("humidity", 0))
            salinity = float(request.POST.get("salinity", 0))
            soil_image = request.FILES.get("image")

            soil_type = SoilType.objects.first()
            if not soil_type:
                messages.error(request, "⚠️ No soil type found. Please add a soil type first.")
                return render(request, "crop_prediction.html", {"last_predictions": last_predictions})

            model, mlb, scaler = get_model()

            X_num = np.array([[ph, moisture, temp, humidity, salinity]], dtype=np.float32)
            X_num_scaled = scaler.transform(X_num)

            if soil_image:
                img_bytes = BytesIO(soil_image.read())
                img = load_img(img_bytes, target_size=(150,150))
                X_img = img_to_array(img)/255.0
                X_img = X_img.reshape((1,) + X_img.shape)
            else:
                X_img = np.zeros((1,150,150,3), dtype=np.float32)

            y_pred = model.predict([X_img, X_num_scaled])
            predicted_crops = mlb.inverse_transform(y_pred)[0]
            if not predicted_crops:
                predicted_crops = ["No crops predicted"]

            soil_pred = SoilPrediction.objects.create(
                user=request.user,
                soil_type=soil_type,
                predicted_crops=", ".join(predicted_crops),
                ph=ph,
                moisture=moisture,
                temp=temp,
                humidity=humidity,
                salinity=salinity,
                image=soil_image,
                created_at=timezone.now().astimezone(dhaka_tz)
            )

            return render(request, "crop_prediction.html", {
                "prediction": soil_pred,
                "last_predictions": last_predictions
            })

        except Exception as e:
            return render(request, "crop_prediction.html", {
                "error": str(e),
                "last_predictions": last_predictions
            })

    return render(request, "crop_prediction.html", {"last_predictions": last_predictions})
