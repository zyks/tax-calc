from django.urls import path
from calculator.api.views import TaxCalculatorAPIView

urlpatterns = [
    path("tax/", TaxCalculatorAPIView.as_view()),
]
