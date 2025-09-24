from django.views.generic import ListView
from .models import ProductionBatch

class ProductionBatchListView(ListView):
    """
    Displays a list of all production batches with optimized queries.
    """
    model = ProductionBatch
    template_name = 'production_planner/batch_list.html'
    context_object_name = 'batches'

    def get_queryset(self):
        """
        Overrides the default queryset to include select_related and prefetch_related
        for query optimization.
        """
        return ProductionBatch.objects.select_related('product', 'created_by').prefetch_related('materials')
