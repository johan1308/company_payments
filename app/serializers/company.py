from rest_framework import serializers
from app.models.company import (
    Companies,
    CompaniesOptions,
)
from app.models.payment import PaymentMethodsCompanies


class CompaniesOptionsSerializer(serializers.ModelSerializer):
    created_by_name = serializers.CharField(source='created_by.name', default=None, read_only=True)
    company_name = serializers.CharField(source='company.name', default=None, read_only=True)
    option_name = serializers.CharField(source='option.name', default=None, read_only=True)
    
    class Meta:
        model = CompaniesOptions
        fields = (
            'id',
            'company',
            'company_name',
            'option',
            'option_name',
            'description',
            'created_by',
            'created_by_name',
            'created_at',
        )

class PaymentMethodsCompaniesSerializer(serializers.ModelSerializer):
    status_name = serializers.CharField(source='status.name', read_only=True, default=None)
    created_by_name = serializers.CharField(source='created_by.short_name', default=None, read_only=True)
    payment_method_name = serializers.CharField(source='payment_method.name', default=None, read_only=True)

    class Meta:
        model = PaymentMethodsCompanies
        fields = (
            'id',
            'payment_method',
            'payment_method_name',
            'status',
            'status_name',
            'created_by_name',
            'created_at',
        )

class CompaniesSerializer(serializers.ModelSerializer):
    status_name = serializers.CharField(source='status.name', read_only=True, default=None)
    

    class Meta:
        model = Companies
        fields = (
            'id',
            'name',
            'email',
            'description',
            'rif',
            'status',
            'status_name',
            'start_date_work',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if not (hasattr(self, 'context')):
            return

        request = self.context.get('request')
        retrieve = self.context.get('retrieve')
        
        if request and request.method in ['POST'] or retrieve:
            self.fields['payment_methods_companies'] = PaymentMethodsCompaniesSerializer(many=True)
            self.fields['company_options'] = CompaniesOptionsSerializer(many=True, read_only=True)


    def create(self, validated_data):
        payment_methods_companies = validated_data.pop('payment_methods_companies')
        request = self.context.get('request')

        instance = self.Meta.model.objects.create(**validated_data)

        for payment_methods in payment_methods_companies:
            PaymentMethodsCompanies.objects.create(company=instance, created_by=request.user, **payment_methods)
        return instance