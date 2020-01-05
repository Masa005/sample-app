from django.shortcuts import redirect
from django.views import generic

def init(request):
    """
    sample_app初期表示用View
    """
    return redirect('account:login')

class ErrorView(generic.TemplateView):
    """
    エラーページ用View
    """
    template_name ='error.html'
