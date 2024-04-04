from django.utils.translation import gettext as _
from rest_framework import (
    permissions,
    generics,
    filters,
)
from rest_framework.response import (
    Response,
)
from app.models.base import (
    Status,
    Options,
)
from app.serializers import (
    StatusSerializer,
    OptionsSerializer,
)
from django_filters.rest_framework import (
    DjangoFilterBackend,
)
from app.permissions import HasModelPermission
from drf_spectacular.utils import (
    extend_schema,
)


# consultar status por tipo
class StatusList(generics.ListAPIView):
    """
    Ruta para consultar status por tipo,
    debe ser administrador (`is_staff` es `True`)
    o tener el permiso:
    - `view_status` para GET,
    """

    pagination_class = None
    queryset = Status.objects.all()
    serializer_class = StatusSerializer
    filter_backends = (
        DjangoFilterBackend,
    )
    filterset_fields = ['type']
    permission_classes = [
        permissions.IsAdminUser
        |
        (HasModelPermission)
    ]
    model_permissions = {
        'GET': ['app.view_status'],
    }

    def get_queryset(self):
        return super().get_queryset()


    @extend_schema(tags=["Base"])
    def get(self, request, *args, **kwargs):
        if not request.query_params.get('type'):
            return Response({"message": "field 'type' is required"})

        return super().get(request, *args, **kwargs)


# consultar opciones por tipo
class OptionsListCreate(generics.ListCreateAPIView):
    """
    Ruta para consultar opciones por tipo,
    debe ser administrador (`is_staff` es `True`)
    o tener el permiso:
    - `view_options` para GET,
    """
    pagination_class = None
    queryset = Options.objects.all().exclude(type=1)
    serializer_class = OptionsSerializer
    search_fields = (
        'name',
    )
    filterset_fields = ['type']
    permission_classes = [
        permissions.IsAdminUser
        |
        (HasModelPermission)
    ]
    model_permissions = {
        'GET': ['app.view_options'],
    }

    @extend_schema(tags=["Base"])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(tags=["Base"])
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)



# consultar, editar y eliminar una opcion
class OptionsRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    """
    Ruta para consultar, editar y eliminar una opcion,
    debe ser administrador (`is_staff` es `True`)
    o tener el permiso:
    - `view_options` para GET,
    - `change_options` para PATCH,
    - `delete_options` para DELETE,
    """
    lookup_field = 'id'
    lookup_url_kwarg = 'id'
    queryset = Options.objects.all().exclude(type=1)
    serializer_class = OptionsSerializer
    permission_classes = [
        permissions.IsAdminUser
        |
        (HasModelPermission)
    ]
    model_permissions = {
        'GET': ['app.view_options'],
        'PATCH': ['app.change_options'],
        'DELETE': ['app.delete_options'],
    }

    @extend_schema(tags=["Base"])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(exclude=True)
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @extend_schema(tags=["Base"])
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @extend_schema(tags=["Base"])
    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        
        if obj.option_companies.count() > 0:
            return Response({"message": _("This option is already in use")})

        return super().delete(request, *args, **kwargs)
