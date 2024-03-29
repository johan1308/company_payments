from django.urls import path
from app.apis import (
    StatusList,
    OptionsListCreate,
    OptionsRetrieveUpdateDestroy,
)

urlpatterns = [
    path(
        'status/',
        StatusList.as_view(),
        name='status',
    ),
    path(
        'options/',
        OptionsListCreate.as_view(),
        name='options_l',
    ),
    path(
        'options/<int:id>/',
        OptionsRetrieveUpdateDestroy.as_view(),
        name='options_rud',
    )
]
