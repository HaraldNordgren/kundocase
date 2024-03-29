from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r"^api/v1/", include("kundocase.api.v1.urls")),
    url(r"^", include("kundocase.forum.urls")),
]

# Set up static file serving for development
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
