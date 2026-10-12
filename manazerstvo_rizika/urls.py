from django.urls import path

from .views import RiskAnalysisView

app_name = "manazerstvo_rizika"

urlpatterns = [
    path("", RiskAnalysisView.as_view(), name="index"),
]
