
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('student/', include('student.urls', namespace='student')),
    path('', include('hotel.urls', namespace='hotel')),
    path('booking/', include('booking.urls', namespace='booking')),
    path('transaction/', include('transaction.urls', namespace='transaction')),
    path('admin_panel/', include('admin_panel.urls', namespace='admin_panel')),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)