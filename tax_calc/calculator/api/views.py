from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from calculator.models import CountryTaxBand
from calculator.api.serializers import IncomeDataSerializer


class TaxCalculatorAPIView(APIView):

    def post(self, request, *args, **kwargs):
        serializer = IncomeDataSerializer(data=request.data)

        if serializer.is_valid():
            country = serializer.data["country"]
            income = serializer.data["income"]
            total_tax = 0
            calc_details = []

            for band in CountryTaxBand.objects.filter(country=country).order_by("-income_from"):
                if income > band.income_from and (band.income_to is None or income <= band.income_to):
                    band_tax = round((income - band.income_from) * band.tax_rate, 2)
                    total_tax += band_tax
                    calc_details.append({
                        "income_from": band.income_from,
                        "income_to": band.income_to,
                        "tax_rate": band.tax_rate,
                        "tax": band_tax,
                    })
                    income = band.income_from

            response_data = {"tax": total_tax}
            if serializer.data.get("detailed", False) is True:
                response_data["details"] = calc_details

            return Response(response_data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
