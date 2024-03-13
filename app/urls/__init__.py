from django.urls import path, include
urlpatterns = [
  path('payments/', include('app.urls.payment')),
]