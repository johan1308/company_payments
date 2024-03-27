from rest_framework import (
    permissions,
    serializers,
    generics,
    filters,
    status,
)
from app.permissions import HasModelPermission
from app.models import Companies
from app.serializers import CompaniesSerializer
from drf_spectacular.utils import (
    extend_schema,
)


# listar compañias de una tienda
class CompaniesListCreate(generics.ListCreateAPIView):
    """
    Ruta para listar y crear compañias de una tienda,
    debe ser administrador (`is_staff` es `True`)
    o tener el permiso:
    - `view_companies` para GET,
    - `add_companies` para POST,
    """
    
    queryset = Companies.objects.all()
    serializer_class = CompaniesSerializer
    filter_backends = (
        filters.SearchFilter,
        DjangoFilterBackend,
    )
    # filterset_class = PaymentsCompanyFilter
    search_fields = (
        'name',
        'email',
        'rif',
    )
    permission_classes = [
        permissions.IsAdminUser
        |
        (HasModelPermission)
    ]
    model_permissions = {
        'GET': ['app.view_companies'],
        'POST': ['app.add_companies'],
    }

    def get_queryset(self):
        queryset = self.queryset
        user = self.request.user
        if not user.is_superuser:
            queryset = queryset.filter(pk=user.company)
        return queryset

    @extend_schema(tags=["Companies"])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(tags=["Companies"])
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
