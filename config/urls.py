from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

from config.settings.local import MEDIA_ROOT, MEDIA_URL

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
    path("api/", include("apps.category.urls")),
    path("api/auth/", include("apps.users.urls")),
    path("api/", include("apps.events.urls")),
    path("api/", include("apps.studies.urls")),
] + static(MEDIA_URL, document_root=MEDIA_ROOT)
