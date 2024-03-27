from django.urls import path, include
urlpatterns = [
  path('payments/', include('app.urls.payment')),
  path('companies/', include('app.urls.company')),
]