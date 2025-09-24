from django.apps import AppConfig


class ProductionPlannerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'production_planner'

    def ready(self):
        import production_planner.signals
