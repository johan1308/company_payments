from django.urls import path
from app.apis import (
    BanksGeneric,
    PaymentsCompanyList,
    PaymentsCompanyGeneric,
    PaymentMethodsGenerics,
    PaymentCompanyBanksGeneric,
    PaymentsCompanyRetrieveUpdate,
)

urlpatterns = [
    path(
        '',
        PaymentsCompanyList.as_view(),
        name='payments_list',
    ),
    path(
        '<int:id>/',
        PaymentsCompanyRetrieveUpdate.as_view(),
        name='payments_ru',
    ),
    path(
        'banks/',
        BanksGeneric.as_view(),
        name='banks_g',
    ),
    path(
        'payment_methods/',
        PaymentMethodsGenerics.as_view(),
        name='payment_methods_g',
    ),
    path(
        'company_banks/',
        PaymentCompanyBanksGeneric.as_view(),
        name='company_banks',
    ),
    path(
        'validate/',
        PaymentsCompanyGeneric.as_view(),
        name='payments_validate',
    ),
]
