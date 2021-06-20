from django.core.management import call_command
from rest_framework import status
from rest_framework.test import APITestCase


class TestTaxCalculatorAPIView(APITestCase):
    url = "/api/calculator/tax/"

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        call_command("load_tax_bands")

    def test_no_country_data_returns_400(self):
        response = self.client.post(self.url, {"income": 0})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {"country": ["This field is required."]})

    def test_no_income_data_returns_400(self):
        response = self.client.post(self.url, {"country": "UK"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {"income": ["This field is required."]})

    def test_uk_income_0(self):
        response = self.client.post(self.url, {"country": "UK", "income": 0})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {"tax": 0})

    def test_uk_income_5000(self):
        response = self.client.post(self.url, {"country": "UK", "income": 5000})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {"tax": 0})

    def test_uk_income_12500(self):
        response = self.client.post(self.url, {"country": "UK", "income": 12500})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {"tax": 0})

    def test_uk_income_12501(self):
        response = self.client.post(self.url, {"country": "UK", "income": 12501})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {"tax": 0.2})

    def test_uk_income_13000(self):
        response = self.client.post(self.url, {"country": "UK", "income": 13000})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {"tax": 100})

    def test_uk_income_50000(self):
        response = self.client.post(self.url, {"country": "UK", "income": 50000})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {"tax": 7500})

    def test_uk_income_50001(self):
        response = self.client.post(self.url, {"country": "UK", "income": 50001})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {"tax": 7500.4})

    def test_uk_income_52000(self):
        response = self.client.post(self.url, {"country": "UK", "income": 52000})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {"tax": 8300})

    def test_uk_income_123000(self):
        response = self.client.post(self.url, {"country": "UK", "income": 123000})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {"tax": 36700})

    def test_uk_income_150000(self):
        response = self.client.post(self.url, {"country": "UK", "income": 150000})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {"tax": 47500})

    def test_uk_income_150001(self):
        response = self.client.post(self.url, {"country": "UK", "income": 150001})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {"tax": 47500.45})

    def test_uk_income_235570(self):
        response = self.client.post(self.url, {"country": "UK", "income": 235570})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {"tax": 86006.5})

    def test_pl_income_0(self):
        response = self.client.post(self.url, {"country": "PL", "income": 0})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {"tax": 0})

    def test_pl_income_6000(self):
        response = self.client.post(self.url, {"country": "PL", "income": 6000})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {"tax": 1020})

    def test_pl_income_55700(self):
        response = self.client.post(self.url, {"country": "PL", "income": 55700})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {"tax": 9469})

    def test_pl_income_85528(self):
        response = self.client.post(self.url, {"country": "PL", "income": 85528})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {"tax": 14539.76})

    def test_pl_income_85529(self):
        response = self.client.post(self.url, {"country": "PL", "income": 85529})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {"tax": 14540.08})

    def test_pl_income_145700(self):
        response = self.client.post(self.url, {"country": "PL", "income": 145700})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {"tax": 33794.8})

    def test_uk_income_235570_detailed_response(self):
        response = self.client.post(self.url, {"country": "UK", "income": 235570, "detailed": True})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {
            "tax": 86006.5,
            "details": [
                {
                    "income_from": 150000,
                    "income_to": None,
                    "tax_rate": 0.45,
                    "tax": 38506.5
                },
                {
                    "income_from": 50000,
                    "income_to": 150000,
                    "tax_rate": 0.4,
                    "tax": 40000.0
                },
                {
                    "income_from": 12500,
                    "income_to": 50000,
                    "tax_rate": 0.2,
                    "tax": 7500.0
                },
                {
                    "income_from": 0,
                    "income_to": 12500,
                    "tax_rate": 0.0,
                    "tax": 0.0
                }
            ]
        })
