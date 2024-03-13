from django.contrib import admin
from django.urls import (
    path,
    include
)
# from app.apis import Login, Logout
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)
from app.apis import Login, Logout



urlpatterns = [
    path('admin/', admin.site.urls),
    path(
        'login/',
        Login.as_view(),
        name='login'
    ),
    path(
        'logout/',
        Logout.as_view(),
        name='logout'
    ),
    path(
        'api/schema/',
        SpectacularAPIView.as_view(),
        name='schema'
    ),
    path(
        'api/swagger/',
        SpectacularSwaggerView.as_view(),
        name='swagger'
    ),
    path(
        'api/',
        include(
            (
                'app.urls',
                'app'
            ),
            namespace='api'
        ),
    )
]
