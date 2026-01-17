from django.db import models
from django.contrib.auth.models import User

# -------------------------------
# SoilType: Soil type information
# -------------------------------
class SoilType(models.Model):
    name = models.CharField(max_length=100)
    ph_min = models.FloatField()
    ph_max = models.FloatField()
    moisture_min = models.FloatField()
    moisture_max = models.FloatField()
    temp_min = models.FloatField()
    temp_max = models.FloatField()
    humidity_min = models.FloatField()
    humidity_max = models.FloatField()
    salinity_min = models.FloatField()
    salinity_max = models.FloatField()
    crops = models.TextField(help_text="Comma-separated crop names suitable for this soil")
    location = models.CharField(max_length=255, blank=True, null=True)  # optional

    class Meta:
        verbose_name = "Soil Type"
        verbose_name_plural = "Soil Types"
        db_table = "soilcore_soiltype"  # keep prefix

    def __str__(self):
        return self.name

    # Helper methods
    def ph_range(self):
        return f"{self.ph_min} - {self.ph_max}"

    def moisture_range(self):
        return f"{self.moisture_min} - {self.moisture_max}"

    def temp_range(self):
        return f"{self.temp_min} - {self.temp_max}"

    def humidity_range(self):
        return f"{self.humidity_min} - {self.humidity_max}"

    def salinity_range(self):
        return f"{self.salinity_min} - {self.salinity_max}"


# -----------------------------------------------
# SoilPrediction: Predictions made by users
# -----------------------------------------------
class SoilPrediction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="soilcore_predictions")
    soil_type = models.ForeignKey(SoilType, on_delete=models.SET_NULL, null=True)
    predicted_crops = models.TextField(help_text="Comma-separated predicted crops")
    ph = models.FloatField()
    moisture = models.FloatField()
    temp = models.FloatField()
    humidity = models.FloatField()
    salinity = models.FloatField()
    image = models.ImageField(upload_to="soil_images/", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Soil Prediction"
        verbose_name_plural = "Soil Predictions"
        ordering = ["-created_at"]
        db_table = "soilcore_soilprediction"  # keep prefix

    def __str__(self):
        soil_name = self.soil_type.name if self.soil_type else "Unknown Soil"
        return f"{self.user.username} - {soil_name} ({self.created_at.strftime('%Y-%m-%d %H:%M')})"


# -----------------------------------------------
# Newsletter: Subscriber emails
# -----------------------------------------------
class Newsletter(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Newsletter Subscriber"
        verbose_name_plural = "Newsletter Subscribers"
        db_table = "soilcore_newsletter"  # keep prefix

    def __str__(self):
        return self.email
