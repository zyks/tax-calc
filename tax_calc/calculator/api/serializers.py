from rest_framework import serializers
from calculator.models import CountryTaxBand


class IncomeDataSerializer(serializers.Serializer):
    country = serializers.ChoiceField(choices=CountryTaxBand.Country.choices)
    income = serializers.FloatField(min_value=0)
    detailed = serializers.BooleanField(required=False)
