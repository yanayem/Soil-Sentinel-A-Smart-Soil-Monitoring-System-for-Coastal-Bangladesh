from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # ---------------- HOME / ABOUT ----------------
    path('', views.homepage, name='homepage'),
    path('about/', views.aboutpage, name='aboutpage'),
    path('terms-privacy/', views.terms_privacy, name='terms_privacy'),

    # ---------------- SOIL TYPES ----------------
    path('soil-types/', views.soil_type_page, name='soil_types'),

    # ---------------- NEWSLETTER ----------------
    path('subscribe-newsletter/', views.subscribe_newsletter, name='subscribe_newsletter'),

    # ---------------- CROP PREDICTION ----------------
    path('crop-prediction/', views.crop_prediction, name='crop_prediction'),

    # ---------------- OTHER APPS ----------------
    path('weather/', include('weather.urls')),
    path('account/', include('account.urls', namespace='account')),
    path('soildata/', include('soildata.urls', namespace='soildata')),
    path('soilvision/', include('soilvision.urls', namespace='soilvision')),
    path('chat/', include('chatApp.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
