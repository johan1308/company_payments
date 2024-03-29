from django.db import transaction
from rest_framework import status


class BaseResource():

    # value_id: id del modelo principal
    # Model: Modelo principal
    # RelatedModel: modelo pivote
    # ThirdModel: modelo tercero
    # list_values: lista de valores uniran Model con ThirdModel
    # field_model: nombre del la fk que se relacion con el modelo principal en la tabla pivote
    # field_related_model: nombre del campo del modelo donde ira el valor que se relaciona
    # method: si se va agregar o eliminar los valores(true, false)
    # assign: # Asignar=True, Crear=False
    # user: usuario que esta realizando la peticion
    def assign_record_to_model(
        self,
        value_id,
        Model,
        RelatedModel,
        ThirdModel,
        list_values,
        field_model,
        field_related_model,
        method,
        assign,
        user
    ):
        message = "successfull registers" if method else "registers removed successfully"
        status_code = status.HTTP_201_CREATED if method else status.HTTP_200_OK

        if not method:
            message = "registers removed successfully"
            status_code = status.HTTP_200_OK

        try:
            with transaction.atomic():
                instance = Model.objects.get(pk=value_id)
                for list_value in list_values:
                    
                    value_id = list_value.get('id')
                    description = list_value.get('description')
                    status_data = list_value.get('status')
                    try:
                        # Asignar los métodos de pago seleccionados a la tienda
                        value = ThirdModel.objects.get(pk=value_id)

                        data_insert = {
                            f"{field_model}":instance,
                            f"{field_related_model}":value 
                        }

                        if method: # True: Agregar, False: eliminar

                            if assign: # True: Asignar, False: Crear
                                obj, created = RelatedModel.objects.get_or_create(
                                    **data_insert
                                )
                            else:
                                obj, created = RelatedModel.objects.create(**data_insert), True

                            if description:
                                obj.description = description

                            if status_data:
                                obj.status_id = status_data

                            if created:
                                obj.created_by = user
                                obj.save()
                            else:
                                obj.updated_by = user
                                obj.save()
                        else:
                            RelatedModel.objects.filter(
                                **data_insert
                            ).delete()

                    except Model.DoesNotExist:
                        message = f"Previous recipe with id {value_id} does not exist."
                        status_code = status.HTTP_404_NOT_FOUND

        except Model.DoesNotExist:     
            message = "Recipes does not exist"
            status_code = status.HTTP_404_NOT_FOUND

        return message, status_code


