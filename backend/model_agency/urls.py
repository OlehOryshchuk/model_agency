"""model_agency_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView


urlpatterns = [
    path("admin/", admin.site.urls),
    path("models/", include("model.urls", namespace="model")),
    path("contact/", include("contact.urls", namespace="contact")),
    path("newsletters/", include("newsletter.urls", namespace="newsletter")),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/doc/swagger/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    )
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# debug toolbar we are not using during testing or production
if (
        not settings.TESTING
        and settings.DJANGO_ENV != "production"
):

    urlpatterns.append(path("__debug__/", include("debug_toolbar.urls")))
