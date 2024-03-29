from django.urls import path, include
urlpatterns = [
  path('base/', include('app.urls.base')),
  path('payments/', include('app.urls.payment')),
  path('companies/', include('app.urls.company')),
]