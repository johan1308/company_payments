from rest_framework import serializers
from app.models.payment import (
    Banks,
    PaymentMethods,
    PaymentsCompany,
    PaymentMethodsCompanies,
)
from app.serializers.company import (
    CompaniesSerializer,
)


class PaymentMethodsSerializer(serializers.ModelSerializer):
    status_name = serializers.CharField(source='status.name', read_only=True, default=None)

    class Meta:
        model = PaymentMethods
        fields = (
            'id',
            'currency',
            'name',
            'status',
            'status_name',
        )


class BanksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banks
        fields = (
            'id',
            'achronym',
            'code',
            'name',
        )


class PaymentMethodsCompaniesSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMethodsCompanies
        fields = (
            'id',
            'company',
            'payment_method',
            'bank',
            'email',
            'identification',
            'phone',
            'created_by',
            'created_at',
        )
        extra_kwargs = {
            'company': {
                'required': False,
            },
        }


class PaymentsCompanySerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(source='company.name', read_only=True, default=None)
    bank_origin_name = serializers.CharField(source='bank_origin.name', read_only=True, default=None)
    bank_destiny_name = serializers.CharField(source='bank_destiny.name', read_only=True, default=None)
    method_name = serializers.CharField(source='method.name', read_only=True, default=None)
    
    class Meta:
        model = PaymentsCompany
        fields = (
            'id',
            'amount',
            'date',
            'description',
            'mobile',
            'reference',
            'sender',
            'status',
            'company',
            'company_name',
            'bank_origin',
            'bank_origin_name',
            'bank_destiny',
            'bank_destiny_name',
            'method',
            'method_name',
            'updated_at',
        )

    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if not (hasattr(self, 'context')):
            return

        retrieve = self.context.get('retrieve', False)

        if retrieve:
            remove_fields = ['company_name', 'bank_origin_name', 'bank_destiny_name', 'method_name']
            for remove_field in remove_fields:
                self.fields.pop(remove_field)

            self.fields['company'] = CompaniesSerializer(read_only=True)
            self.fields['bank_origin'] = BanksSerializer(read_only=True)
            self.fields['bank_destiny'] = BanksSerializer(read_only=True)
            self.fields['method'] = PaymentMethodsSerializer(read_only=True)