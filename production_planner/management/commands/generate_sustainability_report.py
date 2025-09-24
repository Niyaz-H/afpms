from django.core.management.base import BaseCommand
from production_planner.models import ProductionBatch
from django.db.models import Sum

class Command(BaseCommand):
    help = 'Generates a sustainability report based on production data.'

    def handle(self, *args, **kwargs):
        """
        The main logic for the management command.
        """
        self.stdout.write("Generating Sustainability Report...")

        total_co2_saved = ProductionBatch.objects.aggregate(
            total=Sum('product__target_co2_reduction')
        )['total'] or 0

        total_batches = ProductionBatch.objects.count()

        self.stdout.write(self.style.SUCCESS(
            f"Report Generated Successfully!"
        ))
        self.stdout.write(f"Total Production Batches: {total_batches}")
        self.stdout.write(f"Total Estimated CO2 Reduction: {total_co2_saved:.2f} kg")