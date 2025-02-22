"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from django.conf import settings
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from django.urls import path
from django_prometheus.exports import ExportToDjangoView
from django_prometheus import exports


schema_view = get_schema_view(
    openapi.Info(
        title="Pong Backend API",
        default_version="v1",
        description="API documentation",        
        contact=openapi.Contact(email="gkubina@42lehavre.fr"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)



urlpatterns = [
    path("api/swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    path("api/redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),


    path("api/", include("user_mgm.urls")),
    path("api/games/", include("gamestats.urls")),
    path("api/friends/", include("friends.urls")),
    path("admin/", admin.site.urls),
    path("api/", include('django_prometheus.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
