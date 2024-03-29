from django.urls import path
from app.apis import (
    StatusList,
    OptionsList,
)

urlpatterns = [
    path(
        'status/',
        StatusList.as_view(),
        name='status',
    ),
    path(
        'options/',
        OptionsList.as_view(),
        name='options_l',
    )
]
