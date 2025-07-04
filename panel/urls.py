from django.contrib import admin
from django.urls import path, include
from django.urls import path,include

from rest_framework import permissions
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
# api documentation config
schema_view = get_schema_view(
    openapi.Info(
        title="panel-api",
        default_version="v1",
        description="test for panel api documnet",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="admin@admin.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('hr/', include('hr.urls')),
    path('account/', include('accounts.urls')),
     path(
         
        "swagger.json/",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path(
        "redoc/",
        schema_view.with_ui("redoc", cache_timeout=0),
        name="schema-redoc",
    ),
    path('api-auth/', include('rest_framework.urls')),
    path('',include('hr.urls')),
]
