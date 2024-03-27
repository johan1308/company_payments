from django.urls import path
from app.apis import (
    CompaniesListCreate,
)

urlpatterns = [
    path(
        '',
        CompaniesListCreate.as_view(),
        name='payments_lc',
    )
]
