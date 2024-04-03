from django.urls import path
from app.apis import (
    DashboardGeneric,
    CompaniesListCreate,
    CompaniesRetrieveUpdate,
    CompaniesPaymentMethodsGeneric,
)

urlpatterns = [
    path(
        '',
        CompaniesListCreate.as_view(),
        name='payments_lc',
    ),
    path(
        '<int:id>/',
        CompaniesRetrieveUpdate.as_view(),
        name='companies_ru',
    ),
    path(
        '<int:id>/payment_methods/',
        CompaniesPaymentMethodsGeneric.as_view(),
        name='companies_payment_methods_g',
    ),
    path(
        'dashboard/',
        DashboardGeneric.as_view(),
        name='dasgboard_g',
    )
]
