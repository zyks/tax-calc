from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class CountryTaxBand(models.Model):
    class Country(models.TextChoices):
        UK = "UK", "UK"
        PL = "PL", "PL"
    country = models.CharField(max_length=32, choices=Country.choices)
    income_from = models.PositiveIntegerField()
    income_to = models.PositiveIntegerField(null=True)
    tax_rate = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(1)])
