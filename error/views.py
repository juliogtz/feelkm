from django.shortcuts import render
from django.views.decorators.cache import cache_page
from api.models import users, comments_events, photos, events, events_favorites


# Create your views here.

@cache_page(60)
def e_404(request):

     if request.user.is_active:
        if request.user.is_authenticated:
            DATALOGIN_ID=request.user.id
            DATALOGIN = users.objects.get(id_user_admin_id=DATALOGIN_ID)
        else:
            DATALOGIN="0"
     else:
        DATALOGIN="0"

     return render(request, 'Error/404.html', {
        "DATALOGIN":DATALOGIN,
        })
