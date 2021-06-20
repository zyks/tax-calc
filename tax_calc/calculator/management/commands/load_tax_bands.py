import json
from django.core.management.base import BaseCommand
from django.db import transaction
from calculator.models import CountryTaxBand


class Command(BaseCommand):

    @transaction.atomic
    def handle(self, *args, **options):
        tax_data = json.load(open("/code/tax_bands.json"))
        for country_tax_data in tax_data:
            country = country_tax_data.get("country")
            for income_from, income_to, tax_rate in country_tax_data.get("tax_bands", []):
                CountryTaxBand.objects.create(
                    country=country,
                    income_from=income_from,
                    income_to=income_to,
                    tax_rate=tax_rate,
                )
