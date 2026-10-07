from django.urls import path

from .views import InvestmentRiskReturnView

app_name = "investicie"

urlpatterns = [
    path("", InvestmentRiskReturnView.as_view(), name="investicie"),
]
