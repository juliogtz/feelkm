from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from api.models import users, comments_events, photos, events, events_favorites
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from datetime import *
import cloudinary
import cloudinary.uploader
import cloudinary.api
from FeelKm.Bing.bing_search import bing_search
import random
import urllib
from decimal import *
from django.core.cache import cache
from django.views.decorators.cache import cache_page
cloudinary.config(
  cloud_name = "htyoqtggc",
  api_key = "961935933259211",
  api_secret = "COwH0OL6qwHv5fhjD0ey2TjSdTo"
)

# Create your views here.
@cache_page(60)
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


@cache_page(60)
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

        photos_events=[]
        photos_events_arg=[]
        Cont_Arg=[]
        calif_args = []
        for data_pic in events_list:
            pics = photos.objects.filter(id_event=data_pic.id)
            photos_events.append({data_pic.id:pics})
            photos_events_arg.append({int(data_pic.id):pics})

            # Comments:
            com = comments_events.objects.filter(id_event=data_pic.id)
            count_c = com.count()
            Cont_Arg.append(count_c)

            # Califs
            calif_sum=0
            calif_avg=0
            last_comment=""
            for califs in com:
                calif_sum=calif_sum+califs.calif
                last_comment= califs.title_comment

            if(len(com)>0):
                calif_avg = calif_sum / len(com)
            else:
                calif_avg=0

            calif_args.append({int(data_pic.id): [calif_avg, last_comment, count_c ]})


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
                'photos_events':photos_events,
                'photos_events_arg':photos_events_arg,
                'calif_args':calif_args,
                'error_message': "You didn't select a choice.",
                'query': query,
                'count': count,
                'cont_arg':Cont_Arg,
                'countem':0,
                "DATALOGIN":DATALOGIN,
                "objPic":object

            })

@cache_page(60)
def SepecificEvent(request, id, year, month, day):

    data = events.objects.filter(id=id)
    data2 = events.objects.get(id=id)
    com = comments_events.objects.filter(id_event=id)
    com2 = comments_events.objects.filter(id_event=data2).order_by('-date')

    #Pics event:
    photos_events=[]
    pics = photos.objects.filter(id_event=data2.id)
    photos_events.append({data2.id:pics})

    comments_arg=[]

    for cox in com2:
        usr_aux= users.objects.get(id_user_admin=cox.id_user_admin)
        comments_arg.append({'id_facebook':usr_aux.id_facebook, 'pic_url':usr_aux.pic_url, 'city':usr_aux.city, 'region':usr_aux.region, 'country':usr_aux.country, 'first_name':cox.id_user_admin.first_name, 'last_name':cox.id_user_admin.last_name, 'comment':cox })
        #comments_arg.append({'id_user_damin':})

    # Califs
    calif_sum=0
    calif_avg=0
    number_comments=com.count()
    for califs in com:
        calif_sum=calif_sum+califs.calif
    if(len(com)>0):
        calif_avg = calif_sum / len(com)
    else:
        calif_avg=0

    # Data Login:
    number_favorites = 0
    if request.user.is_active:
            if request.user.is_authenticated:
                DATALOGIN_ID=request.user.id
                DATALOGIN = users.objects.get(id_user_admin_id=DATALOGIN_ID)
                # Favorites User Events:
                favorites = events_favorites.objects.filter(id_user_admin=request.user.id, id_event=id)
                number_favorites = favorites.count()
            else:
                 DATALOGIN="0"
    else:
            DATALOGIN="0"


    # Numbers of califs:
    calif_1 = comments_events.objects.filter(calif=1, id_event=id)
    calif_1_count= calif_1.count()
    if(number_comments>0):
        calif_1_count_p=(float(calif_1_count)/float(number_comments))*100
        calif_1_count_p=(70.0*calif_1_count_p)/100
        calif_1_count_p=int(calif_1_count_p)
    else:
        calif_1_count_p=0

    calif_2 = comments_events.objects.filter(calif=2, id_event=id)
    calif_2_count= calif_2.count()
    if(number_comments>0):
        calif_2_count_p=(float(calif_2_count)/float(number_comments))*100
        calif_2_count_p=(70.0*calif_2_count_p)/100
        calif_2_count_p=int(calif_2_count_p)
    else:
        calif_2_count_p=0

    calif_3 = comments_events.objects.filter(calif=3, id_event=id)
    calif_3_count= calif_3.count()
    if(number_comments>0):
        calif_3_count_p=(float(calif_3_count)/float(number_comments))*100
        calif_3_count_p=(70.0*calif_3_count_p)/100
        calif_3_count_p=int(calif_3_count_p)
    else:
        calif_3_count_p=0

    calif_4 = comments_events.objects.filter(calif=4, id_event=id)
    calif_4_count= calif_4.count()
    if(number_comments>0):
        calif_4_count_p=(float(calif_4_count)/float(number_comments))*100
        calif_4_count_p=(70.0*calif_4_count_p)/100
        calif_4_count_p=int(calif_4_count_p)

    else:
        calif_4_count_p=0

    calif_5 = comments_events.objects.filter(calif=5, id_event=id)
    calif_5_count= calif_5.count()
    if(number_comments>0):
        calif_5_count_p=(float(calif_5_count)/float(number_comments))*100
        calif_5_count_p=(70.0*calif_5_count_p)/100
        calif_5_count_p=int(calif_5_count_p)

    else:
        calif_5_count_p=0

    return render(request, 'Search/event.html', {

                'poll': 1,
                'id':id,
                'year':year,
                'month':month,
                'day':day,
                'data':data,
                'DATALOGIN':DATALOGIN,
                'calif_avg':calif_avg,
                'comments':com,
                'data2':data2,
                'number_comments':number_comments,
                'number_favorites':number_favorites,
                'photos_events':photos_events,
                'calif_1_count':calif_1_count,
                'calif_2_count':calif_2_count,
                'calif_3_count':calif_3_count,
                'calif_4_count':calif_4_count,
                'calif_5_count':calif_5_count,
                'calif_1_count_p':calif_1_count_p,
                'calif_2_count_p':calif_2_count_p,
                'calif_3_count_p':calif_3_count_p,
                'calif_4_count_p':calif_4_count_p,
                'calif_5_count_p':calif_5_count_p,
                'comments_arg':comments_arg,
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
                    calif_organizacion=request.POST['calif_organizacion']
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


@csrf_protect
def CreateCommentSend(request):
    if request.user.is_active:
        if request.user.is_authenticated:
                 if request.method == 'POST':
                     usr_usr=request.user.id
                     id_user_instance = User.objects.get(id=usr_usr)
                     id_event = request.POST["id_event_"]
                     id_event_instance = events.objects.get(id=id_event)
                     today = date.today()
                     urlevent=request.POST["urlevent"]


                     for filename, file in request.FILES.iteritems():

                           file_txt=request.FILES[filename].name
                           file_txt=file_txt.split(".")
                           if(file_txt[1]=="jpeg"  or file_txt[1]=="jpg" or file_txt[1]=="png" or file_txt[1]=="gif"):

                                #try:
                                    json=cloudinary.uploader.upload(
                                          request.FILES[filename],
                                          public_id = file_txt[0],
                                          crop = 'limit',
                                          #width = 2000,
                                          #height = 2000,
                                          eager = [
                                            { 'width': 200, 'height': 200,
                                              'crop': 'thumb', 'gravity': 'face',
                                              'radius': 20, 'effect': 'sepia' },
                                            { 'width': 100, 'height': 150,
                                              'crop': 'fit', 'format': 'png' }
                                          ],
                                          tags = ['']
                                          )

                                    photos.objects.create(id_event=id_event_instance, id_user_admin=id_user_instance, file=file_txt[0], title=file_txt[0], date=today, status=1, json = json)

                                #except:
                                 #   print "hey!"

                     return HttpResponseRedirect(str(urlevent))
                     #return HttpResponse("0")
                 else:
                     return HttpResponseRedirect("/")
                     #return HttpResponse("2")

        else:

            return HttpResponseRedirect("/")
    else:

        return HttpResponseRedirect("/")


def return_image(request, id):

    data = events.objects.get(id=id)
    name_event=data.name_event
    name_event=name_event.replace("'",' ')
    name_event=name_event.replace("-",' ')
    name_event=name_event.replace('    ',' ')
    name_event=name_event.replace('   ',' ')
    name_event=name_event.replace('  ',' ')
    name_event=name_event.strip()

    #return HttpResponse(''+name_event+''+'%20running%20race+')
    try:
        bing = bing_search(''+name_event+''+' running race', 'Image')
    except ValueError:
         bing = bing_search(''+data.city+' '+data.region+' '+' running race', 'Image')
    except:

         image_data = open("statics/imgs/carrera-a.png", "rb").read()
         #image_data = open(os.path.join(settings.STATIC_ROOT, 'carrera-a.png', 'rb').read()
         return HttpResponse(image_data, mimetype="image/png")


    if (len(bing)>0):

        record_search = bing[random.randrange(len(bing))]
        rg=record_search['Thumbnail']
        try:

            image_data = urllib.urlopen(rg['MediaUrl'], "rb").read()
            return HttpResponse(image_data, mimetype="image/png")

        except:
            image_data = open("statics/imgs/carrera-a.png", "rb").read()
            #image_data = open(os.path.join(settings.STATIC_ROOT, 'carrera-a.png', 'rb').read()
            return HttpResponse(image_data, mimetype="image/png")

    else:

        image_data = open("statics/imgs/carrera-a.png", "rb").read()
        #image_data = open(os.path.join(settings.STATIC_ROOT, 'carrera-a.png', 'rb').read()
        return HttpResponse(image_data, mimetype="image/png")

@cache_page(60)
def favorites(request):

    if request.method == 'POST':
        if request.user.is_active:
            if request.user.is_authenticated:
                favorite_request = request.POST['stf']

                id_event = events.objects.get(id=int(request.POST['id_event']))
                id_user_instance = User.objects.get(id=request.user.id)

                if(str(favorite_request)=="1"):
                    # Add Favorite this event

                    try:
                        today = date.today()

                        events_favorites.objects.create(id_event=id_event, id_user_admin=id_user_instance, date=today)

                        return HttpResponse("1")
                    except:
                        return HttpResponse("-1")



                if(str(favorite_request)=="0"):
                    # Remove Favorite this event

                    try:

                        favorite=events_favorites.objects.get(id_event=id_event, id_user_admin=id_user_instance)
                        favorite.delete()

                        return HttpResponse("1")
                    except:
                        return HttpResponse("-2")


            else:
                return HttpResponse("-3")
        else:
            return HttpResponse("-4")
    else:
        return HttpResponseRedirect("/")


