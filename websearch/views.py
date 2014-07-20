from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
#from rest_framework.decorators import api_view
#from rest_framework.response import Response
#from api.serializers import SinippetSerializer
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import *
from api.models import users, comments_events, photos, events
from django.contrib.auth.models import User, Permission, check_password, is_password_usable
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from datetime import *

# Create your views here.

def LandingWeb(request):
    if request.user.is_active:
        if request.user.is_authenticated:
            DATALOGIN_ID=request.user.id
            DATALOGIN = users.objects.get(id_user_admin_id=DATALOGIN_ID)
        else:
            DATALOGIN="0"
    else:
        DATALOGIN="0"

    return render(request, 'Home/home.html', {
            'poll': 1,
            'error_message': "You didn't select a choice.",
            'DATALOGIN':DATALOGIN

        })


def SearchWeb(request):

        query= request.GET.get('q','')
        snippets= events.objects.filter( Q(name_event__icontains=query) | Q(city__icontains=query) | Q(region__icontains=query) | Q(country__icontains=query) | Q(description__icontains=query) | Q(distan_txt__icontains=query) | Q(distan_txt__icontains=query) | Q(short_desc__icontains=query) | Q(region_l__icontains=query)).order_by('-date_event')
        count = snippets.count()
        paginator = Paginator(snippets, 10) # Show 10 events per page

        #Get the number of comments:

        page = request.GET.get('page')
        try:
            events_list = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            events_list = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            events_list = paginator.page(paginator.num_pages)

        Cont_Arg = []
        for data_events in events_list:
            com = comments_events.objects.filter(id_event=data_events.id)
            count_c = com.count()
            Cont_Arg.append(count_c)
            print count_c


        if request.user.is_active:
            if request.user.is_authenticated:
                DATALOGIN_ID=request.user.id
                DATALOGIN = users.objects.get(id_user_admin_id=DATALOGIN_ID)
            else:
                 DATALOGIN="0"
        else:
            DATALOGIN="0"


        return render(request, 'Search/search.html', {
                'poll': 1,
                'data': events_list,
                'error_message': "You didn't select a choice.",
                'query': query,
                'count': count,
                'cont_arg':Cont_Arg,
                'countem':0,
                "DATALOGIN":DATALOGIN,

            })


def SepecificEvent(request, id, year, month, day):


    data = events.objects.filter(id=id)

    if request.user.is_active:
            if request.user.is_authenticated:
                DATALOGIN_ID=request.user.id
                DATALOGIN = users.objects.get(id_user_admin_id=DATALOGIN_ID)
            else:
                 DATALOGIN="0"
    else:
            DATALOGIN="0"

    return render(request, 'Search/event.html', {
                'poll': 1,
                'id':id,
                'year':year,
                'month':month,
                'day':day,
                'data':data,
                'DATALOGIN':DATALOGIN

            })



def NewCommentEvent(request, id, month, day, year):



    if request.user.is_active:
            if request.user.is_authenticated:
                DATALOGIN_ID=request.user.id
                DATALOGIN = users.objects.get(id_user_admin_id=DATALOGIN_ID)
                data = events.objects.get(id=id)

                return render(request, 'Search/new_comment.html', {
                'poll': 1,
                'id':id,
                'data':data,
                'year':year,
                'month':month,
                'day':day,
                'DATALOGIN':DATALOGIN
                 })

            else:
                 DATALOGIN="0"
                 return HttpResponseRedirect("/")
    else:
            DATALOGIN="0"
            return HttpResponseRedirect("/")



@csrf_exempt
def CreateComment(request):
    if request.user.is_active:
        if request.user.is_authenticated:
                 if request.method == 'POST':
                    usr_usr=request.user.id
                    id_user_instance = User.objects.get(id=usr_usr)
                    id_event = request.POST["id_event"]
                    id_event_instance = events.objects.get(id=id_event)
                    title_comment = request.POST['title_comment']
                    comments=request.POST['comments']
                    accept=request.POST['accept']
                    particiate=request.POST['particiate']
                    year_run=request.POST['year_run']
                    calif_general=request.POST['calif_general']
                    calif_organizacion=request.POST['calif_general']
                    calif_hidratacion=request.POST['calif_hidratacion']
                    calif_ruta=request.POST['calif_ruta']
                    calif_parking=request.POST['calif_parking']
                    calif_ambiente=request.POST['calif_ambiente']
                    calif_music=request.POST['calif_music']
                    calif_medalla=request.POST['calif_medalla']
                    calif_salida=request.POST['calif_salida']
                    calif_meta=request.POST['calif_meta']
                    calif_seguridad=request.POST['calif_seguridad']
                    calif_wc=request.POST['calif_wc']
                    STATUS_FILE_1=request.POST['STATUS_FILE_1']
                    STATUS_FILE_2=request.POST['STATUS_FILE_2']
                    STATUS_FILE_3=request.POST['STATUS_FILE_3']

                    # Make date:
                    today = date.today()

                    if(title_comment=="" or comments==""):
                        return HttpResponse("-1")
                    else:
                        # Max characters of title_comment:
                        # Max characters of comments:
                        if(len(title_comment)>50):
                            return HttpResponse("-2")
                        else:
                            if(len(comments)>450):
                                return HttpResponse("-3")
                            else:
                                if(particiate=="0"):
                                #Save comment, this person never been run this event.
                                    comments_events.objects.create(id_event=id_event_instance, id_user_admin=id_user_instance, title_comment=title_comment, comment=comments, cer=accept, participado=particiate, year_run=year_run, calif=calif_general, hidr=calif_hidratacion, route=calif_ruta, parking=calif_parking, enviroment=calif_ambiente, music=calif_music, medl=calif_medalla, salida=calif_salida, meta=calif_meta, seguridad=calif_seguridad, toilets=calif_wc, org=calif_organizacion, status=1, date=today)
                                    return HttpResponse("1")
                                else:
                                    if(calif_general=="0"):
                                        return HttpResponse("-4")
                                    else:
                                        if(year_run=="0"):
                                            return HttpResponse("-5")
                                        else:
                                            if(calif_hidratacion=="0" or calif_ruta=="0" or calif_parking=="0" or calif_ambiente=="0" or calif_music=="0" or calif_medalla=="0" or calif_salida=="0" or calif_meta=="0" or  calif_seguridad=="0" or calif_wc=="0"):
                                                return HttpResponse("-6")
                                            else:
                                                if(accept==0):
                                                    return HttpResponse("-7")
                                                else:
                                                    #Validate pics if the user upload
                                                    #Crear comentario
                                                    creatc=comments_events.objects.create(id_event=id_event_instance, id_user_admin=id_user_instance, title_comment=title_comment, comment=comments, cer=accept, participado=particiate, year_run=year_run, calif=calif_general, hidr=calif_hidratacion, route=calif_ruta, parking=calif_parking, enviroment=calif_ambiente, music=calif_music, medl=calif_medalla, salida=calif_salida, meta=calif_meta, seguridad=calif_seguridad, toilets=calif_wc, org=calif_organizacion, status=1, date=today)
                                                    return HttpResponse("1")


                 else:
                     return HttpResponseRedirect("/")

        else:

            return HttpResponseRedirect("/")
    else:


        return HttpResponseRedirect("/")


@csrf_exempt
def CreateCommentSend(request):
    if request.user.is_active:
        if request.user.is_authenticated:
                 if request.method == 'POST':
                     return HttpResponse("hola")
                 else:
                     return HttpResponseRedirect("/")

        else:

            return HttpResponseRedirect("/")
    else:

        return HttpResponseRedirect("/")