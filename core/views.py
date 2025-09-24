from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator

from .decorators import role_required
from .models import Profile

class HomeView(LoginRequiredMixin, TemplateView):
    """
    A general landing page for any authenticated user.
    """
    template_name = 'core/home.html'

@method_decorator(role_required(allowed_roles=[Profile.Role.FACTORY_MANAGER]), name='dispatch')
class FactoryManagerDashboardView(LoginRequiredMixin, TemplateView):
    """
    A dashboard view restricted to users with the 'Factory Manager' role.
    """
    template_name = 'core/factory_manager_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_role'] = self.request.user.profile.get_role_display()
        return context
