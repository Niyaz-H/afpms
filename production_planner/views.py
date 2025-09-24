from django.views.generic import ListView
from django.db.models import Q, Sum, F
from .models import ProductionBatch
from django.db.models import Value as V
from django.db.models.functions import Coalesce
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializers import ProductionBatchSerializer

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
        for query optimization, and to add advanced filtering and annotations.
        """
        queryset = ProductionBatch.objects.select_related('product', 'created_by').prefetch_related('materials')
        
        # Annotate each batch with its total material cost
        queryset = queryset.annotate(
            total_material_cost=Coalesce(Sum(F('batchmaterial__quantity') * F('batchmaterial__material__cost_per_unit')), V(0))
        )

        # Filter for batches created by the current user OR batches with quantity > 100
        if self.request.user.is_authenticated:
            queryset = queryset.filter(
                Q(created_by=self.request.user) | Q(quantity__gt=100)
            )
            
        return queryset

    def get_context_data(self, **kwargs):
        """
        Adds aggregated data to the context.
        """
        context = super().get_context_data(**kwargs)
        context['total_quantity_all_batches'] = ProductionBatch.objects.aggregate(total_quantity=Sum('quantity'))['total_quantity']
        return context

class ProductionBatchViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows production batches to be viewed or edited.
    """
    queryset = ProductionBatch.objects.all()
    serializer_class = ProductionBatchSerializer

    @action(detail=True, methods=['post'])
    def start_production(self, request, pk=None):
        """
        A custom action to simulate starting a production run.
        """
        batch = self.get_object()
        # In a real application, this is where you would trigger the production process.
        # For this simulation, we'll just return a success message.
        return Response(
            {'status': f'Production started for batch #{batch.id}'},
            status=status.HTTP_200_OK
        )
