from prowler.lib.check.models import Check, Check_Report_Azure
from prowler.providers.azure.services.defender.defender_client import defender_client


class defender_container_images_scan_enabled(Check):
    def execute(self) -> Check_Report_Azure:
        findings = []
        for subscription, pricings in defender_client.pricings.items():
            if "Containers" in pricings:
                report = Check_Report_Azure(
                    metadata=self.metadata(), resource=pricings["Containers"]
                )
                report.subscription = subscription
                report.status = "PASS"
                report.status_extended = (
                    f"Container image scan is enabled in subscription {subscription}."
                )
                if not pricings["Containers"].extensions.get(
                    "ContainerRegistriesVulnerabilityAssessments"
                ):
                    report.status = "FAIL"
                    report.status_extended = f"Container image scan is disabled in subscription {subscription}."

                findings.append(report)
        return findings
