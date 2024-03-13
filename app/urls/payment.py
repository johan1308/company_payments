from django.urls import path
from app.apis import (
    PaymentCompanyBanksGeneric,
)

urlpatterns = [
    path(
        'company_banks/',
        PaymentCompanyBanksGeneric.as_view(),
        name='company_banks',
    )
]
