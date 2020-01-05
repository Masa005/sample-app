from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

class HomeView(LoginRequiredMixin,generic.TemplateView):
    """
    ホーム画面用View
    """
    template_name ="short_post/home.html"

