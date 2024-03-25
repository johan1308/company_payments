from rest_framework import serializers
from app.models.company import Companies


class CompaniesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Companies
        fields = (
            'id',
            'name',
            'email',
            'description',
            'rif',
        )
