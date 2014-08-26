from django.shortcuts import render
from django.views.decorators.cache import cache_page

# Create your views here.

@cache_page(60)
def e_404(request):

    return render(request, 'Error/404.html', {

        })
