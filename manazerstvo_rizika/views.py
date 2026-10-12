import json
from pathlib import Path

from django.views.generic import TemplateView


class RiskAnalysisView(TemplateView):
    template_name = "manazerstvo_rizika/manazerstvo_rizika.html"

    BAND_NAMES = {"M": "Malé", "S": "Stredné", "V": "Veľké"}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        data = json.loads(
            Path(__file__).with_name("risk_analysis.json").read_text(encoding="utf-8")
        )
        data["risks"].sort(key=lambda risk: (-risk["score"], -risk["n"], risk["id"]))
        lookup = {risk["id"]: risk for risk in data["risks"]}
        for risk in data["risks"]:
            risk["band_name"] = self.BAND_NAMES[risk["band"]]
        for cell in data["matrix"]:
            cell["band_name"] = self.BAND_NAMES[cell["band"]]
        for scenario in data["economics"]["scenarios"]:
            scenario["title"] = lookup[scenario["id"]]["title"]
        context["analysis"] = data
        return context
