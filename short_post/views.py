from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

class HomeView(LoginRequiredMixin,generic.TemplateView):
    """
    ホーム画面用View
    """
    template_name ="short_post/home.html"

class TimeLineView(LoginRequiredMixin,generic.TemplateView):
    """
    タイムライン画面用View
    """
    template_name ="short_post/timeline.html"

